import  pytest
from utilities.read_test_data import json_user_group_data, upload_file_path
from api_classes.file_cloud_api import FileCloudApi


class TestLoadUserData:
      
   @pytest.mark.user
   @pytest.mark.group
   @pytest.mark.parametrize("group, users", json_user_group_data())
   def test_load_groups_and_users(self, load_env, get_cookies, group, users):
      """ 
         This method acts as a test case and as well set up data for future cases
      """
      # search for a group
      base_url = load_env.get_base_url()
      default_password = load_env.get_default_password()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)

      # check whether the group already exists
      search_params = { 'start' :0, 'limit' : 100, 'filter' : f'{group}' }
      search_group = file_cloud_api.search_group(params=search_params)
      group_id = ''

      assert search_group.status_code == 200, f'Search for the group {group} is failed'
      #if group not exists, create a group
      if search_group.json()['meta']['total'] == 0 :
         group_email =  group.replace(' ','_')+'@email.com'
          
         add_params = { 'groupname' : f'{group}', 'groupemail' : group_email }
         add_group = file_cloud_api.add_group(params=add_params)#requests.post(f'{base_url}/core/addgroup', params= add_params, cookies= get_cookies, headers=headers)

         assert add_group.status_code == 200, f'create a group: {group} status code is not 200'
         assert add_group.json()['command'][0]['result'] == 1, 'Group: {group} is not successfully created'
         # create the group and get the ID by search the same group
         search_params = { 'start' :0, 'limit' : 100, 'filter' : f'{group}' }
         search_group = file_cloud_api.search_group(params=search_params)#requests.get(f'{base_url}/core/searchgroups', params= search_params, cookies= get_cookies, headers=headers)
         group_id = search_group.json()['group'][0]['groupid']
        
      else:
          # If group exist get the group id
          group_id = search_group.json()['group'][0]['groupid']

      # searh for a user is present, if nor create a  new user
      for user in users:
         user_email = user.replace(' ','_')+'@email.com'
         search_profile_params = { 'filter' : f'{user}', 'context' : 'usergroup' }
         search_profile = file_cloud_api.search_user(params=search_profile_params)#requests.post(f'{base_url}/core/searchprofiles', params= search_profile_params, cookies= get_cookies, headers=headers)
         
         if( search_profile.status_code == 200 and len(search_profile.json()) == 0 ):
            # create a user
            create_user_params = { 'profile' : f'{user}', 'email' : user_email, 'password' : default_password }
            create_user =  file_cloud_api.create_user(params=create_user_params)#requests.post(f'{base_url}/core/createprofile', params= create_user_params, cookies= get_cookies, headers=headers)

            assert create_user.status_code == 200, f'Creation of username {user} is failed'
            assert create_user.json()['command'][0]['result'] == 1, f'Username {user} creation is not successfull'
   
      # add user to the group
         add_user_params = { 'groupid' : group_id, 'username' : user.lower() } 
         add_user_res = file_cloud_api.add_user_to_group(params=add_user_params)#requests.post(f'{base_url}/core/addgroupmember', params= add_file_cloud_api_params, cookies= get_cookies, headers=headers)

         if(add_user_res.status_code == 200):
            assert add_user_res.json()['command'][0]['result'] == 1, f'User: {user} is not successfully added to group: {group}'
         elif(add_user_res.status_code == 400):
             assert add_user_res.json()['command'][0]['result'] == 0, f'User: {user} is not already in group: {group}'
         else:
            assert False, f'There is an error while try to add user: {user} to group: {group}'


   @pytest.mark.upload
   def test_upload_file(self, load_env, get_cookies):
      """ 
         This test case act as individual case and upload the file for future test case
      """
        # search for a group
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)

      # check whether the group already exists
      upload_params = {'appname': 'explorer', 'path': f'/{load_env.get_guest_username()}', 'offset': 0}
      
      upload_file = file_cloud_api.get_upload_file(params=upload_params,file=upload_file_path())

      assert upload_file.status_code == 200, 'verify file uploaded successfully'
      assert upload_file.text == 'OK'

      # for upcoming scenario data validation upload the same file 5 times

      for i in range(4):
          upload_file = file_cloud_api.get_upload_file(params=upload_params,file=upload_file_path())

     