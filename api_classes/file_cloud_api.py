import requests

class FileCloudApi:

   
    
    def __init__(self, base_url, cookies={}):
        self.BASE_URL = base_url
        self.COOKIES = cookies
        self.set_headers()
    
    def login_guest(self, params):
        return requests.get(f'{self.BASE_URL}/core/loginguest', params=params,  headers=self.headers)
        
   

    def set_headers(self, headers={'Accept': 'application/json'}):
        self.headers = headers
    
    def search_group(self, params):
        return requests.get(f'{self.BASE_URL}/core/searchgroups', params= params, cookies= self.COOKIES, headers=self.headers)
    
    def add_group(self, params):
        return  requests.post(f'{self.BASE_URL}/core/addgroup', params= params, cookies= self.COOKIES, headers=self.headers)
    
    def search_user(self, params):
        return  requests.post(f'{self.BASE_URL}/core/searchprofiles', params= params, cookies= self.COOKIES, headers=self.headers)
    
    def create_user(self, params):
        return  requests.post(f'{self.BASE_URL}/core/createprofile', params= params, cookies= self.COOKIES, headers=self.headers)
    
    def add_user_to_group(self, params):
        return  requests.post(f'{self.BASE_URL}/core/addgroupmember', params= params, cookies= self.COOKIES, headers=self.headers)
    
    def get_group_members(self, params):
        return  requests.post(f'{self.BASE_URL}/core/groups', params= params, cookies= self.COOKIES, headers=self.headers)
    

    def get_upload_file(self, params, file):
        return  requests.post(f'{self.BASE_URL}/core/upload', params= params, files=file, cookies= self.COOKIES, headers=self.headers)
    

    def get_file_exists(self, params):
        return requests.post(f'{self.BASE_URL}/core/fileexists', params= params, cookies= self.COOKIES, headers=self.headers)
   
    def get_file_versions(self, params):
        return requests.post(f'{self.BASE_URL}/core/getversions', params= params, cookies= self.COOKIES, headers=self.headers)
   

    def get_make_version_live(self, params):
        return requests.post(f'{self.BASE_URL}/core/makeversionlive', params= params, cookies= self.COOKIES, headers=self.headers)
   
    def get_copy_file(self, params):
        return requests.post(f'{self.BASE_URL}/core/copyfile', params= params, cookies= self.COOKIES, headers=self.headers)
   
    def get_delete_file_version(self, params):
        return requests.post(f'{self.BASE_URL}/core/deleteversion', params= params, cookies= self.COOKIES, headers=self.headers)
    
    def get_delete_file(self, params):
        return requests.post(f'{self.BASE_URL}/core/deletefile', params= params, cookies= self.COOKIES, headers=self.headers)
   
   