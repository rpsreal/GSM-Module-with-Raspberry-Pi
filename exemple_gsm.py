#!/usr/bin/env python
'''
Exemple 'How to use the library GSM' - Rui Pedro Silva; Portugal; 03/2015
This exemple will send 2 sms. Connect the power and the reset pin to raspberry pi.
'''
from GSM import *


GSM = GSM_MODULE(17, 18, 1234, 123123123, ['Python library for GSM module.', 'Developed by Rui Pedro Silva', 'Portugal, 03/2015'])
#GSM = GSM_MODULE(PWR_pin, RST_pin, SIM_cart_pin, phone_number, ['message_1','message_2', 'message_3', 'message_...'])

error=GSM.init()
if erro == 0:
	print 'OK'
else:
	print 'NO OK!!!!'
	

error_2=GSM.send_sms()
if erro_2 == 0:
	print 'SEND SMS 1'
else:
	print 'ERROR!!!!'

'''  ---- SEND ANOTHER SMS ----
GSM.set_text(['So cool','END!!!']) # set new text for sms
GSM.set_phone_number(321321321) # set a new phone number
error_3=GSM.send_sms()
if error_3 == 0:
	print 'SEND SMS 2!!!!'
else:
	print 'ERROR!!!!'
'''	

GSM.power_gsm() # turn off the GSM module

print 'END of program' 


