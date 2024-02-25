""" web api for www.pyanywhere.com and eu.pyanywhere.com

"""
import os
import requests

from typing import Callable, Optional, Sequence

from ae.base import PY_INIT                                 # type: ignore
from aedev.setup_project import code_version                # type: ignore


__version__ = '0.3.1'


class Pythonanywhere:
    """ remote host api to the web hosts eu.pythonanywhere.com and pythonanywhere.com. """

    def __init__(self, web_domain: str, web_user: str, web_token: str):
        """ initialize web host api.

        :param web_domain:      remote web host domain.
        :param web_user:        remote connection username.
        :param web_token:       personal user credential token string on remote host.
        """
        self.error_message = ""

        # self.web_domain = web_domain
        self.web_user = web_user
        # self.web_token = web_token

        self.base_url = f"https://{web_domain}/api/v0/user/{web_user}/"
        self.protocol_headers = {'Authorization': f"Token {web_token}"}

    def _request(self, url_path: str, task: str, method: Callable = requests.get, success_codes: Sequence = (200, 201),
                 **request_kwargs) -> requests.Response:
        """ send a https request specified via :paramref:`.method` and return the response.

        :param url_path:        sub url path to send request to.
        :param task:            string describing the task to archive (used to compile an error message).
        :param method:          requests method (get, post, push, delete, patch, ...).
        :param success_codes:   sequence of response.status_code success codes
        :param request_kwargs:  additional request method arguments.
        :return:                request response. the :attr:`.error_message` will be set on error, else reset to "".
        """
        response = method(f"{self.base_url}{url_path}", headers=self.protocol_headers, **request_kwargs)
        if response.status_code in success_codes:
            self.error_message = ""
        else:
            self.error_message = (f"error '{response.status_code}:{response.reason}'"
                                  f" {task} via '{self.base_url}{url_path}'")
        return response

    def deployed_file_content(self, package_name: str, file_path: str) -> Optional[bytes]:
        """ determine the file content of a file deployed to a web server.

        :param package_name:    name of the web project package.
        :param file_path:       path of a deployed file relative to the project root.
        :return:                file content as bytes or None if error occurred (check self.error_message).
        """
        url_path = f"files/path/home/{self.web_user}/{package_name}/{file_path}"
        response = self._request(url_path, "fetching file content")
        if self.error_message:
            return None
        return response.content

    def delete_file_or_folder(self, package_name: str, file_path: str) -> str:
        """ delete a file or folder on the web server.

        :param package_name:    name of the web project package.
        :param file_path:       path relative to the project root of the file to be deleted.
        :return:                error message if deletion failed else on success an empty string.
        """
        url_path = f"files/path/home/{self.web_user}/{package_name}/{file_path}"
        self._request(url_path, f"deleting file {file_path}", method=requests.delete, success_codes=(204, ))
        return self.error_message

    def deploy_file(self, package_name: str, file_path: str, file_content: bytes) -> str:
        """ add or update a project file to the web server.

        :param package_name:    name of the web project package.
        :param file_path:       path relative to the project root of the file to be deployed (added or updated).
        :param file_content:    file content to deploy/upload.
        :return:                error message if update/add failed else on success an empty string.
        """
        url_path = f"files/path/home/{self.web_user}/{package_name}/{file_path}"
        self._request(url_path, f"deploy file {file_path}", method=requests.post, files={'content': file_content})
        return self.error_message

    def deployed_version(self, package_name: str) -> str:
        """ determine the version of a deployed django project package.

        :param package_name:    name of the web project package.
        :return:                version string of the package deployed to the web host/server
                                or empty string if package version file or version-in-file not found.
        """
        init_file_content = self.deployed_file_content(package_name, os.path.join(package_name, PY_INIT))
        return "" if init_file_content is None else code_version(init_file_content)

    def find_package_files(self, package_name: str, file_path: str = "",
                           exclude: Callable[[str], bool] = lambda _: _ in ('media', 'media_ini', 'static')
                           ) -> Optional[set[str]]:
        """ determine the package files deployed onto the app/web server.

        not using the files tree api endpoints/function (f"files/tree/?path=/home/{self.web_user}/{package_name}")
        because their response is limited to 1000 files
        (see https://help.pythonanywhere.com/pages/API#apiv0userusernamefilestreepathpath) and e.g. kairos has more
        than 5300 files in its package folder (mainly for django filer and the static files).

        :param package_name:    name of the project package.
        :param file_path:       folder path relative to the project root to be searched (not ending with a slash).
        :param exclude:         called for each found file with the file_path relative to the package root folder
                                as argument, returning True to exclude the specified file. if not passed then the
                                following project root folders will be excluded: 'media', 'media_ini', 'static'.
        :return:                set of file paths of the package deployed on the web, relative to the project root
                                or None if an error occurred.
        """
        url_path = f"files/path/home/{self.web_user}/{package_name}/"
        if file_path:
            url_path += file_path + '/'
        response = self._request(url_path, f"fetching files in folder {file_path}")
        if self.error_message:
            return None

        try:
            folder_dict = response.json()
        except Exception as exc:   # requests.exceptions.JSONDecodeError
            self.error_message = f"{exc} in response.json() call on response content '{response.content!r}'"
            return None

        folder_files = set()
        for entry, attr in folder_dict.items():
            found_file_path = os.path.join(file_path, entry)
            if attr['type'] == 'directory':
                sub_dir_files = self.find_package_files(package_name, file_path=found_file_path, exclude=exclude)
                if sub_dir_files:
                    folder_files.update(sub_dir_files)
            elif not exclude(found_file_path):
                folder_files.add(found_file_path)

        return folder_files
