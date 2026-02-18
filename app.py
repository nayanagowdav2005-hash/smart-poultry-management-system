import time
import board
import adafruit_dht
import requests
import RPi.GPIO as GPIO
from gpiozero import Servo, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory

# ================== THINGSPEAK ==================
THINGSPEAK_API_KEY = "6QXNUP3U8YK7PM1F"
THINGSPEAK_URL = "https://api.thingspeak.com/update"
THINGSPEAK_INTERVAL = 5  # ThingSpeak rule (>=15 sec)

# ================== GPIO SETUP ==================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Ultrasonic pins
TRIG = 16
ECHO = 5
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Servo + buzzer (pigpio)
factory = PiGPIOFactory()
servo = Servo(18, pin_factory=factory)
buzzer = Buzzer(23)

# DHT11
dht = adafruit_dht.DHT11(board.D17)

TEMP_THRESHOLD = 24  # °C
last_upload_time = 0

print("===================================")
print(" Poultry Management System Started ")
print(" DHT11 + Ultrasonic + Servo + Buzzer")
print(" ThingSpeak Upload Enabled")
print("===================================")

# ================== ULTRASONIC FUNCTION ==================
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 0.04
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    timeout = time.time() + 0.04
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    pulse_duration = pulse_end - pulse_start
    return round(pulse_duration * 17150, 2)

# ================== MAIN LOOP ==================
try:
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
            distance = get_distance()

            # -------- ULTRASONIC TEST OUTPUT --------
            if distance is not None:
                print(f"[ULTRASONIC TEST] Distance = {distance} cm")
            else:
                print("[ULTRASONIC TEST] No echo detected")

            # -------- DHT OUTPUT --------
            if temperature is not None and humidity is not None:
                print(f"[DHT] Temp = {temperature} °C | Humidity = {humidity} %")
            else:
                print("[DHT] Waiting for valid data...")
                time.sleep(2)
                continue

            # -------- CONTROL LOGIC --------
            if temperature > TEMP_THRESHOLD:
                print("⚠ HIGH TEMP → Vent MOVING + Buzzer ON")
                buzzer.on()

                servo.max()
                time.sleep(0.5)
                servo.min()
                time.sleep(0.5)
            else:
                print("✅ TEMP NORMAL")
                buzzer.off()
                servo.mid()

            # -------- THINGSPEAK UPLOAD --------
            current_time = time.time()
            if current_time - last_upload_time >= THINGSPEAK_INTERVAL:
                payload = {
                    "api_key": THINGSPEAK_API_KEY,
                    "field1": temperature,
                    "field2": humidity,
                    "field3": distance if distance is not None else 0
                }

                r = requests.get(THINGSPEAK_URL, params=payload)
                if r.status_code == 200:
                    print("📤 Data uploaded to ThingSpeak")
                else:
                    print("❌ ThingSpeak upload failed")

                last_upload_time = current_time

            print("-----------------------------------")
            time.sleep(2)

        except RuntimeError as e:
            print("Sensor read error, retrying...")
            time.sleep(2)

except KeyboardInterrupt:
    print("\nSystem stopped by user")

finally:
    buzzer.off()
    servo.detach()
    dht.exit()
    GPIO.cleanup()
