import pytest
from utilities.global_env import GlobalConfig
from api_classes.file_cloud_api import FileCloudApi

global_config = GlobalConfig()

@pytest.fixture(scope='session')
def load_env(request):
    """ All the global configuration like env variable, secrets, commondata are stored in config class"""
    return global_config

@pytest.fixture(scope='session')
def get_cookies(load_env):
    """ cookies is the base for all API call, with help of fixture this value will be available before all test  cases"""
    file_cloud_api = FileCloudApi(base_url= load_env.get_base_url())
    params={ 'userid' : global_config.get_guest_username(), 'password' : global_config.get_guest_password() }
    res = file_cloud_api.login_guest(params=params)
    if res.status_code == 200:
        return res.cookies
    else:
        raise Exception(f'Cookie is not found for the user {global_config.get_guest_username()}')

@pytest.fixture(scope='session')   
def get_common_data(load_env, get_cookies):
    """ add the data and cookie fixture as a single fixture """
    return { 'env' : load_env, 'cookies': get_cookies }


def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test classes run in a given order."""
    CLASS_ORDER = ["TestLoadUserData", "TestUsersAndGroups", "TestUploadFile"]
    class_mapping = {item: item.cls.__name__ for item in items}

    sorted_items = items.copy()
    # Iteratively move tests of each class to the end of the test queue
    for class_ in CLASS_ORDER:
        sorted_items = [it for it in sorted_items if class_mapping[it] != class_] + [
            it for it in sorted_items if class_mapping[it] == class_
        ]
    items[:] = sorted_items