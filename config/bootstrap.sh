#!/usr/bin/env bash

# add swap if DNE
# swap is necessary for using Docker
if [ $(sudo swapon -s | wc -l) -eq 1 ]
then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
fi

if [ ! -d "/opt/conda" ]; then
    wget --quiet --no-clobber http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
    bash Miniconda2-latest-Linux-x86_64.sh -b -p "/opt/conda"
    echo 'export PATH="/opt/conda/bin:$PATH"' >> /home/vagrant/.bashrc
    chown -R vagrant:vagrant /opt/conda
fi

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

apt-get update
apt-get --yes install mongodb-org
service mongod start


export PATH="/opt/conda/bin:$PATH"
conda update --yes conda
pip install -r /vagrant/requirements.txt

exit 0
