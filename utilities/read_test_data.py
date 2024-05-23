import json
from faker import Faker

faker = Faker()

def json_user_group_data():
    """ load the test data json file for method parameter"""
    with open(f'test_data/data.json', 'r') as test_data:
        data = json.load(test_data)['user_group']
    conv_params = [(key, value)  for key, value in data.items()]
    return conv_params

def json_email_exist_data():
    """ send the email as tuple"""
    with open(f'test_data/data.json', 'r') as test_data:
        data = json.load(test_data)['exist_email']
    return [(data)]

def upload_file_path():
    """ file path for upload to server"""
    file_name = 'file_cloud.docx'
    return {'file': (open(f'test_data/{file_name}','rb')), 'filename': file_name}


