import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from utilities.global_env import GlobalConfig
from utilities.read_test_data import upload_file_path


config = GlobalConfig()
# Define the URL for the file upload endpoint````
base_url = config.get_base_url()
#'https://filecloud.example.com/upload'
# Define the path to the file to upload

headers = {'Accept' : 'application/json'}
params = {'userid': config.get_guest_username(), 'password': config.get_guest_password()}
# Define the range of concurrent users
concurrent_users_list = [10, 20, 50, 100, 200, 500, 1000]
# Define thresholds for determining system breakdown
error_threshold = 0.1  # 10% error rate
response_time_threshold = 5  # 5 seconds
file_path = 'test_data/file_cloud.docx'
class TestConcurent:

    def upload_file(self, file_path):
        """ 
            login and upload file with cookies
        """
        file_path = 'test_data/file_cloud.docx'
        with open(file_path, 'rb') as file:
            files = {'file': file}
            login_res = requests.post(base_url+'/core/loginguest', params==params, headers=headers)
            if login_res.json()['command'][0]['result'] == 1:
                
                upload_params = {'appname': 'explorer', 'path': f'/{config.get_guest_username()}', 'offset': 0}
                response = requests.post(base_url+'/core/upload', data=upload_params, files=files, cookies=login_res.cookies() )
                return response.status_code, response.elapsed.total_seconds() # result is returned as tuple

    def perform_load_test(self, concurrent_users):
        print(f"Testing with {concurrent_users} concurrent users")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # executor executes this loop in asynchronous way
            futures = [executor.submit(self.upload_file,  file_path) for _ in range(concurrent_users)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        duration = end_time - start_time
        error_count = sum(1 for status, _ in results if status != 200)
        error_rate = error_count / concurrent_users
        avg_response_time = sum(response_time for _, response_time in results) / concurrent_users
        
        print(f"Duration: {duration}s, Error Rate: {error_rate}, Avg Response Time: {avg_response_time}s")
        
        return error_rate, avg_response_time

    def template_concurrent_users(self):
        """
            This is psuedo code and it's not tested fully
        """
        for concurrent_users in concurrent_users_list:
            error_rate, avg_response_time = self.perform_load_test(concurrent_users)
            if error_rate > error_threshold or avg_response_time > response_time_threshold:
                print(f"System breakdown at {concurrent_users} concurrent users")
                break


