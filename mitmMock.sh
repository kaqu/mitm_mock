#!/bin/bash -e

function prepare {
	echo "Preparing mitmmock..."
	
	if ! command -v mitmdump &> /dev/null
	then
			echo "mitmproxy not installed, please run setup.sh"
			exit
	fi
	
	echo "[Note that it will change your autoproxy settings]"
	
	networksetup -setautoproxyurl Wi-Fi "http://localhost:8888/mitmproxy.pac"
	
	python3 -m http.server 8888 2> /dev/null &
	SERVER_PID=$!
}

function run {
	echo "mitmmock running at localhost:8080"
	mitmdump -q -s ./src/interceptor.py
}

function cleanup {
	echo "Cleaning up after proxy "
	kill $SERVER_PID
	networksetup -setautoproxystate Wi-Fi off
}

trap cleanup EXIT
prepare
run
