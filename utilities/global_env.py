from dotenv import dotenv_values
import os

class GlobalConfig:

    def __load_env_var(self):
        env = os.getenv('ENV','qa')
    #loaded secret
        props = {
            **dotenv_values('env/.env.secret'),  # load sensitive variables
            **dotenv_values(f'env/.env.{env}') # Load environment variables
        }

        return props

    def get_base_url(self):
        return self.__load_env_var().get('BASE_URL')
    
    def get_admin_username(self):
        return self.__load_env_var().get('ADMIN_USERNAME')
    
    def get_admin_password(self):
        return self.__load_env_var().get('ADMIN_PASSWORD')
    
    def get_guest_username(self):
        return self.__load_env_var().get('GUEST_USERNAME')
    
    def get_guest_password(self):
        return self.__load_env_var().get('GUEST_PASSWORD')
    
    def get_default_password(self):
        return self.__load_env_var().get('DEFAULT_PASSWORD')