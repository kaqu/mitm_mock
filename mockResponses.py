import yaml # pip3 install PyYaml
import os
import threading
import json
import config_loader
import re
import datetime
from mitmproxy import http

sem = threading.Semaphore(1)
now = datetime.datetime.now()

mock_global_config = config_loader.load_global_config()
active_mock_set_config = config_loader.load_mock_set(mock_global_config.active_mock_set)
active_mocks = []

def reload_mock_config_if_needed():
    global mock_global_config
    global active_mock_set_config
    global active_mocks
    
    global_config_needs_update = mock_global_config.check_needs_update()
    active_set_config_needs_update = active_mock_set_config.check_needs_update()
    if global_config_needs_update:
        print("\x1b[1;34;40mPlease wait, updating global mocks config...\x1b[0m\n")
        mock_global_config = config_loader.load_global_config()
        active_set_config_needs_update = True
    
    if active_set_config_needs_update:
        print("\x1b[1;34;40mPlease wait, updating active mocks set config...\x1b[0m\n")
        active_mock_set_config = config_loader.load_mock_set(mock_global_config.active_mock_set)
    else:
        return

    print("\x1b[1;34;40mActive mocks set: " + str(mock_global_config.active_mock_set) + "\x1b[0m")
    print("\x1b[1;34;40mOnline calls blocked for mocks: \n" + str(mock_global_config.block_online_calls) + "\x1b[0m")
    print("\x1b[1;34;40mRecording enabled: " + str(mock_global_config.record_session) + "\x1b[0m\n")
update_mocks()
print("\x1b[1;34;40mLoading completed, resuming...\x1b[0m\n")

def update_mocks():
    print("Updating mocks...\n")
    global active_mocks
    
    if mock_global_config.global_variables and active_mock_set_config.variables:
        variables = mock_global_config.global_variables.copy()
        variables.update(active_mock_set_config.variables)
    elif mock_global_config.global_variables:
        variables = mock_global_config.global_variables
    elif active_mock_set_config.variables:
        variables = active_mock_set_config.variables
    else:
        variables = None
    
    print("Active mocks:\n")
    active_mocks = []
    for mock in active_mock_set_config.service_mocks:
        if "enabled" in mock:
            enabled = mock["enabled"]
        else:
            enabled = True
        if "interactive" in mock:
            interactive = mock["interactive"]
        else:
            interactive = False

        if enabled:
            if variables:
                for key in variables.keys():
                    if key in mock["service_path"]:
                        mock["service_path"] = mock["service_path"].replace(key, variables[key])
            print(mock["service_path"] + " - is active: " + str(enabled) + " interactive: " + str(interactive) +"\n")
            regex = ".*" + mock["service_path"]
            mock["service_path"] = re.compile(regex)
            active_mocks.append(mock)


def print_response(url, response):
    if "content-type" in response.headers and "json" in response.headers["content-type"]:
        print("\x1b[1;32;40m#" + url + " \x1b[1;35;40m" + str(response) + "\x1b[0m\ncontent: " + "\n" + json.dumps(json.loads(response.content), sort_keys=True, indent=4, separators=(',', ': ')) + "\n")
    else:
        print("\x1b[1;32;40m#" + url + " \x1b[1;35;40m" + str(response) + "\x1b[0m\ncontent is not json \n")

def request(flow):
    global mock_global_config
    
    with sem:
        reload_mock_config_if_needed()
    
    if mock_global_config.block_online_calls:
        for mock in active_mocks:
            if mock["service_path"].match(str(flow.request.url)):
                print("Intercepted: " + str(flow.request.url))
                flow.response = http.HTTPResponse.make(
                                                       None,  # (optional) status code
                                                       b"",  # (optional) content
                                                       {}  # (optional) headers
                                                       )

def record(flow):
    if mock_global_config.record_session:
        with open("session_recording_" + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + ".txt", "a") as recording_file:
            recording_file.write("### " + str(now) + " ###\n")
            recording_file.write("Request =>\n")
            recording_file.write(str(flow.request.method) + " ")
            recording_file.write(str(flow.request.url) + "\n")
            recording_file.write(str(flow.request.headers) + "\n")
            recording_file.write("Body: ")
            recording_file.write(str(flow.request.content) + "\n")
            recording_file.write("Response =>\n")
            recording_file.write("Status code: " + str(flow.response.status_code) + "\n")
            recording_file.write(str(flow.response.headers) + "\n")
            recording_file.write("Body: ")
            recording_file.write(str(flow.response.content) + "\n")
    else:
        return

def response(flow):
    with sem:
        reload_mock_config_if_needed()
    
    for mock in active_mocks:
        if mock["service_path"].match(str(flow.request.url)):
            if "interactive" in mock and mock["interactive"]:
                print("Wating for confirmation for: " + str(flow.request.url))
                input("\x1b[1;30;41mPress Enter to continue...\x1b[0m")
            with open(active_mock_set_config.path + "/" + mock["mock_content"], "r") as mock_data:
                print("\x1b[0;33;40mMocking : " + str(flow.request.url) + "\x1b[0m\n")
                flow.response.status_code = mock["status_code"]
                flow.response.content = str.encode(mock_data.read())
                if "content_type" in mock:
                    flow.response.headers["Content-Type"] = mock["content_type"]
                else:
                    flow.response.headers["Content-Type"] = "application/json;charset=UTF-8"
                if "headers" in mock:
                    mock_headers = mock["headers"]
                    if mock_headers:
                        for k, v in mock_headers.items():
                            flow.response.headers[k] = v
            break
    print_response(str(flow.request.url), flow.response)
    record(flow)

print("\x1b[1;34;40mActive mocks set: " + str(mock_global_config.active_mock_set) + "\x1b[0m")
print("\x1b[1;34;40mOnline calls blocked for mocks: " + str(mock_global_config.block_online_calls) + "\x1b[0m")
print("\x1b[1;34;40mRecording enabled: " + str(mock_global_config.record_session) + "\x1b[0m\n")
update_mocks()
