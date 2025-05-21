# mitmMock

A mitmproxy-based mock server.

**Python 3.8+ required**

## Setup

This project uses `uv` for dependency management and as a build system.

1.  **Install `uv`**:
    Follow the instructions on the official `uv` website: https://github.com/astral-sh/uv#installation

2.  **Create a virtual environment**:
    Navigate to the project root directory and run:
    ```bash
    uv venv
    ```
    This will create a virtual environment named `.venv` in the project directory.

3.  **Activate the virtual environment**:
    On macOS and Linux:
    ```bash
    source .venv/bin/activate
    ```
    On Windows:
    ```bash
    .venv\Scripts\activate
    ```

4.  **Install dependencies**:
    With the virtual environment activated, install the project dependencies:
    ```bash
    uv pip install -e .
    ```

## Running the Proxy

Once the setup is complete, you can run the proxy using:

```bash
mitmdump -s src/mitmmock/interceptor.py
```

By default, `mitmdump` will listen on `localhost:8080`.

## Configuring Your System/Device to Use the Proxy

To route traffic through mitmMock, you need to configure your system or device's HTTP/HTTPS proxy settings.

1.  **Proxy Address**: `127.0.0.1` (or `localhost`)
2.  **Proxy Port**: `8080` (or the port mitmdump is running on, if you've changed it)

**Important Notes:**

*   The exact steps for configuring proxy settings vary depending on your operating system (Windows, macOS, Linux) or device (iOS, Android). Please refer to your system's or device's documentation for specific instructions.
*   You are no longer required to use the `mitmproxy.pac` file. Direct proxy configuration is recommended.

## SSL/TLS Interception

To intercept and inspect HTTPS traffic, you need to install the mitmproxy CA certificate on the device or system running the browser/application.

1.  **Start `mitmdump`** as described above.
2.  With the proxy configured in your browser, go to `http://mitm.it`.
3.  Follow the instructions on that page to install the certificate for your operating system/device.

For **iOS simulators**, after installing the certificate via `mitm.it` in Safari, you might also need to enable full trust for it:
Go to Settings > General > About > Certificate Trust Settings, and enable full trust for the "mitmproxy" root certificate.
The older method using `iosCertTrustManager.py` (mentioned below) might still be relevant for specific scenarios or older iOS versions, but try the `mitm.it` method first.

### Legacy iOS Simulator Certificate Installation (if mitm.it is insufficient)

The script `iOS simulator certs/iosCertTrustManager.py` can be used to install the mitmproxy CA certificate into iOS simulators.

First, ensure mitmproxy has generated its CA certificate. This usually happens the first time you run `mitmdump`. The certificate will be located at `~/.mitmproxy/mitmproxy-ca-cert.pem`.

Then, run the script:

```bash
python "iOS simulator certs/iosCertTrustManager.py" -a ~/.mitmproxy/mitmproxy-ca-cert.pem
```
For more details, refer to the README in the `iOS simulator certs/` directory or [ADVTrustStore](https://github.com/ADVTOOLS/ADVTrustStore#how-to-use-advtruststore).

## Configuration

Configure mocks in `config.yaml`. The `mitm_sample` directory contains an example configuration (`mitm_sample/config.yaml`) and a sample JSON response body (`mitm_sample/test.json`).
```
