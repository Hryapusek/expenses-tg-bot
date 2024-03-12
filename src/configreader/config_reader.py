from singleton_decorator import singleton
import yaml

@singleton
class ConfigReader:
    def __init__(self, path_to_file) -> None:
        with open(path_to_file, 'r') as config_file:
            self.yaml_config = yaml.safe_load(config_file)

    @property
    def db_host(self):
        return self.yaml_config["database"]["host"]
    
    @property
    def db_name(self):
        return self.yaml_config["database"]["dbname"]
    
    @property
    def db_user(self):
        return self.yaml_config["database"]["user"]
    
    @property
    def db_password(self):
        return self.yaml_config["database"]["password"]

