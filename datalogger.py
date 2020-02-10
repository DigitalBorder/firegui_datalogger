import RPi.GPIO as GPIO
import time
import requests

pirPin = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT) # Relay
GPIO.setup(pirPin, GPIO.IN) # Pir

GPIO.output(4, GPIO.LOW)

# FireGUI Connector
url = "https://<your-project-name>.firegui.com/rest/v1/create/<your-entity-name>"
api_public_key = "<your-api-token>"
headers = {"Authorization": "Bearer " + api_public_key}

def send_to_api():
	# Change with your entity fields
	payload = {
		'sensor_log_type': '1',
		'sensor_log_value': 'Motion Detected'
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	print(response.text)


def open_gate():
	send_to_api()
	print "Open gate!"
	GPIO.output(4, GPIO.HIGH)
	time.sleep(6)
	print "Close gate!"
	GPIO.output(4, GPIO.LOW)

try:
	while True:
		if GPIO.input(pirPin) == GPIO.LOW:
			print "No motion"
			time.sleep(0.5)
		else:
			print "Motion detected"
			open_gate()

except KeyboardInterrupt:
	GPIO.cleanup()
