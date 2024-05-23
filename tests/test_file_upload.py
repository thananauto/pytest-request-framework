from api_classes.file_cloud_api import FileCloudApi
from utilities.read_test_data import upload_file_path
import pytest

class TestUploadFile:

    @pytest.mark.upload
    def test_file_exists(self, load_env, get_cookies):
      """ verify whether the file exists in file cloud server"""
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      file_name = upload_file_path()['filename']
      # check file exists in given path
      file_params = {'file' : f'/{load_env.get_guest_username()}/{file_name}', 'caseinsensitive' : 1}
      # check the file exists
      file_exists = file_cloud_api.get_file_exists(params=file_params)
      assert file_exists.status_code == 200, 'Check for file exists'
      assert file_exists.json()['command'][0]['result'] == 1


    
    @pytest.mark.upload
    def test_file_have_version(self, load_env, get_cookies):
      """ verify give file have multiple version"""
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      file_name = upload_file_path()['filename']
      file_params = {'filepath' : f'/{load_env.get_guest_username()}', 'filename' : file_name}
      # get the files version as list
      file_version =  file_cloud_api.get_file_versions(params=file_params)
      assert file_version.status_code == 200
      assert len(file_version.json()['version']) == 4
      
    @pytest.mark.upload  
    def test_make_previous_verion_live(self, load_env, get_cookies):
      """ verify make the previous version as the current version"""
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      file_name = upload_file_path()['filename']
      file_params = {'filepath' : f'/{load_env.get_guest_username()}', 'filename' : file_name}
      # get the list of versions and get the previous id
      file_version =  file_cloud_api.get_file_versions(params=file_params)
      assert file_version.status_code == 200

      prvs_version_id = file_version.json()['version'][1]['fileid']
      prvs_version_params = {'filepath' : f'/{load_env.get_guest_username()}', 'filename' : file_name, 'fileid': prvs_version_id}
      # make the previous version live
      file_version =  file_cloud_api.get_make_version_live(params=prvs_version_params)
      assert file_version.status_code == 200 
      file_version =  file_cloud_api.get_file_versions(params=file_params)

      # compare  the current version with previous version
      assert file_version.status_code == 200
      assert file_version.json()['version'][0]['fileid'] == prvs_version_id


    @pytest.mark.upload
    def test_copy_file(self, load_env, get_cookies):
      """ Verify copy the file to the new directory"""
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      file_name = upload_file_path()['filename']
      file_params = {'path' : f'/{load_env.get_guest_username()}', 'name' : file_name, 'overwrite' : 1, 'copyto' : f'/{load_env.get_guest_username()}/Media' }
      # get the list of versions and get the previous id
      file_version =  file_cloud_api.get_copy_file(params=file_params)
      assert file_version.status_code == 200
      assert file_version.json()['command'][0]['result'] == 1

    @pytest.mark.upload 
    def test_x_delete_file_version(self, load_env, get_cookies):
      """ verify the particular version of file to be deleted"""
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      
      file_name = upload_file_path()['filename']
      file_params = {'filepath' : f'/{load_env.get_guest_username()}', 'filename' : file_name}
      # get the list of versions and get the previous id
      file_version =  file_cloud_api.get_file_versions(params=file_params)
      assert file_version.status_code == 200

      first_version_id = file_version.json()['version'][-1]['fileid']
      prvs_version_params = {'filepath' : f'/{load_env.get_guest_username()}', 'filename' : file_name, 'fileid': first_version_id}
      # make the previous version live
      file_version =  file_cloud_api.get_delete_file_version(params=prvs_version_params)
      assert file_version.status_code == 200 
      assert file_version.json()['command'][0]['result'] == 1
      
    @pytest.mark.upload
    def test_y_delete_file(self, load_env, get_cookies):
      """ verify file can be deleted """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      
      file_name = upload_file_path()['filename']
      file_params = {'path' : f'/{load_env.get_guest_username()}', 'name' : file_name}
      # get the list of versions and get the previous id
      file_version =  file_cloud_api.get_delete_file(params=file_params)
      assert file_version.status_code == 200
      assert file_version.json()['command'][0]['result'] == 1


