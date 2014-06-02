#!/bin/bash
## Startup script to launch all python services

directory="/home/pi/LightingSystem/"

(cd ${directory}VisualAlert/ ; python3 VisualAlertForPi.py &)
(cd ${directory}TempSensor/ ; python3 ReadTemp.py &)
(cd ${directory}webServer/ ; python StartHTTPServer.py &)
