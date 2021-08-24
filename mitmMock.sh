#!/bin/bash -e

function prepare {
	echo "Preparing mitmmock..."
	
	if ! command -v mitmdump &> /dev/null
	then
			echo "mitmproxy not installed, please run setup.sh"
			exit
	fi
	
	echo "[Note that it will change your autoproxy settings]"
	networksetup -setautoproxystate Wi-Fi off
	
	current_dir="file://$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/mitmproxy.pac"
	networksetup -setautoproxyurl Wi-Fi $current_dir
}

function run {
	echo "mitmmock running at localhost:8080"
	mitmdump -q -s ./src/interceptor.py
}

function cleanup {
	echo "Cleanung up after proxy "
	networksetup -setautoproxystate Wi-Fi off
}

trap cleanup EXIT
prepare
run
