# Quick setup

## Not valid for current version

**Python 3 required!**

To install:

``` bash
./setup.sh
```

tu run proxy:

``` bash
./mitmMock.sh
```

Tu use proxy with ssl you need add mitmproxy cert to trusted certs on device. To do that go to `mitm.it` in web browser and add certificate.

For iOS simulators you need to use script:

```bash
python iosCertTrustManager.py -a ~/.mitmproxy/mitmproxy-ca-cert.pem
```

script from [cert on iOS simulators] - available locally in repository(https://github.com/ADVTOOLS/ADVTrustStore#how-to-use-advtruststore)

To work you need to provide config in mock_config.yaml

variables - variables that can be used in mocks - matching strings in urls will be mapped to those
active_set - mock set used to change traffic, mock set is folder with 'mitm_' prefix containing config.yaml
block_online_calls - set true to respond with mocks without calling real services

each mock set need to have unique name and contain list of mocked services with its parameters

service_path - service path after host name, you can use defined variables and treat it as regex, you can ommit base address prefix
enabled - used to tell if mocking is active (true / false)
interactive - if true response will be sent only after console interaction (true / false)
status_code - response code
headers - set or change headers (optional) (currently can't clean existing ones from online response)
content_type - type of response body, 'application/json' is default if not provided
mocked_content - response body path to file

Proxy will get only data dedicated to selected hosts. Change host name in mitmproxy.pac to redirect traffic you need.