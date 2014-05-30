import urllib.request
import re
import time


page_url = 'http://osi-cc100:9080/stats'
pattern = '(\d*) CALLS WAITING FOR (\d*):(\d*)'	# define RegEx search pattern
searchPattern = re.compile(pattern)				# compile pattern into RegEx object
delayTime = 1
maxDisconnectTime = 30

# define pin numbers for lights
redPin = 'red'
yellowPin = 'yellow'
greenPin = 'green'

class Light:
	def __init__(self, pin):
		self.pin = pin

	def On(self):
		print(self.pin + ' pin ON')		# PLACEHOLDER: Replace with GPIO command


	def Off(self):
		print(self.pin + ' pin OFF')	# PLACEHOLDER: Replace with GPIO command

class Tower:							# Establish states for light tower
	def __init__(self, redLight, yellowLight, greenLight):
		self.redLight = redLight
		self.yellowLight = yellowLight
		self.greenLight = greenLight

	def Red(self):
		self.redLight.On()
		self.yellowLight.Off()
		self.greenLight.Off()

	def YellowRed(self):
		self.redLight.On()
		self.yellowLight.On()
		self.greenLight.Off()

	def Yellow(self):
		self.redLight.Off()
		self.yellowLight.On()
		self.greenLight.Off()

	def GreenYellow(self):
		self.redLight.Off()
		self.yellowLight.On()
		self.greenLight.On()

	def Green(self):
		self.redLight.Off()
		self.yellowLight.Off()
		self.greenLight.On()

	def AllOff(self):
		self.redLight.Off()
		self.yellowLight.Off()
		self.greenLight.Off()

	def ConnectionLost(self):
		self.redLight.On()
		self.yellowLight.On()
		self.greenLight.On()

def DisplayState(lightTower, calls, waitTime, failCount):
	callPoints = calls
	timePoints = waitTime // 60
	points = callPoints + timePoints
	if failCount*delayTime >= maxDisconnectTime:
		lightTower.ConnectionLost()
	elif points == 0:
		lightTower.Green()
	elif points >= 0 and points < 4:
		lightTower.GreenYellow()
	elif points >= 4 and points < 7:
		lightTower.Yellow()
	elif points >= 7 and points < 9:
		lightTower.YellowRed()
	elif points >= 9:
		lightTower.Red()

def MainLoop():
	Red = Light(redPin)			# instantiate the light and tower objects
	Yellow = Light(yellowPin)
	Green = Light(greenPin)
	LightTower = Tower(Red, Yellow, Green)

	connectFailCount = 0		# create error counter
	while True:
		thisTime = time.time()						# record time when entering loop
		try:
			data = str(urllib.request.urlopen(page_url).read())	# fetch CISCO phone data
			connectFailCount = 0					# reset error counter
			extracted = searchPattern.search(data)	# extract desired values from data
			[callsWaiting, minutesWaiting, secondsWaiting] = [
				extracted.group(1), extracted.group(2), extracted.group(3)]
			print('{0:2s} calls waiting for {1:s}:{2:2s}'.format(callsWaiting, minutesWaiting, secondsWaiting))
			timeSeconds = int(secondsWaiting) + int(minutesWaiting)*60

		except urllib.error.URLError:				# print error if network lost
			print('CANNOT CONNECT TO CISCO PHONE STATUS PAGE')
			connectFailCount += 1					# step fail counter up by 1

		DisplayState(LightTower, int(callsWaiting), timeSeconds, connectFailCount)

		elapsedTime = time.time() - thisTime		# check time elapsed fetching data
		if elapsedTime > delayTime:					# proceed if fetching took longer than 5 sec
			pass
		else:										# otherwise delay the remainder of 5 sec
			time.sleep(delayTime - elapsedTime)

if __name__ == '__main__':
	MainLoop()
