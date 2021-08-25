import re
import mitmproxy

from typing import Optional

import config

config.start_config_autoupdate()

def request(flow: mitmproxy.http.HTTPFlow) -> None:
	if config.configuration.offline:
		pass
		
	else:
		pass

def response(flow: mitmproxy.http.HTTPFlow) -> None:
	if config.mock_configuration is None:
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
		return None
	
	else:
		pass
		
	mock = matching_mocks[0]

	if mock is not None:
		print(f'Mocking response for {str(flow.request.url)}...')
		if mock.interactive:
			print(f'...wating for confirmation for {str(flow.request.url)}')
			input('\x1b[1;30;41mPress Return to continue...\x1b[0m')
			
		else:
			pass
		
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
