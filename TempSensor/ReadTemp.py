import os
import glob
import time
import sys

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

time.sleep(10)

baseDir = '/sys/bus/w1/devices/'
deviceFolders = glob.glob(baseDir + '28-*')
deviceFiles = []
for folder in deviceFolders:
	deviceFiles.append(folder + '/w1_slave')

try:
  DEBUG = sys.argv[1] == '-d'
except IndexError:
  DEBUG = False

def readTempRaw(device):
  f = open(device)
  lines = f.readlines()
  f.close()
  return lines

def readTemp(device):
  lines = readTempRaw(device)
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = readTempRaw(device)
  position = lines[1].find('t=')
  if position != -1:
    tempString = lines[1][position+2:]
    tempC = float(tempString)/1000.0
    tempF = tempC * 9.0 / 5.0 + 32.0
    return tempC, tempF

def writeToFile(tempC, tempF):
	f = open('../webServer/TempReadings.txt','w')
	f.write(time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime()) + 
			' tempC=' + str(tempC) + ', tempF=' + str(tempF) + '\n')
	f.close()
		

if __name__ == '__main__':
	while True:
		for device in deviceFiles:
			tempC, tempF = readTemp(device)
			if DEBUG: print(tempC, tempF)
		writeToFile(tempC,tempF)
		if DEBUG: print()
		time.sleep(2)

