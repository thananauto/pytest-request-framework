import json, pytest
from utilities.read_test_data import json_user_group_data, json_email_exist_data, faker
from utilities.parse_xml import getXmlValue_with_keyword, getXmlValue_with_path
from api_classes.file_cloud_api import FileCloudApi


class TestUsersAndGroups:

   @pytest.mark.group
   @pytest.mark.parametrize("group, users", json_user_group_data())
   def test_group_size(self, load_env, get_cookies, group, users):
      """ 
         Validate the members size in group is same as added members to the group 
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      search_params = { 'start' :0, 'limit' : 100, 'filter' : f'{group}' }
      search_group = file_cloud_api.search_group(params=search_params)#requests.get(f'{base_url}/core/searchgroups', params= search_params, cookies= get_cookies, headers=headers)
      group_name = search_group.json()['group'][0]['groupname']
      group_count = search_group.json()['group'][0]['membercount']
      # compare group name and group count
      assert group_name == group, 'Expecting value = group: {group}, Actual: {group_name}'
      assert len(users) == group_count, 'Users size and Group members size are not same'

   @pytest.mark.group
   @pytest.mark.parametrize("group, users", json_user_group_data())
   def test_check_group_members(self, load_env, get_cookies, group, users):
      """ 
         Validate the members in the group is as added
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      search_params = { 'start' :0, 'limit' : 100, 'filter' : f'{group}' }
      res = file_cloud_api.get_group_members(params=search_params)

      assert res.status_code == 200
      # traverse the each group member and compare with test data
      for each_group in res.json()['group']:
         if(each_group['groupname'].lower() == group.lower()):
              fin_list = list(map(lambda mem : mem['name'], each_group['members']))
              users = list(map(lambda user : user.lower(), users))
              assert set(fin_list) == set(users), 'Validate members in each group are correct'

   @pytest.mark.user
   def test_create_user_invalid_character(self, load_env, get_cookies): 
      """ 
         Create user with invalid character
      """          
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
       
      create_user_params = { 'profile' : f'${faker.name()}', 'email' : faker.email(), 'password' : faker.password() }
      create_user =  file_cloud_api.create_user(params=create_user_params)

      assert create_user.status_code == 400
      assert create_user.json()['command'][0]['message'] == 'Username can only contain numbers, spaces, hyphens, periods, underscores, and letters from the Latin alphabet (A-Z, uppercase and lowercase)'


   @pytest.mark.user
   def test_username_exists(self, load_env, get_cookies):
      """ 
         Check whether the username exists already
      """
       # create a user
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      create_user_params = { 'profile' : load_env.get_guest_username(), 'email' : faker.email(), 'password' : faker.password() }
      create_user =  file_cloud_api.create_user(params=create_user_params)#requests.post(f'{base_url}/core/createprofile', params= create_user_params, cookies= get_cookies, headers=headers)

      assert create_user.status_code == 400, f'Creation of username {load_env.get_guest_username()} is failed'
      assert create_user.json()['command'][0]['result'] == 0, f'Username {load_env.get_guest_username()} creation is not successfull'
      assert create_user.json()['command'][0]['message'] == 'Username is Not Available', f'Username {load_env.get_guest_username()} creation is not successfull'
   
   @pytest.mark.user
   @pytest.mark.parametrize("email", json_email_exist_data())
   def test_email_exists(self, load_env, get_cookies, email):
      """ 
         verify the given email is already exists
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      create_user_params = { 'profile' : faker.name(), 'email' : email, 'password' : faker.password() }
      create_user =  file_cloud_api.create_user(params=create_user_params)#requests.post(f'{base_url}/core/createprofile', params= create_user_params, cookies= get_cookies, headers=headers)

      assert create_user.status_code == 400, f'Creation of username {load_env.get_guest_username()} is failed'
      assert create_user.json()['command'][0]['result'] == 0, f'Username {load_env.get_guest_username()} creation is not successfull'
      assert create_user.json()['command'][0]['message'] == 'Email already used', f'Username {load_env.get_guest_username()} creation is not successfull'
   
   @pytest.mark.user
   def test_invalid_credentials(self, load_env):
      """ 
         Login in with the invalid credentials
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url)
      params={ 'userid' : faker.name(), 'password' : faker.password() }
      res = file_cloud_api.login_guest(params=params)

      assert res.status_code == 400, 'verify the login with invalid credentials'
      assert res.json()['command'][0]['result'] == 0, 'Invalid login guest'
      assert res.json()['command'][0]['message'] == 'Invalid Username or Password. Password is Case Sensitive.', 'Invalid Error message'

   @pytest.mark.user
   def test_create_user_with_invalid_email(self, load_env, get_cookies):
      """ 
         verify that create profile with invalid email address
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
      email = faker.name()+'@email' 
      create_user_params = { 'profile' : f'{faker.name()}', 'email' : email, 'password' : faker.password() }
      create_user =  file_cloud_api.create_user(params=create_user_params)

      assert create_user.status_code == 422, f'validate create user profile with invalid email address {email}'
      assert create_user.json()['command'][0]['message'] == 'bad request'

   @pytest.mark.user
   def test_create_user_common_password(self, load_env, get_cookies):
      """ 
         verify profile can't be created with commonly used password 
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
     
      create_user_params = { 'profile' : f'{faker.name()}', 'email' : faker.email(), 'password' : 'password' }
      create_user =  file_cloud_api.create_user(params=create_user_params)

      assert create_user.status_code == 400, f'validate create user profile with commonly used password : password123'
      assert create_user.json()['command'][0]['message'] == 'This password is commonly used on internet. Please choose another one.'
   
   @pytest.mark.user
   def test_create_user_password_minimum_character(self, load_env, get_cookies):
      """ 
         verify profile can't be created with minimum password length 
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
     
      create_user_params = { 'profile' : f'{faker.name()}', 'email' : faker.email(), 'password' : 'paris' }
      create_user =  file_cloud_api.create_user(params=create_user_params)

      assert create_user.status_code == 400, f'validate user can create profile with less than 8 characters'
      assert create_user.json()['command'][0]['message'] == 'Password must be minimum of 8 characters.'

   @pytest.mark.user
   def test_create_user_without_profile_name(self, load_env, get_cookies):
      """ 
          verify profile can't be created with email and password
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies)
     
      create_user_params = { 'email' : faker.email(), 'password' : faker.password() }
      create_user =  file_cloud_api.create_user(params=create_user_params)

      assert create_user.status_code == 422, f'validate user can create profile with only email and password'
      assert create_user.json()['command'][0]['message'] == 'bad request'

   @pytest.mark.user
   @pytest.mark.parametrize("email", json_email_exist_data())
   def test_search_profile_name_and_email(self, load_env, get_cookies, email):  
       """  
         verify search the profile with name or email 
       """
       base_url = load_env.get_base_url()
       file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies) 
       search_profile_params = { 'filter' : email, 'context' : 'usergroup' }
       search_profile = file_cloud_api.search_user(params=search_profile_params)#r

       assert search_profile.status_code == 200, f'search result for email: {email}'
       assert search_profile.json()['profile'][0]['emailid'] == email

       search_profile_params = { 'filter' : email.split("@")[0], 'context' : 'usergroup' }
       search_profile = file_cloud_api.search_user(params=search_profile_params)#r

       assert search_profile.status_code == 200, f'search result for email: {email.split("@")[0]}'
       assert search_profile.json()['profile'][0]['username'] == email.split("@")[0]

   @pytest.mark.group
   @pytest.mark.parametrize("group, users", json_user_group_data())
   def test_add_existing_group(self, load_env, get_cookies, group, users): 
      """ 
         verify new group can't be created with existing group name
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies) 
      group_email =  group.replace(' ','_')+'@email.com'
          #if group not exists, create a group
      add_params = { 'groupname' : f'{group}', 'groupemail' : group_email }
      add_group = file_cloud_api.add_group(params=add_params)
      assert add_group.status_code == 400, f'Add an existing group {group}'
      assert add_group.json()['command'][0]['message'] == 'Cannot add user group'

   @pytest.mark.group
   def test_create_group_without_email(self, load_env, get_cookies):
      """  
         verify that the group can be created without email
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies) 
      add_params = { 'groupname' : faker.city() }
      add_group = file_cloud_api.add_group(params=add_params)#requests.post(f'{base_url}/core/addgroup', params= add_params, cookies= get_cookies, headers=headers)

      assert add_group.status_code == 200, f'create a group without email address'
      assert add_group.json()['command'][0]['result'] == 1, 'Group without email address is not successfully created'

   @pytest.mark.group
   @pytest.mark.parametrize("group, users", json_user_group_data())
   def test_search_group_with_partial_text(self, load_env, get_cookies, group, users): 
      """ 
         verify the group can be searched with partial text
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies) 
      search_params = { 'start' :0, 'limit' : 100, 'filter' : f'{group}' }
      search_group = file_cloud_api.search_group(params=search_params)
      group = group[0:round(len(group)/2)]
      assert search_group.status_code == 200, f'search group with name: {group}'
      for each_group in search_group.json()['group']:
         assert group in each_group['groupname']   
   
   @pytest.mark.group
   @pytest.mark.parametrize("group, users", json_user_group_data())
   def test_search_profile_with_groupid(self, load_env, get_cookies, group, users):   
      """ 
          verify the user list can be retrived with group id
      """
      base_url = load_env.get_base_url()
      file_cloud_api = FileCloudApi(base_url=base_url, cookies=get_cookies) 
      search_params = { 'start' :0, 'limit' : 100, 'filter' : f'{group}' }
      search_group = file_cloud_api.search_group(params=search_params)
     
      assert search_group.status_code == 200, f'Search for the group {group} is failed'
      group_id = search_group.json()['group'][0]['groupid']
      
      search_profile_params = { 'context' : 'usergroup', 'groupid' : group_id, 'start' : 0, 'limit' : 100 }
      search_profile = file_cloud_api.search_user(params=search_profile_params)

      assert search_profile.status_code == 200, f'Result retured for group {group} with id: {group_id}'
      assert len(users) == len(search_profile.json()['profile'])
      users = list(map(lambda x : x.lower(), users))
      for username in search_profile.json()['profile']:
         assert username['username'] in users,'validate returned users are correctly in list'
       