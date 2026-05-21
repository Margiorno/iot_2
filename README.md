## 1. Pobranie interpretera MicroPython

Pobierz najnowszy firmware dla ESP32:

https://micropython.org/download/ESP32_GENERIC/

Po pobraniu zmień nazwę pliku na:

```bash
ESP32_GENERIC.bin
```

---

## 2. Instalacja narzędzi

W katalogu z pobranym firmware uruchom:

```bash
pip install esptool mpremote
```

---

## 3. Wyczyszczenie pamięci ESP32

```bash
python -m esptool --port COM4 erase_flash
```

---

## 4. Wgranie firmware MicroPython

```bash
python -m esptool --chip esp32 --port COM4 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC.bin
```

---

## 5. Wgranie kodu `main.py`

```bash
python -m mpremote cp main.py :main.py
```

---

## 6. Sprawdzenie plików na płytce

```bash
python -m mpremote ls
```

---

## 7. Instalacja biblioteki MQTT

```bash
python -m mpremote mip install umqtt.simple
```

---

## 8. Instalacja biblioteki BMP280

Źródło biblioteki:

https://github.com/dafvid/micropython-bmp280/blob/master/bmp280.py

Skopiowanie biblioteki na płytkę:

```bash
python -m mpremote cp bmp280.py :bmp280.py
```

---

## 9. Wgranie kodu z resetem i logami

```bash
python -m mpremote cp main.py :main.py + reset repl
```



# InfluxDB + Node-RED — instalacja i konfiguracja

## 1. Instalacja Docker + Docker Compose

```bash
sudo dnf install moby-engine docker-compose -y
```

---

## 2. Uruchomienie i autostart Dockera

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 3. Uruchomienie InfluxDB 2

```bash
sudo docker run \
 --name influxdb2 \
 --publish 8086:8086 \
 --mount type=volume,source=influxdb2-data,target=/var/lib/influxdb2 \
 --mount type=volume,source=influxdb2-config,target=/etc/influxdb2 \
 --env DOCKER_INFLUXDB_INIT_MODE=setup \
 --env DOCKER_INFLUXDB_INIT_USERNAME=user \
 --env DOCKER_INFLUXDB_INIT_PASSWORD=password \
 --env DOCKER_INFLUXDB_INIT_ORG=pk \
 --env DOCKER_INFLUXDB_INIT_BUCKET=pk \
 influxdb:2
```

Po uruchomieniu panel będzie dostępny pod adresem:

```text
http://localhost:8086
```

---

# NODE-RED

## 4. Instalacja Node.js i npm

```bash
sudo dnf install -y nodejs npm
```

---

## 5. Sprawdzenie wersji

```bash
node -v
npm -v
```

---

## 6. Instalacja Node-RED

```bash
sudo npm install -g --unsafe-perm node-red
```

---

## 7. Uruchomienie Node-RED

```bash
node-red
```

Panel będzie dostępny pod adresem:

```text
http://localhost:1880
```

Dashboard będzie dostępny pod:

```text
http://localhost:1880/ui
```

Biblioteki do dodania:
```text
node-red-contrib-influxdb
```
```text
node-red-dashboard
```
