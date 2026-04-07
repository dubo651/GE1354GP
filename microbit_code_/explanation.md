# This md tells what the two micro:bit should do and the wiring method for the system.

Micro:bit 1 
- Octaves: 2, 3, 4
- Right hand data
- Produces combined sound output
- Displays left hand distance on OLED

Micro:bit 2
- Octaves: 5, 6, 7
- Sends distance and octave data to micro:bit 1
- Displays right hand distance on OLED

Wiring:

**Micro:bit 1**
```
Ultrasonic Sensor:
  VCC  → 3V
  GND  → GND
  TRIG → Pin 1
  ECHO → Pin 2

SSD1306 OLED (I2C):
  VCC → 3V
  GND → GND
  SCL → Pin 19 
  SDA → Pin 20 

Speaker/Buzzer:
  + → Pin 0 (or use built-in speaker)
  - → GND
```

**Micro:bit 2:**
```
Ultrasonic Sensor:
  VCC  → 3V
  GND  → GND
  TRIG → Pin 1
  ECHO → Pin 2

SSD1306 OLED (I2C):
  VCC → 3V
  GND → GND
  SCL → Pin 19 
  SDA → Pin 20 
```

---


