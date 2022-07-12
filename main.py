import recog_func as rf
import gpio_func as gf

gpio = gf.my_gpio(19,13,6,5,11,9,10,18)

gpio.idle_on()
while True:
	input = gpio.wait_input()

	if input==1:
		rf.known_face_encode(gpio)
	elif input==2:
		rf.face_recog(gpio)
	elif input==3:
		gpio.serv_lock()
