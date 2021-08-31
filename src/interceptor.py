import re
import mitmproxy

from typing import Optional

import config

def load(loader: mitmproxy.addonmanager.Loader):
	config.start_autoupdating_config()

def request(flow: mitmproxy.http.HTTPFlow) -> None:
	if config.configuration.offline:
		print(f'Blocking request to {str(flow.request.url)}')
		flow.request = None
		
	else:
		if config.mock_configuration is None:
			print(f'Passing request to {str(flow.request.url)}')
			return None
			
		else:
			pass
		
		matching_mocks = [
			mock 
			for mock 
			in config.mock_configuration.mocks 
			if re.match(mock.path, str(flow.request.url))
			and mock.enabled
		]
		
		if len(matching_mocks) <= 0:
			print(f'Passing request to {str(flow.request.url)}')
			return None
		
		else:
			pass
			
		mock = matching_mocks[0]
	
		if mock is not None:
			if mock.interactive:
				print(f'Wating for send confirmation for {str(flow.request.url)}')
				input('\x1b[1;30;41mPress Return to continue...\x1b[0m')
				
			else:
				pass
		
		print(f'Passing request to {str(flow.request.url)}')

def response(flow: mitmproxy.http.HTTPFlow) -> None:
	if config.mock_configuration is None:
		print(f'Passing response from {str(flow.request.url)}')
		return None
		
	else:
		pass
	
	matching_mocks = [
		mock 
		for mock 
		in config.mock_configuration.mocks 
		if re.match(mock.path, str(flow.request.url))
		and mock.enabled
	]
	
	if len(matching_mocks) <= 0:
		print(f'Passing request to {str(flow.request.url)}')
		return None
	
	else:
		pass
		
	mock = matching_mocks[0]

	if mock is not None:
		print(f'Mocking response for {str(flow.request.url)}...')
		
		if mock.status_code is not None:
			print(f'...replacing status code with {mock.status_code}')
			flow.response.status_code = mock.status_code
			
		else:
			pass
		
		body = mock.body
		body_path = mock.body_path
		if body_path is not None:
			print(f'...replacing body with content of {body_path}')
			with open(f'{config.mock_configuration.path}/{body_path}', 'r') as mock_data:
				flow.response.content = str.encode(mock_data.read())
			
		elif body is not None:
			print(f'...replacing body with {body}')
			flow.response.content = body.encode('utf-8')
			
		else:
			pass
		
		for k, v in mock.headers.items():
			print(f'...replacing header {k} with {v}')
			flow.response.headers[k] = v
			
	else:
		pass

def done():
	config.configuration_file_observer.stop()
	config.mock_configuration_file_observer.stop()
	config.configuration_file_observer.join()
	config.mock_configuration_file_observer.join()