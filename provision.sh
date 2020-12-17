#!/usr/bin/env bash

# Provisionning script for Ubuntu 20.04

# Some build dependencies
apt install llvm

# Install Python 3.{7,8,9,10} via Deadsnakes
add-apt-repository ppa:deadsnakes/ppa
apt update

apt install -y python3.6 python3.7 python3.8 python3.9 python3.10 pypy3
apt install -y python3.7-dev python3.8-dev python3.9-dev python3.10-dev
apt install -y python3.7-venv python3.8-venv python3.9-venv python3.10-venv

# Install miniconda
curl https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc | gpg --dearmor > conda.gpg
install -o root -g root -m 644 conda.gpg /usr/share/keyrings/conda-archive-keyring.gpg
gpg --keyring /usr/share/keyrings/conda-archive-keyring.gpg --no-default-keyring --fingerprint 34161F5BF5EB1D4BFBBB8F0A8AEB4F8B29D82806
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/conda-archive-keyring.gpg] https://repo.anaconda.com/pkgs/misc/debrepo/conda stable main" >
apt update
apt install conda
ln -sf /opt/conda/bin/conda /usr/local/bin
conda update -n base -c defaults conda

# Install lua
apt install -y lua5.3 luajit

# Install JS interpreters
apt install -y nodejs npm
apt install -y duktape
curl -fsSL https://deno.land/x/install/install.sh | sh
cp /root/.deno/bin/deno /usr/local/bin/

# Install Ruby and variants
apt install -y jruby
npm install -g opal
