""" unit tests for aedev_pythonanywhere module package.

minimal testing because of the rate-limits on pythonanywhere.com (each endpoint has a 40 requests per minute rate limit,
apart from the send_input endpoint on consoles, which is 120 requests per minute - see
`https://help.pythonanywhere.com/pages/API`__ for more details).
"""
import os
import pytest
import requests

from conftest import skip_gitlab_ci
from unittest.mock import patch

from ae.base import PY_INIT, norm_name
from aedev.pythonanywhere import Pythonanywhere


@pytest.fixture
def connection():
    """ provide a connected Gitlab remote repository api. """
    web_domain = "www.pythonanywhere.com"
    web_user = "AndiEcker"
    from dotenv import load_dotenv
    load_dotenv()
    web_token = os.environ.get(f'AE_OPTIONS_WEB_TOKEN_AT_{norm_name(web_domain).upper()}')

    remote_connection = Pythonanywhere(web_domain, web_user, web_token)

    yield remote_connection


def test_pythonanywhere_init():
    """ test the initialization of the module (and having one test case on gitlab ci). """
    assert requests         # for json() patching
    assert Pythonanywhere


@skip_gitlab_ci  # skip on gitlab because of missing remote repository user account token
class TestLocallyOnly:
    def test_deploy_file(self, connection):
        package_name = 'grm_tests'
        file_path = os.path.join(package_name, PY_INIT)
        dep_version = '3.6.9'
        file_content = f'""" test package doc string. """\n\n__version__ = \'{dep_version}\'\n'.encode()

        assert not connection.deploy_file(package_name, file_path, file_content)

        assert connection.deployed_file_content(package_name, file_path) == file_content

        assert connection.deployed_version(package_name) == dep_version

        assert not connection.delete_file_or_folder(package_name, file_path)   # delete test file
        assert not connection.delete_file_or_folder(package_name, "")          # also delete test folder

    def test_find_package_files(self, connection):
        package_name = 'grm_find_tests'
        file3 = "test2/sub2/file3.z"
        file_paths = {"test1/file1.x", "test1/file2.y", file3}
        for fil_pat in file_paths:
            assert not connection.deploy_file(package_name, fil_pat, b"content of " + fil_pat.encode())

        assert connection.find_package_files("not_existing_package_name") is None   # test error
        assert connection.error_message

        def _raise_json_err():
            raise Exception
        with patch('requests.Response.json', _raise_json_err):
            assert connection.find_package_files(package_name) is None  # simulate broken response.content for coverage

        found_paths = connection.find_package_files(package_name)
        assert found_paths == file_paths

        found_paths = connection.find_package_files(package_name, "test2")
        assert found_paths == {file3}

        found_paths = connection.find_package_files(package_name, exclude=lambda _: "3" not in _)
        assert found_paths == {file3}

        assert not connection.delete_file_or_folder(package_name, "test1")      # delete test1 folder with content
        assert not connection.delete_file_or_folder(package_name, "")           # finally delete test root folder
