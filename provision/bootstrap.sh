#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install curl -y
sudo apt-get install openjdk-7-jre-headless -y
mkdir elasticsearch
cd elasticsearch
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.2.2.deb
sudo dpkg -i elasticsearch-1.2.2.deb

sudo update-rc.d elasticsearch defaults 95 10
sudo /etc/init.d/elasticsearch start


sudo /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head
sudo /usr/share/elasticsearch/bin/plugin -install karmi/elasticsearch-paramedic
sudo /usr/share/elasticsearch/bin/plugin -install lukas-vlcek/bigdesk
