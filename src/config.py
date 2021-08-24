import yaml
import threading

from dataclasses import dataclass
from typing import Optional, Union, Final
from os import stat
from os.path import realpath, dirname

from mock import Mock

CONFIG_FILE_NAME: Final = 'config.yaml'
MOCK_NAME_PREFIX: Final = 'mitm_'
CONFIG_RELOAD_INTERVAL: Final = 10

@dataclass
class Configuration:
	path: str
	timestamp: int
	active_mock: Optional[str]
	offline: bool
	record_session: bool

@dataclass
class MockConfiguration:
	name: str
	path: str
	timestamp: int
	mocks: list[Mock]
	
configuration: Configuration = None
mock_configuration: Optional[MockConfiguration] = None

def start_config_autoupdate():
	config_autoupdate()

def config_autoupdate():
	reload_config_if_needed()
	
	threading.Timer(CONFIG_RELOAD_INTERVAL, config_autoupdate).start()

def reload_config_if_needed() -> None:
	global configuration
	global mock_configuration
	
	if configuration is None:
		configuration = load_configuration()
		
	else:
		configuration = reload_if_needed(configuration)
	
	if configuration is None:
		exit(-1)
		
	elif mock_configuration is not None and configuration.active_mock is None:
		print('\x1b[1;34;40mDisabling active mock...\x1b[0m')
		mock_configuration = None
		
	elif mock_configuration is None or mock_configuration.name != configuration.active_mock:
		mock_configuration = load_mock_configuration(name=configuration.active_mock)
		print(f'\x1b[1;34;40mActive mock: {configuration.active_mock}\x1b[0m')
	
	else:
		mock_configuration = reload_if_needed(mock_configuration)

def load_configuration() -> Configuration:
	print('\x1b[1;34;40mLoading config...\x1b[0m')
	path = f'{dirname(realpath(__file__))}/..'
	config = yaml.safe_load(open(f'{path}/{CONFIG_FILE_NAME}', 'r'))
	timestamp = stat(path).st_mtime
	
	return Configuration(
		path=path,
		timestamp=timestamp,
		active_mock=config.get('active_mock', None),
		offline=config.get('offline', False),
		record_session=config.get('record', False)
	)

def load_mock_configuration(name: Optional[str]) -> Optional[MockConfiguration]:
	print('\x1b[1;34;40mLoading mock...\x1b[0m')
	if name:
		path = f'{dirname(realpath(__file__))}/../{MOCK_NAME_PREFIX}{name}'
		config = yaml.safe_load(open(f'{path}/{CONFIG_FILE_NAME}', 'r'))
		timestamp = stat(path).st_mtime
		
		return MockConfiguration(
			name=name,
			path=path,
			timestamp=timestamp,
			mocks=[
				Mock(
					enabled=mock.get('enabled', True),
					path=mock['path'],
					interactive=mock.get('enabled', False),
					status_code=mock.get('status_code', None),
					headers=mock.get('headers', {}),
					body=mock.get('body', None),
					body_path=mock.get('body_path', None),
				) 
				for mock 
				in config.get('mocks', [])
			]
		)
		
	else:
		return None
	
def needs_update(configuration: Union[Configuration, MockConfiguration]) -> bool:
	return configuration.timestamp < stat(f'{configuration.path}/{CONFIG_FILE_NAME}').st_mtime

def reload_if_needed(configuration: Union[Configuration, MockConfiguration]) -> Union[Configuration, MockConfiguration]:
	if needs_update(configuration):
		if type(configuration) is Configuration:
			print('\x1b[1;34;40mReloading config...\x1b[0m')
			return load_configuration()
			
		elif type(configuration) is MockConfiguration:
			print('\x1b[1;34;40mReloading active mock...\x1b[0m')
			return load_mock_configuration(configuration.name)
			
		else:
			return configuration
			
	else:
		return configuration
