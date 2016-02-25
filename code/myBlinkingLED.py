#!usr/bin/python
import time
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)


def Blink():
          var  = 1	
          while var == 1 :
	   for i in range(0,3):
		print "blink #" + str(i+1)
                GPIO.output(17, True)
		time.sleep(0.25)
		GPIO.output(17, False)
		time.sleep(0.25)
	   print "pause"
	   time.sleep(4.75)
	   
           for i in range(0,4):
                print "blink #" + str(i+1)
		GPIO.output(17, True)
		time.sleep(0.25)
		GPIO.output(17, False)
                time.sleep(0.25)
           print "pause"                		
           time.sleep(4.75)
Blink()
GPIO.cleanup()
