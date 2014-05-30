import os, glob, time

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#baseDir = '/sys/bus/w1/devices'
#deviceFolder = glob.glob(baseDir + '28*')[0]
#deviceFile = deviceFolder + '/w1_slave'

deviceFile = os.path.join(os.getcwd() + '/example.txt')

def readTempRaw():
  f = open(deviceFile)
  lines = f.readlines()
  f.close()
  return lines

def readTemp():
  lines = readTempRaw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = readTempRaw()
  position = lines[1].find('t=')
  if position != -1:
    tempString = lines[1][position+2:]
    tempC = float(tempString)/1000.0
    tempF = tempC * 9.0 / 5.0 + 32.0
    return tempC, tempF

def writeToFile(tempC, tempF):
  f = open('TempReadings.txt','w')
  f.write('tempC=' + str(tempC) + ', tempF=' + str(tempF))
  f.close()

while True:
  tempC, tempF = readTemp()
  print(tempC, tempF)
  writeToFile(tempC,tempF)
  time.sleep(1)
