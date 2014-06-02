#!/bin/bash

## Delete prexisting install

rm /opt/LightingSystem

## Clone git repo

cd /opt && git clone https://github.com/bretter/LightingSystem.git

## Make startup script executable

cd /opt/LightingSystem && chmod +x visualalert.sh

## Copy over launch script

cd /bin && ln -s /opt/LightingSystem/visualalert.sh
