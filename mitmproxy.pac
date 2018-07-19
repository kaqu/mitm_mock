function FindProxyForURL(url, host) {
    PROXY = "PROXY localhost:8080"

    // only matching host will be redirected to proxy
    if (shExpMatch(host,"*.httpbin.org")) {
        return PROXY;
    }
    // Everything else directly!
    return "DIRECT";
}