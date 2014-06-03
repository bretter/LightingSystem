#!/bin/bash
## Startup script to launch all python services

directory="/opt/LightingSystem/"

## webserver
(cd ${directory}webServer/ ; python StartHTTPServer.py &)

## visualalert
#(cd ${directory}VisualAlert/ ; python3 VisualAlertForPi.py &)

## tempsensor
#(cd ${directory}TempSensor/ ; python3 ReadTemp.py &)
