from os import listdir, stat
from os.path import isfile, isdir, join, realpath, dirname
import yaml

class MockGlobalConfig:
    def __init__(self, config_timestamp, active_mock_set, global_variables, block_online_calls):
        self.config_timestamp = config_timestamp
        self.active_mock_set = active_mock_set
        self.global_variables = global_variables
        self.block_online_calls = block_online_calls
    
    def check_needs_update(self):
        return self.config_timestamp < stat("mock_config.yaml").st_mtime

class MockSetConfig:
    def __init__(self, path, config_timestamp, variables, service_mocks):
        self.path = path
        self.config_timestamp = config_timestamp
        self.variables = variables
        self.service_mocks = service_mocks

    def check_needs_update(self):
        return self.config_timestamp < stat(self.path + "/config.yaml").st_mtime


def load_global_config():
    mock_config = yaml.load(open("mock_config.yaml", "r"))
    config_timestamp = stat("mock_config.yaml").st_mtime
    if "active_set" in mock_config:
        active_mock_set = mock_config["active_set"]
    else:
        active_mock_set = None
    if "variables" in mock_config:
        global_variables =  mock_config["variables"]
    else:
        global_variables = {}
    if "block_online_calls" in mock_config:
        block_online_calls = mock_config["block_online_calls"]
    else:    
        block_online_calls = False
    return MockGlobalConfig(config_timestamp, active_mock_set, global_variables, block_online_calls)

def load_mock_set(dir_name):
    mock_config_path = dir_name + "/config.yaml"
    mock_config = yaml.load(open(mock_config_path, "r"))
    config_timestamp = stat(mock_config_path).st_mtime
    if "variables" in mock_config:
        variables =  mock_config["variables"]
    else:
        variables = {}
    if "mocks" in mock_config:
        mocks =  mock_config["mocks"]
    else:
        mocks =  {}
    return MockSetConfig(dir_name, config_timestamp, variables, mocks)

def mock_sets_dirs():
    disk_location = dirname(realpath(__file__))
    onlyfolders = [f for f in listdir(disk_location) if isdir(join(disk_location, f))]
    mock_config_folders = [f for f in onlyfolders if f.startswith("mitm_")]
    return mock_config_folders