import network
import time
import sys
import json
import random
from umqtt.simple import MQTTClient

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
        
        # 2. Połączenie z brokerem HiveMQ
        print('Łączenie z brokerem HiveMQ...')
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        print('Połączono z MQTT!')

        # Wartości startowe do symulacji płynnych zmian (błądzenie losowe)
        sim_temp = 22.0
        sim_press = 1013.25

        while True:
            # 3. Generowanie danych testowych (zaślepka zamiast fizycznego BMP280)
            # Dodajemy mały, losowy szum, żeby wykres w Node-RED ładnie "żył"
            sim_temp += random.choice([-0.1, -0.05, 0.0, 0.05, 0.1])
            sim_press += random.choice([-0.3, -0.1, 0.0, 0.1, 0.3])
            
            # Ograniczamy wartości do realistycznych zakresów
            sim_temp = max(18.0, min(sim_temp, 26.0))
            sim_press = max(990.0, min(sim_press, 1035.0))
            
            # 4. Pakowanie w identyczny słownik JSON jak na kolokwium
            payload_dict = {
                "temp_czujnik_C": round(sim_temp, 2),
                "cisnienie_hPa": round(sim_press, 2)
            }
            
            # 5. Konwersja na string i wysyłka bajtów przez MQTT
            payload_json = json.dumps(payload_dict)
            msg = payload_json.encode('utf-8')
            
            print(f'Wysyłanie na {MQTT_TOPIC.decode()}: {payload_json}')
            client.publish(MQTT_TOPIC, msg)
            
            # Częstotliwość wysyłania pomiarów
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
