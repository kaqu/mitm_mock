import yaml
import threading

from dataclasses import dataclass
from typing import Optional, Union, Final
from os.path import realpath, dirname

from watchdog.observers import Observer

from models import Configuration, MockConfiguration, Mock
from observers import observe_file_modifications

CONFIG_FILE_NAME: Final = 'config.yaml'
MOCK_NAME_PREFIX: Final = 'mitm_'

configuration: Configuration = None
configuration_file_observer: Observer = None
mock_configuration: Optional[MockConfiguration] = None
mock_configuration_file_observer: Optional[Observer] = None

def start_autoupdating_config() -> None:
	global configuration
	global configuration_file_observer
	
	print('Starting configuration autoupdating...')
	
	if configuration_file_observer is not None:
		configuration_file_observer.stop()
		configuration_file_observer.join()
		configuration_file_observer = None
		
	else:
		pass
	
	load_configuration()
	
	if configuration is None:
		print('Failed to load configuration')
		exit(-1) # can't use without base configuration
	
	else:
		configuration_file_observer = observe_file_modifications(path=configuration.path, update=load_configuration)
	
	print('...configuration autoupdating started')
	return None

def load_configuration() -> None:
	global configuration
	global mock_configuration
	global mock_configuration_file_observer
	
	print('Loading configuration...')
	
	path = f'{dirname(realpath(__file__))}/..'
	raw_config = yaml.safe_load(open(f'{path}/{CONFIG_FILE_NAME}', 'r'))
	
	configuration = Configuration(
		path=path,
		active_mock=raw_config.get('active_mock', None),
		offline=raw_config.get('offline', False),
		record_session=bool(raw_config.get('record', False))
	)
	
	if configuration.active_mock:
		load_mock_configuration()
		if mock_configuration is not None:
			print(f'Active mock configuration: {configuration.active_mock}')
			mock_configuration_file_observer = observe_file_modifications(
				path=mock_configuration.path, 
				update=load_mock_configuration
			)
			
		else:
			print('Failed to load mock configuration...')
			
	else:
		if mock_configuration is not None:
			mock_configuration = None
			print('Mock configuration disabled')
		else:
			pass
			
		if mock_configuration_file_observer is not None:
			mock_configuration_file_observer.stop()
			mock_configuration_file_observer.join()
			mock_configuration_file_observer = None
			
		else:
			pass
			
	return None

def load_mock_configuration() -> None:
	global configuration
	global mock_configuration
	
	if configuration.active_mock:
		print('Loading mock configuration...')
		
		path = f'{dirname(realpath(__file__))}/../{MOCK_NAME_PREFIX}{configuration.active_mock}'
		raw_config = yaml.safe_load(open(f'{path}/{CONFIG_FILE_NAME}', 'r'))
		
		mock_configuration = MockConfiguration(
			name=configuration.active_mock,
			path=path,
			mocks=[
				Mock(
					enabled=mock.get('enabled', True),
					path=mock['path'],
					interactive=mock.get('interactive', False),
					status_code=mock.get('status_code', None),
					headers=mock.get('headers', {}),
					body=mock.get('body', None),
					body_path=mock.get('body_path', None),
				) 
				for mock 
				in raw_config.get('mocks', [])
			]
		)
		
	else:
		mock_configuration = None
	
	return None
