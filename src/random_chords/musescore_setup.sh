#!/bin/bash
sudo add-apt-repository ppa:mscore-ubuntu/mscore-stable
sudo apt-get update
sudo apt-get install musescore
chmod 755 -R '/usr/bin/mscore'
