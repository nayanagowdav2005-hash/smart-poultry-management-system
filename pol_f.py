import time
import requests
import board
import adafruit_dht
import RPi.GPIO as GPIO

API_KEY = "6QXNUP3U8YK7PM1F"
URL = "https://api.thingspeak.com/update"

dht = adafruit_dht.DHT11(board.D17)

TRIG = 27
ECHO = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        end = time.time()

    return round((end - start) * 17150, 2)

print("Uploading data to ThingSpeak...")

while True:
    try:
        temp = dht.temperature
        hum = dht.humidity
        dist = get_distance()

        if temp is not None and hum is not None:
            payload = {
                "api_key": API_KEY,
                "field1": temp,
                "field2": hum,
                "field3": dist
            }
            requests.get(URL, params=payload)
            print("Uploaded:", temp, hum, dist)

        else:
            print("Waiting for sensor data...")

    except Exception as e:
        print("Sensor error")

    time.sleep(20)  # REQUIRED by ThingSpeak
