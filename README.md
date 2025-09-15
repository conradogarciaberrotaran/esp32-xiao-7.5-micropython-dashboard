# ESP32-C3 CircuitPython E-Paper Dashboard

```bash
pip install esptool circup mpremote
```

## 1. Installing CircuitPython on ESP32-C3

### Download Firmware

1. Visit [CircuitPython Downloads](https://circuitpython.org/board/seeed_xiao_esp32c3/) for your specific ESP32-C3 board
2. Download the latest stable firmware (`.bin` file)

### Flash the Firmware

1. **Enter bootloader mode:**
   - Hold the BOOT button on your ESP32-C3 board
   - Connect the USB-C cable to your computer
   - Release the BOOT button

2. **Flash CircuitPython:**
   ```bash
   esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 1000000 write_flash -z 0x0 firmware.bin
   ```

   Replace:
   - `/dev/ttyUSB0` with your actual port (check with `ls /dev/tty*` on Linux/macOS or Device Manager on Windows)
   - `firmware.bin` with the downloaded firmware filename

## 2. Setting Up WiFi for Web Workflow

1. Connect to your ESP32-C3 via mpremote
2. In the CircuitPython REPL, create the settings file:
   ```python
   f = open('settings.toml', 'w')
   f.write('CIRCUITPY_WIFI_SSID = "YourWiFiSSID"\\n')
   f.write('CIRCUITPY_WIFI_PASSWORD = "YourWiFiPassword"\\n')
   f.write('CIRCUITPY_WEB_API_PASSWORD = "YourWebPassword"\\n')
   f.close()
   ```

3. **Hard reset** the board (press RESET button or power cycle)

### Verify WiFi Connection

```python
import wifi
print("MAC address:", tuple(wifi.radio.mac_address))
print("IP address:", wifi.radio.ipv4_address)
```

## 3. Installing Libraries with circup

### Install circup

```bash
pip3 install circup
```

### Install Required Libraries

Based on the `main.py` file, install these libraries:

```bash
ESP32_IP="192.168.0.57"  # Replace with your actual IP
WEB_PASSWORD="YourWebPassword"  # From settings.toml

# Show currently installed libraries
circup --host $ESP32_IP --password $WEB_PASSWORD show

# Install required libraries for this project
circup --host $ESP32_IP --password $WEB_PASSWORD install adafruit_displayio_layout
circup --host $ESP32_IP --password $WEB_PASSWORD install adafruit_display_text
circup --host $ESP32_IP --password $WEB_PASSWORD install adafruit_uc8179
```

## 4. Required Libraries

This project uses the following CircuitPython libraries:

- `adafruit_displayio_layout` - Layout management
- `adafruit_display_text` - Text rendering
- `adafruit_uc8179` (or equivalent EPaper driver)
- Built-in libraries: `busio`, `displayio`, `microcontroller`, `terminalio`, `fourwire`
