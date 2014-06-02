#!/bin/bash

## Delete prexisting install

rm -rf /opt/LightingSystem
rm /bin/visualalert

## Clone git repo

git clone -b Dev https://github.com/bretter/LightingSystem.git /opt/LightingSystem

## Make startup script executable

chmod +x /opt/LightingSystem/visualalert.sh

## Copy over launch script

ln -s /opt/LightingSystem/visualalert.sh /bin/visualalert

## Add to chrontab startup

#crontab -l | { cat; echo "@reboot visualalert"; } | crontab -
crontab -l > crontab.tmp
echo "@reboot visualalert" >> crontab.tmp
crontab crontab.tmp
