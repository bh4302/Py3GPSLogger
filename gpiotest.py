import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(7, GPIO.OUT)
def printFunction(channel):
	print("Pin37 engaged")
	print("Note how the bouncetime affects the button press")
	GPIO.output(7, GPIO.HIGH)

GPIO.add_event_detect(37, GPIO.FALLING, callback=printFunction, bouncetime=300)

while True:
	GPIO.wait_for_edge(40, GPIO.FALLING)
	print("Button Pin 40 Pressed")
	GPIO.output(7, GPIO.HIGH)
	GPIO.wait_for_edge(40, GPIO.RISING)
	print("Button Pin 40 Released")
	GPIO.output(7, GPIO.LOW)
	 
GPIO.remove_event_detect(37)
GPIO.cleanup()


