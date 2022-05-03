import time
import RPi.GPIO as GPIO

from sense_hat import SenseHat
from gpiozero import AngularServo
servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
GPIO.setmode(GPIO.BCM)

"""The following pins connected to raspberry pi board and components"""
#pin2,6,12 for motors
#pin2,6,11,13 for ultrasonic
#pin2,6,31,37 for IR interrupter
#pin1,2,3,5,6,16,18,22,24,27,28 for Sensehat

#IR data
NC =6
SIG=26 
GPIO.setup(NC, GPIO.OUT)
GPIO.setup(SIG, GPIO.IN)
GPIO.output(NC, False)

#Sensehat data
sense = SenseHat()
G = (0,255,0)
O= (0,0,0)
R = (255,0,0)
logo_ok=[
O,O,O,O,O,O,O,O,
O,G,G,O,O,G,O,G,
G,O,O,G,O,G,G,O,
G,O,O,G,O,G,O,O,
G,O,O,G,O,G,O,O,
G,O,O,G,O,G,G,O,
O,G,G,O,O,G,O,G,
O,O,O,O,O,O,O,O,
]
	
logo_R=[
O,G,G,G,G,G,O,O,
O,G,O,O,O,G,O,O,
O,G,O,O,G,O,O,O,
O,G,G,G,O,O,O,O,
O,G,G,O,O,O,O,O,
O,G,O,G,O,O,O,O,
O,G,O,O,G,O,O,O,
O,G,O,O,O,G,O,O,
]

logo_cross=[
R,O,O,O,O,O,O,R,
O,R,O,O,O,O,R,O,
O,O,R,O,O,R,O,O,
O,O,O,R,R,O,O,O,
O,O,O,R,R,O,O,O,
O,O,R,O,O,R,O,O,
O,R,O,O,O,O,R,O,
R,O,O,O,O,O,O,R,
]

#ultrasonic data
TRIG=27
ECHO=17
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
liquid = True #have liquid

while True:
	
	#initial state of motor
	servo.angle=90
	
	#ultrasonic data analysis
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	while GPIO.input(ECHO)==0:
		pulse_start = time.time()
	while GPIO.input(ECHO)==1:
		pulse_stop= time.time()
	pulse_time = pulse_stop-pulse_start
	distance = pulse_time*17150
	print(round(distance,2))
	liquid = True
	if round(distance,2) >=12.5:
		sense.set_pixels(logo_cross)
		liquid = False
		
		
	#IR data analysis
	if liquid == True:
		sense.set_pixels(logo_R)
		if GPIO.input(SIG)==0:
			print("detected")
			sense.set_pixels(logo_ok)
			servo.angle=-40
			time.sleep(2)
		elif GPIO.input(SIG)==1:
			print("not detected yet")
			time.sleep(1)
	time.sleep(1)
	
	
	
	
