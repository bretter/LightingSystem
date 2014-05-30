import RPi.GPIO as GPIO

# define pin numbers for lights
redPin = 11
yellowPin = 13
greenPin = 15

class Light:
  def __init__(self, pin):
    self.pin = pin
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

  def setState(self, state):
    print(str(self.pin) + ' pin ' + str(state))
    GPIO.output(self.pin, state)

class Tower:
  def __init__(self):
    self.redLight    = Light(redPin)
    self.yellowLight = Light(yellowPin)
    self.greenLight  = Light(greenPin)

  def setState(self, state):
    self.redLight.setState(state[0])
    self.yellowLight.setState(state[1])
    self.greenLight.setState(state[2])

def main():
  import time
  tower = Tower()
  states = [[1, 0, 0]\
           ,[1, 1, 0]\
           ,[0, 1, 0]\
           ,[0, 1, 1]\
           ,[0, 0, 1]\
           ,[1, 1, 1]\
           ,[0, 0, 0]\
           ]

  while true:
    for state in states:
      tower.setState(state)
      time.sleep(1)

if __name__ == '__main__':
  main()
