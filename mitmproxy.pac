function FindProxyForURL(url, host) {
  PROXY = "PROXY localhost:8080"
  
  if (shExpMatch(host, "httpbin.org")) {
    return PROXY;
  }

  if (shExpMatch(host, "mitm.it")) {
    return PROXY;
  }
  
  return "DIRECT";
}