import time
import board
import adafruit_dht

dht = adafruit_dht.DHT11(board.D17)

while True:
    try:
        temp = dht.temperature
        hum = dht.humidity
        print("Temp:", temp, "Humidity:", hum)
    except Exception as e:
        print("DHT error:", e)

    time.sleep(5)
