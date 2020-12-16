#!/usr/bin/env bash

# Provisionning script for Ubuntu 20.04

# Some build dependencies
apt install llvm

# Install Python 3.{7,8,9,10} via Deadsnakes
add-apt-repository ppa:deadsnakes/ppa
apt update

apt install python3.6 python3.7 python3.8 python3.9 python3.10 pypy3
apt install python3.7-dev python3.8-dev python3.9-dev python3.10-dev
apt install python3.7-venv python3.8-venv python3.9-venv python3.10-venv

# Install lua
apt install lua5.3 luajit

# Install JS interpreters
apt install nodejs
apt install duktape
curl -fsSL https://deno.land/x/install/install.sh | sh
cp /root/.deno/bin/deno /usr/local/bin/
