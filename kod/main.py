import network
import time
import sys
import json
import random
from machine import Pin, I2C
from umqtt.simple import MQTTClient
# Importujemy klasę z dostarczonego pliku bmp280.py
from bmp280 import BMP280


WIFI_SSID = 'Marcin Router King'
WIFI_PASS = '11111111'


MQTT_CLIENT_ID = 'esp32_student_' + str(random.randint(1000, 9999))
MQTT_BROKER = 'broker.hivemq.com'
MQTT_TOPIC = b'PK/MZ'


def connect_wifi():
    """Nawiązuje połączenie z siecią WiFi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
   
    if not wlan.isconnected():
        print(f'Łączenie z WiFi: {WIFI_SSID}...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
       
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print(f'Czekam na IP... ({timeout}s)')
            time.sleep(1)
            timeout -= 1
           
        if not wlan.isconnected():
            print('BŁĄD: Nie udało się połączyć z WiFi!')
            sys.exit()
           
    print('Połączono z WiFi!')
    print('Adres IP:', wlan.ifconfig()[0])


def main():
    try:
        # 1. Połączenie z WiFi
        connect_wifi()
       
        # 2. Inicjalizacja magistrali I2C oraz czujnika BMP280
        # Zmień piny 22 i 21, jeśli Twój czujnik jest wpięty gdzie indziej
        i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
       
        print('Inicjalizacja czujnika BMP280...')
        # Domyślny adres I2C w bibliotece to 0x76 (zmień na 0x77 jeśli nie wykrywa)
        sensor = BMP280(i2c, addr=0x76)
        print('Czujnik gotowy!')


        # 3. Połączenie z brokerem HiveMQ
        print('Łączenie z brokerem HiveMQ...')
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        print('Połączono z MQTT!')


        while True:
            # 4. Odczyt realnych danych z fizycznego czujnika przy użyciu biblioteki
            temp_czujnik = sensor.temperature
            cisnienie_czujnik = sensor.pressure  # Ciśnienie zwracane w paskalach (Pa)
           
            # Opcjonalnie: konwersja na hektopaskale (hPa) dla łatwiejszego czytania
            cisnienie_hpa = cisnienie_czujnik / 100.0
           
            # 5. Pakowanie w oczyszczony słownik JSON
            payload_dict = {
                "urzadzenie": "ESP32_Mzet",
                "temp_czujnik_C": round(temp_czujnik, 2),
                "cisnienie_hPa": round(cisnienie_hpa, 2)
            }
           
            # 6. Konwersja na string i wysyłka bajtów przez MQTT
            payload_json = json.dumps(payload_dict)
            msg = payload_json.encode('utf-8')
           
            print(f'Wysyłanie na {MQTT_TOPIC.decode()}: {payload_json}')
            client.publish(MQTT_TOPIC, msg)
           
            # Bez HTTP możemy bezpiecznie wysyłać dane nawet co 2-3 sekundy
            time.sleep(2)
           
    except Exception as e:
        print(f'Wystąpił błąd krytyczny: {e}')
    finally:
        try:
            client.disconnect()
        except:
            pass
        print('Program zakończony.')


if __name__ == '__main__':
    main()
