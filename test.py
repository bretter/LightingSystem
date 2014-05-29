redPin = 'red'
yellowPin = 'yellow'
greenPin = 'green'

class Light:
	def __init__(self, pin):
		self.pin = pin
		
	def On(self):
		print(self.pin + ' pin ON')
	
	def Off(self):
		print(self.pin + ' pin OFF')
		
class Tower:
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