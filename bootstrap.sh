#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install curl -y
sudo apt-get install openjdk-7-jre-headless -y
mkdir elasticsearch
cd elasticsearch
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.8.deb
sudo dpkg -i elasticsearch-0.90.8.deb
sudo /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head
sudo /usr/share/elasticsearch/bin/plugin -install karmi/elasticsearch-paramedic




