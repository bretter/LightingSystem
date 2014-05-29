import urllib.request, re, time
#import RPi.GPIO as GPIO

page_url = 'http://osi-cc100:9080/stats'
pattern = '(\d*) CALLS WAITING FOR (\d*):(\d*)'	# define RegEx search pattern
searchPattern = re.compile(pattern)				# compile pattern into RegEx object
delayTime = 1
maxDisconnectTime = 30

# define pin numbers for lights
redPin = 'redPin'
yellowPin = 'yellowPin'
greenPin = 'greenPin'

class Light:
	def __init__(self, pin):
		self.pin = pin
		#GPIO.setup(pin, GPIO.OUT)
		#GPIO.setmode(GPIO.BOARD)

	def setState(self, state):
		print(self.pin + ' pin ' + str(state))
		#GPIO.output(self.pin, state)
##### Commented out while not running on rPi#####
	# def On(self):
	# 	print(self.pin + ' pin ON')		# PLACEHOLDER: Replace with GPIO command
	# 	#GPIO.output(self.pin, True)
	#
	# def Off(self):
	# 	print(self.pin + ' pin OFF')	# PLACEHOLDER: Replace with GPIO command
	# 	#GPIO.output(self.pin, False)

class Tower:
	def __init__(self, redLight, yellowLight, greenLight):
		self.redLight    = redLight
		self.yellowLight = yellowLight
		self.greenLight  = greenLight

	def setState(self, state):
		self.redLight.setState(state[0])
		self.yellowLight.setState(state[1])
		self.greenLight.setState(state[2])

def updateDisplay(lightTower, points, connectionFailure):

	# Lis of States
	# array elements map to lights : [red, yellow, green]
	red         = [1, 0, 0]
	redYellow   = [1, 1, 0]
	yellow      = [0, 1, 0]
	yellowGreen = [0, 1, 1]
	green       = [0, 0, 1]

	allOn       = [1, 1, 1]
	allOff      = [0, 0, 0]
	# Aliases
	conLost     = allOn
	greenYellow = yellowGreen
	yellowRed   = redYellow

	if connectionFailure:
		lightTower.setState(conLost)
	elif points == 0:
		lightTower.setState(green)
	elif points >= 0 and points < 4:
		lightTower.setState(yellowGreen)
	elif points >= 4 and points < 7:
		lightTower.setState(yellow)
	elif points >= 7 and points < 9:
		lightTower.setState(redYellow)
	elif points >= 9:
		lightTower.setState(red)

def calcPoints(calls, waitTime):
	callPoints = calls
	timePoints = waitTime // 60
	points = callPoints + timePoints
	return points


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

		points = calcPoints(int(callsWaiting), timeSeconds)
		connectionFailure = connectFailCount*delayTime >= maxDisconnectTime
		updateDisplay(LightTower, points, connectionFailure)

		elapsedTime = time.time() - thisTime		# check time elapsed fetching data
		if elapsedTime > delayTime:					# proceed if fetching took longer than 5 sec
			pass
		else:										# otherwise delay the remainder of 5 sec
			time.sleep(delayTime - elapsedTime)

if __name__ == '__main__':
	MainLoop()
