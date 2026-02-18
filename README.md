# 🐔 Smart Poultry Management System Using IoT

An IoT-based smart poultry monitoring system built using Raspberry Pi and Python.  
This project monitors environmental conditions in real-time and provides automated alerts and control mechanisms to improve poultry farm efficiency.

---

## 📌 Project Overview

Traditional poultry farms rely on manual monitoring of temperature and environmental conditions.  
This project automates the monitoring process using IoT technology.

The system continuously tracks:

- Temperature
- Humidity
- Movement / Distance (Ultrasonic Sensor)

When abnormal conditions are detected, the system automatically triggers alerts and control mechanisms.

---

## 🛠 Technologies & Components Used

### Hardware:
- Raspberry Pi
- DHT11 / DHT22 Sensor (Temperature & Humidity)
- Ultrasonic Sensor
- Servo Motor
- Buzzer

### Software:
- Python
- Flask (Web Framework)
- HTML / CSS
- RPi.GPIO
- Adafruit DHT Library

---

## 🚀 Features

- Real-time environmental monitoring
- Automatic alert system using buzzer
- Servo motor-based automated control
- Cloud-based data transmission
- Web dashboard for remote monitoring
- Threshold-based decision making

---

## 🏗 System Architecture

Sensors collect data →  
Raspberry Pi processes data →  
Data sent to cloud →  
Web dashboard displays live readings →  
Alerts triggered if threshold exceeded.

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
