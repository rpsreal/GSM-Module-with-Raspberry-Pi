#!/usr/bin/env python
'''
Library GSM - Rui Pedro Silva; Portugal; 03/2015
'''
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
import serial, time
from threading import Thread
 
class GSM_MODULE:
	def __init__(self, pino_pwr, pino_rst, pin, number, message): 
			self.pino_pwr = pino_pwr
			self.pino_rst = pino_rst
			self.pin = str(pin)
			self.phone_number = str(number)
			self.text = message
			global last_received
			global end_tread
			last_received=''
			end_tread=1
			
			
	def init(self): # pode ser usada fora da class
			self.power_gsm()
			
			self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=5)
			self.thread_serial=Thread(target=receiving, args=(self.ser,))
			self.thread_serial.start()
			
			error=self.init_gms()
			if error==1:
				self.reset_gsm()
				error=self.init_gms()
				if error==1:
					return 1;		
			return 0;
	
	
	def init_gms(self):
		global last_received
		global end_tread
		self.ser.open()
		end_tread=0
		time.sleep(1)
		self.ser.write('AT\r\n')
		time.sleep(1)
	
		#print '1-', last_received
		if last_received != 'OK\r\n':
			self.ser.close()
			return 1;
					
				
		self.ser.write('AT+CPIN="' + self.pin +'"\r\n')
		time.sleep(2)
				
		#print '2-',last_received
		if last_received != 'OK\r\n':
			self.ser.close()
			return 1;
		self.ser.close()
		
		return 0;
				
        	 
        	    	
	def power_gsm(self): # pode ser usada fora da class (com cuidado!)
			GPIO.setup(self.pino_pwr, GPIO.OUT) # power
			GPIO.output(self.pino_pwr, 1)
			time.sleep(1)
			GPIO.output(self.pino_pwr, 0)
			time.sleep(3)
	
	def reset_gsm(self): # pode ser usada fora da class
			global end_tread
			end_tread=0
			self.thread_serial.join()
			GPIO.setup(self.pino_rst, GPIO.OUT) # reset
			GPIO.output(self.pino_rst, 1)
			time.sleep(1)
			GPIO.output(self.pino_rst, 0)
			time.sleep(3)
			self.thread_serial=Thread(target=receiving, args=(self.ser,))
			self.thread_serial.start()
	
 
	def set_phone_number(self, number): # pode ser usada fora da class
			self.phone_number = str(number)
 
	def set_text(self, message): # pode ser usada fora da class
			self.text = message
 
	def send_sms(self): # pode ser usada fora da class
			global last_received
			global end_tread
			end_tread=1
			try:
				self.thread_serial.start()
			except:
				pass;
			self.ser.open()
			time.sleep(1)
			self.ser.write('AT+CMGF=1\r\n')
			time.sleep(1)
			#print '3-',last_received
			self.ser.write('''AT+CMGS="''' + self.phone_number + '''"\r\n''')
			time.sleep(1)
			for x in self.text:
				self.ser.write(x + "\r\n")
				time.sleep(1)
			self.ser.write('\x1A')
			time.sleep(3)
			#print '4-',last_received
			if last_received != 'OK\r\n':
				end_tread=0
				self.ser.close()
				return 1;
			end_tread=0
			self.ser.close()
			return 0;

def receiving(ser):
		global last_received
		global end_tread

		while end_tread:
			last_received = ser.readline()
