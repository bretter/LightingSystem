import urllib.request

while True:

	print(str(urllib.request.urlopen(
		'http://jamesrpi.local:8000/currentLightState.txt').read()))
