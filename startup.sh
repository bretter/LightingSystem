## Startup script to launch all python services

sudo python3 ~/LightingSystem/VisualAlert/VisualAlertForPi.py &
sudo python3 ~/LightingSystem/TempSensor/ReadTemp.py &
sudo python  ~/LightingSystem/webServer/StartHTTPServer.py &
