#!/bin/bash 
echo "Setting up proxy at localhost:8080"
current_dir="file://$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/mitmproxy.pac"
echo "[Note that it will change your autoproxy settings]"
networksetup -setautoproxyurl Wi-Fi $current_dir
mitmdump -q -s mockResponses.py
echo "Cleanung up after proxy "
networksetup -setautoproxystate Wi-Fi off
