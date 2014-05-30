## Startup script to launch all python services

sudo python3 /home/pi/LightingSystem/VisualAlert/VisualAlertForPi.py &
sudo python3 /home/pi/LightingSystem/TempSensor/ReadTemp.py &
sudo python  /home/pi/LightingSystem/webServer/StartHTTPServer.py &
