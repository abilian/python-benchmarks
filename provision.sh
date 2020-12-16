#!/usr/bin/env bash

# For Ubuntu 20.04, you need these packages
apt install llvm

add-apt-repository ppa:deadsnakes/ppa
apt update

apt install python3.6 python3.7 python3.8 python3.9 python3.10 pypy3
apt install python3.7-dev python3.8-dev python3.9-dev python3.10-dev
apt install python3.7-venv python3.8-venv python3.9-venv python3.10-venv
