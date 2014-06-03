#!/bin/bash

## Delete prexisting install
rm -rf /opt/LightingSystem
rm /bin/visualalert

## Clone git repo
git clone -b Dev git://github.com/bretter/LightingSystem.git /opt/LightingSystem

## Modify startup script
function prompt () {
  read -r -p "Install $1? [y/n] : " response
  if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
  then
    sed -i "$2s/^#*//" /opt/LightingSystem/visualalert.sh
  fi
}

prompt $"VisualAlert" $"10"
prompt $"TempSensor" $"13"

## Make startup script executable
chmod +x /opt/LightingSystem/visualalert.sh

## Add launch script to /bin
ln -s /opt/LightingSystem/visualalert.sh /bin/visualalert

## Add to appropriate hook to chrontab
#crontab -l | { cat; echo "@reboot visualalert"; } | crontab -
crontab -l > crontab.tmp
echo "@reboot visualalert" >> crontab.tmp
crontab crontab.tmp
