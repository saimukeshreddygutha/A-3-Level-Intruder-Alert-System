import keysandids, json, time  #importing all the ids, json to load the content in json format
from boltiot import Email, Bolt, Sms  #impoting bolt class, Email for sending mail and Sms for sending sms
mybolt = Bolt(keysandids.bolt_api_key, keysandids.bolt_device_id)    #for bolt cloud to identify your device
isOn = mybolt.isOnline()    #to check the status of the system
print(isOn)
c = 0   #this constant is used to turn off the buzzer
if isOn[-2] == '1':   #isOn[-2] gives 1 if the system is online and 0 the other case
	print("Turning ON Intruder Alert System")
	mybolt.digitalWrite('0', 'HIGH')   #to turn on the LED
	while True:
		if c >= 2:    #to turn off the buzzer after 20 sec
			print("Turning Alarm OFF")
			mybolt.digitalWrite('1', 'LOW')
			c = 0
		elif c == 1:
			c = c + 1
		response = mybolt.analogRead('A0')    #getting response from the bolt A0 pin
		data = json.loads(response)
		try:
			light_intensity = int(data['value'])
			if light_intensity < 1024:    #if the LED is turned off
				c = c + 1
				print('Intruder Detected')
				print('Turning ON ALARM')
				mybolt.digitalWrite('1', 'HIGH')    #turns on the buzzer
				print('Alerting through SMS and Mail')
				sms = Sms(keysandids.twilio_sid, keysandids.twilio_auth_token, keysandids.from_number)     #passing the parameters required to send sms
				response = sms.send_sms("Alert!There's an Intruder in the house")        #sends the msg as Alert! theres an Intruder in the house
				print('Status of SMS at twilio is '+ str(response.status))
				mailer = Email(keysandids.mailgun_api,keysandids.mailgun_domain_name,keysandids.sender_mail, keysandids.rec_mail)      #passing the requiresd info to send mail
				response = mailer.send_email('Alert!',"there's an intruder in the house")     #getting the response
				response_text =json.loads(response.text)    #loading response json format
				print('Status of Mailgun is '+str(response_text))      #printing the status of the mail
		except Exception as e:
			print('An Error Occured')
			print(e)
		time.sleep(10)
else:
	print('The Intruder Alert system is OFFLINE')
