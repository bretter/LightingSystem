import urllib.request, re, time, atexit
import LightTower

pageURL = 'http://osi-cc100:9080/stats'
pattern = '(\d*) CALLS WAITING FOR (\d*):(\d*)'	# define RegEx search pattern
searchPattern = re.compile(pattern)				# compile pattern into RegEx object
delayTime = 1
maxDisconnectTime = 30
lightTower = LightTower.Tower()

def updateDisplay(points, connectionFailure):

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

def getData(address):
	try:
		data = str(urllib.request.urlopen(address).read())	# fetch CISCO phone data
		connectFail = 0					# reset error counter
		extracted = searchPattern.search(data)	# extract desired values from data
		[callsWaiting, minutesWaiting, secondsWaiting] = [
			extracted.group(1), extracted.group(2), extracted.group(3)]
		print('{0:2s} calls waiting for {1:s}:{2:2s}'.format(callsWaiting, minutesWaiting, secondsWaiting))
		timeSeconds = int(secondsWaiting) + int(minutesWaiting)*60
		return [callsWaiting, timeSeconds, connectFail]
	except urllib.error.URLError:				# print error if network lost
		print('CANNOT CONNECT TO CISCO PHONE STATUS PAGE')
		connectFail = 1					# step fail counter up by 1
		return [None, None, connectFail]


def MainLoop():
	connectFailCount = 0		# create error counter
	points = 0

	while True:
		thisTime = time.time()						# record time when entering loop
		[newCallsWaiting, newTimeSeconds, connectFail] = getData(pageURL)
		if connectFail:
			connectFailCount += 1
		else:
			callsWaiting = newCallsWaiting
			timeSeconds = newTimeSeconds
			points = calcPoints(int(callsWaiting), timeSeconds)
			connectFailCount = 0

		connectionFailure = connectFailCount*delayTime >= maxDisconnectTime
		updateDisplay(points, connectionFailure)
		elapsedTime = time.time() - thisTime		# check time elapsed fetching data
		if elapsedTime > delayTime:					# proceed if fetching took longer than 5 sec
			pass
		else:										# otherwise delay the remainder of 5 sec
			time.sleep(delayTime - elapsedTime)



def resetLights():
	lightTower.setState([0,0,0])

atexit.register(resetLights)

if __name__ == '__main__':
	MainLoop()
