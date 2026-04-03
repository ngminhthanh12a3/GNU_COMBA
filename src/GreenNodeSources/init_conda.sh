#!/bin/bash

/network-volume/miniconda3/bin/conda init

echo "envs_dirs:
  - /network-volume/conda_envs
pkgs_dirs:
  - /network-volume/conda_pkgs" >> ~/.condarc

echo "Dir::Cache{Archives /network-volume/apt_cache}
Dir::Cache::Archives /network-volume/apt_cache;" >> /etc/apt/apt.conf

cp cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
dpkg -i cuda-repo-ubuntu2204-12-4-local_12.4.0-550.54.14-1_amd64.deb
cp /var/cuda-repo-ubuntu2204-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
apt-get update
apt install libcublas-12-4=12.4.5.8-1 -y --allow-change-held-packages
apt-get -y install cuda-toolkit-12-4 --allow-change-held-packages

apt-get install cmake libcurl4-openssl-dev git curl -y

export PATH=${PATH}:/usr/local/cuda-12.4/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda-12.4/lib64

echo "export PATH=\${PATH}:/usr/local/cuda-12.4/bin
export LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:/usr/local/cuda-12.4/lib64" >> ~/.bashrc
