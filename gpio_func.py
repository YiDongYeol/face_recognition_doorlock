import RPi.GPIO as GPIO
from time import sleep

class my_gpio:

	def __init__(self,G,B,Y,R,SAV,CMP,LOK,servo):
		self.ledG=G
		self.ledR=R
		self.ledB=B
		self.ledY=Y
		self.btnSAV=SAV
		self.btnCMP=CMP
		self.btnLOK=LOK

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(self.ledG,GPIO.OUT)
		GPIO.setup(self.ledR,GPIO.OUT)
		GPIO.setup(self.ledB,GPIO.OUT)
		GPIO.setup(self.ledY,GPIO.OUT)
		GPIO.setup(self.btnSAV,GPIO.IN)
		GPIO.setup(self.btnCMP,GPIO.IN)
		GPIO.setup(self.btnLOK,GPIO.IN)
		GPIO.setup(servo,GPIO.OUT)

		self.pwm=GPIO.PWM(servo, 50)

		self.pwm.start(3.0)
		sleep(1)

	def clean_up(self):
		self.pwm.stop()
		GPIO.cleanup()

	def serv_unlock(self):
		self.pwm.ChangeDutyCycle(12.4)
		sleep(1)

	def serv_lock(self):
		self.pwm.ChangeDutyCycle(3.1)
		sleep(1)

	#IDLE = GREEN, CAP = BLUE, ENCODING = YELLOW ,FAIL = RED

	def idle_on(self):
		GPIO.output(self.ledG,True)

	def idle_off(self):
		GPIO.output(self.ledG,False)

	def cap_on(self):
		GPIO.output(self.ledB,True)

	def cap_off(self):
		GPIO.output(self.ledB,False)

	def enc_on(self):
		GPIO.output(self.ledY,True)

	def enc_off(self):
		GPIO.output(self.ledY,False)

	def fail(self):
		GPIO.output(self.ledR, True)
		sleep(5)
		GPIO.output(self.ledR, False)

	# SAV = SAVE, CMP = COMPARE, LOK = LOCK
	def wait_input(self):
		while(True):
			if GPIO.input(self.btnSAV)==1:
				return 1
			elif GPIO.input(self.btnCMP)==1:
				return 2
			elif GPIO.input(self.btnLOK)==1:
				return 3
