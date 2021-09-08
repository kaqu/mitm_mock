# Quick setup

To work with proxy you need to provide config in config.yaml and modify mitmproxy.pac to provide hosts that will be passed through proxy.

**Python 3 required**

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
