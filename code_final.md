# This is the final version of code, implemented in 00:20, 19 April 2026

---

The whole project was strictly ended right after the implementation success.

## 1. keyleft project (.hex)

1. main.py
```python
from microbit import *
import music
import radio
import utime
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

#Configuration
'''This is the left hand code. The difference between the function of the left hand
and the right hand is the range of the octave and the radio group''' 

trigger= pin8
echo = pin9

NOTE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']# Do Re Mi Fa Sol La Ti

# Note frequencies for octaves from 2 to 4
# Format: NOTE_FREQUENCIES[octave][note_index]
NOTE_FREQUENCIES = {
    2: [65, 73, 82, 87, 98, 110, 123],      # C2-B2
    3: [131, 147, 165, 175, 196, 220, 247], # C3-B3
    4: [262, 294, 330, 349, 392, 440, 494], # C4-B4
}

# Some default variables
left_octave = 3  # Default octave for left hand
last_left_note = -1 #Default note for left hand

#Ultrasonic sensor functions
def get_distance():
    """Read distance from ultrasonic sensor in cm"""
    # 1. Prepare trigger pin
    trigger.write_digital(0)
    utime.sleep_us(2)

    # 2. Send a 10 microsecond pulse
    trigger.write_digital(1)
    utime.sleep_us(10)
    trigger.write_digital(0)

    # 3. Measure pulse duration
    pulse_start = utime.ticks_us()
    pulse_end = pulse_start
    timeout = pulse_start + 30000  # 30 ms timeout

    # Wait for echo to go HIGH
    while echo.read_digital() == 0:
        pulse_start = utime.ticks_us()
        if pulse_start > timeout: return False

    # Wait for echo to go LOW
    while echo.read_digital() == 1:
        pulse_end = utime.ticks_us()
        if pulse_end > timeout: return False

    duration = utime.ticks_diff(pulse_end, pulse_start)

    # Convert to centimeters (speed of sound ≈ 343 m/s)
    distance_cm = (duration * 34300) // (2 * 1000000)
    return distance_cm

# Functions to connect the distance with the note
def distance_to_note_index(dist):
    """Convert distance to note index (0-6 for C-B, -1 for no note)"""
    if dist <=2 :
        return -1  # No note
    elif dist <= 5:
        return 0  # C
    elif dist <= 8:
        return 1  # D
    elif dist <= 11:
        return 2  # E
    elif dist <= 14:
        return 3  # F
    elif dist <= 17:
        return 4  # G
    elif dist <= 20:
        return 5  # A
    elif dist <= 23:
        return 6  # B
    else:
        return -1  # Too far

# The function to make sounds
def play_note(note_index, octave, duration=200):
    """Play a note at given octave"""
    if note_index >= 0 and note_index < 7:
        freq = NOTE_FREQUENCIES[octave][note_index]
        music.pitch(freq, duration)

# OLED display functions
def update_display(distance, note_index, octave):
    """Update OLED with current state"""
    clear_oled()

    # Line 1: Distance
    add_text(0, 0, str(distance)+"cm")

    # Line 2: Current note
    if note_index >= 0:
        note_name = NOTE_NAMES[note_index]
        add_text(0, 1, "Note"+str(note_name)+str(octave))
    else:
        add_text(0, 1, "Note: ---")

    # Line 3: Octave info
    add_text(0, 2, "Octave"+ str(octave))
    
# Function to change the octave
def handle_buttons(left_octave):
    # 2-3-4-2-3-4-2-3-4...... Infinite sequence by pressing the button A
    if button_a.was_pressed():
        if left_octave < 4:
            return left_octave + 1
        else:
            return 2
    #4-3-2-4-3-2-4-3-2......  Infinite sequence by pressing the button B
    elif button_b.was_pressed():
        if left_octave > 2:
            return left_octave - 1
        else:
            return 4
    #The octave remains still
    else:
        return left_octave

# ============ MAIN PROGRAM ============
radio.on()
radio.config(channel=41, power=7, group=1)
initialize()
clear_oled()
add_text(0, 0, "Left Hand")
add_text(0, 1, "Initializing...")
sleep(1000)

display.show(Image.MUSIC_QUAVER)
clear_oled()
add_text(0, 0, "Ready!")
sleep(1000)
clear_oled()
while True:
    # Read left hand distance
    distance = int(get_distance())
    
    # Handle button presses
    left_octave = handle_buttons(left_octave)

    # Convert distances to note indices
    note_index = distance_to_note_index(distance)

    # Send the information of the notes to the microbit controlling the LEDs
    radio.send(str(note_index))
    
    # Play music if notes changed
    if note_index != last_left_note:
        play_note(note_index, left_octave, duration=200)

    # Update display
    if distance >= 0:
        update_display(distance, note_index, left_octave)

    # More visual elements
    if note_index >= 0:
        display.show(Image.MUSIC_QUAVER)
    else:
        display.show(Image.MUSIC_CROTCHET)

    sleep(100)  # 10Hz update rate

```

2. ssd1306.py
```python
# I2C LCD library for the micro:bit
# Thanks to adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Thanks to lopyi2c.py
# Author: fizban99
# v0.1 beta
# Only supports display type I2C128x64

from microbit import i2c

# LCD Control constants
ADDR = 0x3C
screen = bytearray(513)  # send byte plus pixels
screen[0] = 0x40
zoom = 1


def command(c):
    i2c.write(ADDR, b'\x00' + bytearray(c))


def initialize():
    cmd = [
        [0xAE],                     # SSD1306_DISPLAYOFF
        [0xA4],                     # SSD1306_DISPLAYALLON_RESUME
        [0xD5, 0xF0],               # SSD1306_SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],               # SSD1306_SETMULTIPLEX
        [0xD3, 0x00],               # SSD1306_SETDISPLAYOFFSET
        [0 | 0x0],                  # line #SSD1306_SETSTARTLINE
        [0x8D, 0x14],               # SSD1306_CHARGEPUMP
        # 0x20 0x00 horizontal addressing
        [0x20, 0x00],               # SSD1306_MEMORYMODE
        [0x21, 0, 127],             # SSD1306_COLUMNADDR
        [0x22, 0, 63],              # SSD1306_PAGEADDR
        [0xa0 | 0x1],               # SSD1306_SEGREMAP
        [0xc8],                     # SSD1306_COMSCANDEC
        [0xDA, 0x12],               # SSD1306_SETCOMPINS
        [0x81, 0xCF],               # SSD1306_SETCONTRAST
        [0xd9, 0xF1],               # SSD1306_SETPRECHARGE
        [0xDB, 0x40],               # SSD1306_SETVCOMDETECT
        [0xA6],                     # SSD1306_NORMALDISPLAY
        [0xd6, 1],                  # zoom on
        [0xaf]                      # SSD1306_DISPLAYON
    ]
    for c in cmd:
        command(c)


def set_pos(col=0, page=0):
    command([0xb0 | page])  # page number
    # take upper and lower value of col * 2
    c1, c2 = col * 2 & 0x0F, col >> 3
    command([0x00 | c1])  # lower start column address
    command([0x10 | c2])  # upper start column address


def clear_oled(c=0):
    global screen
    set_pos()
    for i in range(1, 513):
        screen[i] = 0
    draw_screen()


def set_zoom(v):
    global zoom
    if zoom != v:
        command([0xd6, v])  # zoom on/off
        command([0xa7 - v])  # inverted display
        zoom = v


def draw_screen():
    set_zoom(1)
    set_pos()
    i2c.write(ADDR, screen)
```

3. ssd1306_text.py
```python
from microbit import Image, i2c

from ssd1306 import screen, set_zoom, set_pos, ADDR


def add_text(x, y, text, draw=1):
    for i in range(0, min(len(text), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(text[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            screen[ind], screen[ind + 1] = col, col
    if draw == 1:
        set_zoom(1)
        set_pos(x * 5, y)
        ind0 = x * 10 + y * 128 + 1
        i2c.write(ADDR, b'\x40' + screen[ind0:ind + 1])

```

## 2. Keyright project(.hex)

1. main.py
```python
from microbit import *
import music
import radio
import utime
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

#Configuration
'''This is the right hand code. The difference between the function of the left hand
and the right hand is the range of the octave and the radio group'''

trigger= pin8
echo = pin9

NOTE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']# Do Re Mi Fa Sol La Ti

# Note frequencies for octaves from 5 to 7
# Format: NOTE_FREQUENCIES[octave][note_index]
NOTE_FREQUENCIES = {
    5: [523, 587, 659, 698, 784, 880, 988], # C5-B5
    6: [1047, 1175, 1319, 1397, 1568, 1760, 1976], # C6-B6
    7: [2093, 2349, 2637, 2794, 3136, 3520, 3951]  # C7-B7
}

# Some default variables
right_octave = 6 # Default octave for right hand
last_right_note = -1 #Default note for right hand

#Ultrasonic sensor functions
def get_distance():
    """Read distance from ultrasonic sensor in cm"""
    # 1. Prepare trigger pin
    trigger.write_digital(0)
    utime.sleep_us(2)

    # 2. Send a 10 microsecond pulse
    trigger.write_digital(1)
    utime.sleep_us(10)
    trigger.write_digital(0)

    # 3. Measure pulse duration
    pulse_start = utime.ticks_us()
    pulse_end = pulse_start
    timeout = pulse_start + 30000  # 30 ms timeout

    # Wait for echo to go HIGH
    while echo.read_digital() == 0:
        pulse_start = utime.ticks_us()
        if pulse_start > timeout: return False

    # Wait for echo to go LOW
    while echo.read_digital() == 1:
        pulse_end = utime.ticks_us()
        if pulse_end > timeout: return False

    duration = utime.ticks_diff(pulse_end, pulse_start)

    # Convert to centimeters (speed of sound ≈ 343 m/s)
    distance_cm = (duration * 34300) // (2 * 1000000)
    return distance_cm

# Functions to connect the distance with the note
def distance_to_note_index(dist):
    """Convert distance to note index (0-6 for C-B, -1 for no note)"""
    if dist <=2 :
        return -1  # No note
    elif dist <= 5:
        return 0  # C
    elif dist <= 8:
        return 1  # D
    elif dist <= 11:
        return 2  # E
    elif dist <= 14:
        return 3  # F
    elif dist <= 17:
        return 4  # G
    elif dist <= 20:
        return 5  # A
    elif dist <= 23:
        return 6  # B
    else:
        return -1  # Too far

# The function to make sounds
def play_note(note_index, octave, duration=200):
    """Play a note at given octave"""
    if note_index >= 0 and note_index < 7:
        freq = NOTE_FREQUENCIES[octave][note_index]
        music.pitch(freq, duration)

# OLED display functions
def update_display(distance, note_index, octave):
    """Update OLED with current state"""
    clear_oled()

    # Line 1: Distance
    add_text(0, 0, str(distance)+"cm")

    # Line 2: Current note
    if note_index >= 0:
        note_name = NOTE_NAMES[note_index]
        add_text(0, 1, "Note"+str(note_name)+str(octave))
    else:
        add_text(0, 1, "Note: ---")

    # Line 3: Octave info
    add_text(0, 2, "Octave"+ str(octave))
    
# Function to change the octave
def handle_buttons(right_octave):
    # 5-6-7-5-6-7-5-6-7...... Infinite sequence by pressing the button A
    if button_a.was_pressed():
        if right_octave < 7:
            return right_octave + 1
        else:
            return 5
    #7-6-5-7-6-5-7-6-5......  Infinite sequence by pressing the button B
    elif button_b.was_pressed():
        if right_octave > 5:
            return right_octave - 1
        else:
            return 7
    #The octave remains still
    else:
        return right_octave

# ============ MAIN PROGRAM ============
radio.on()
radio.config(channel=42, power=7, group=2)
initialize()
clear_oled()
add_text(0, 0, "Right Hand")
add_text(0, 1, "Initializing...")
sleep(1000)

display.show(Image.MUSIC_QUAVER)
clear_oled()
add_text(0, 0, "Ready!")
sleep(1000)
clear_oled()
while True:
    # Read right hand distance
    distance = int(get_distance())
    
    # Handle button presses
    right_octave = handle_buttons(right_octave)

    # Convert distances to note indices
    note_index = distance_to_note_index(distance)

    # Send the information of the notes to the microbit controlling the LEDs
    radio.send(str(note_index))
    
    # Play music if notes changed
    if note_index != last_right_note:
        play_note(note_index, right_octave, duration=200)

    # Update display
    if distance >= 0:
        update_display(distance, note_index, right_octave)

    # More visual elements
    if note_index >= 0:
        display.show(Image.MUSIC_QUAVER)
    else:
        display.show(Image.MUSIC_CROTCHET)

    sleep(100)  # 10Hz update rate


```

2. ssd1306.py
```python
# I2C LCD library for the micro:bit
# Thanks to adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Thanks to lopyi2c.py
# Author: fizban99
# v0.1 beta
# Only supports display type I2C128x64

from microbit import i2c

# LCD Control constants
ADDR = 0x3C
screen = bytearray(513)  # send byte plus pixels
screen[0] = 0x40
zoom = 1


def command(c):
    i2c.write(ADDR, b'\x00' + bytearray(c))


def initialize():
    cmd = [
        [0xAE],                     # SSD1306_DISPLAYOFF
        [0xA4],                     # SSD1306_DISPLAYALLON_RESUME
        [0xD5, 0xF0],               # SSD1306_SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],               # SSD1306_SETMULTIPLEX
        [0xD3, 0x00],               # SSD1306_SETDISPLAYOFFSET
        [0 | 0x0],                  # line #SSD1306_SETSTARTLINE
        [0x8D, 0x14],               # SSD1306_CHARGEPUMP
        # 0x20 0x00 horizontal addressing
        [0x20, 0x00],               # SSD1306_MEMORYMODE
        [0x21, 0, 127],             # SSD1306_COLUMNADDR
        [0x22, 0, 63],              # SSD1306_PAGEADDR
        [0xa0 | 0x1],               # SSD1306_SEGREMAP
        [0xc8],                     # SSD1306_COMSCANDEC
        [0xDA, 0x12],               # SSD1306_SETCOMPINS
        [0x81, 0xCF],               # SSD1306_SETCONTRAST
        [0xd9, 0xF1],               # SSD1306_SETPRECHARGE
        [0xDB, 0x40],               # SSD1306_SETVCOMDETECT
        [0xA6],                     # SSD1306_NORMALDISPLAY
        [0xd6, 1],                  # zoom on
        [0xaf]                      # SSD1306_DISPLAYON
    ]
    for c in cmd:
        command(c)


def set_pos(col=0, page=0):
    command([0xb0 | page])  # page number
    # take upper and lower value of col * 2
    c1, c2 = col * 2 & 0x0F, col >> 3
    command([0x00 | c1])  # lower start column address
    command([0x10 | c2])  # upper start column address


def clear_oled(c=0):
    global screen
    set_pos()
    for i in range(1, 513):
        screen[i] = 0
    draw_screen()


def set_zoom(v):
    global zoom
    if zoom != v:
        command([0xd6, v])  # zoom on/off
        command([0xa7 - v])  # inverted display
        zoom = v


def draw_screen():
    set_zoom(1)
    set_pos()
    i2c.write(ADDR, screen)
```

3. sd1306_text.py
```python
from microbit import Image, i2c

from ssd1306 import screen, set_zoom, set_pos, ADDR


def add_text(x, y, text, draw=1):
    for i in range(0, min(len(text), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(text[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            screen[ind], screen[ind + 1] = col, col
    if draw == 1:
        set_zoom(1)
        set_pos(x * 5, y)
        ind0 = x * 10 + y * 128 + 1
        i2c.write(ADDR, b'\x40' + screen[ind0:ind + 1])
```

## 3. Right Hand LED(.hex)

main.py
```python
from microbit import *
import radio
display.off()# Avoid the function conflicts of specific GPIO PINs.
radio.on()
radio.config(channel=42, power=7,group=2)
while True:
    i=radio.receive()
    if  i is not None:
        if i=='-1':
            continue
        elif i=='0':
            pin0.write_digital(1)
            sleep(5)
            pin0.write_digital(0)
        elif i=='1':
            pin1.write_digital(1)
            sleep(5)
            pin1.write_digital(0)
        elif i=='2':
            pin2.write_digital(1)
            sleep(5)
            pin2.write_digital(0)
        elif i=='3':
            pin3.write_digital(1)
            sleep(5)
            pin3.write_digital(0)
        elif i=='4':
            pin6.write_digital(1)
            sleep(5)
            pin6.write_digital(0)
        elif i=='5':
            pin7.write_digital(1)
            sleep(5)
            pin7.write_digital(0)
        elif i=='6':
            pin8.write_digital(1)
            sleep(5)
            pin8.write_digital(0)
        else:
            pass
```

## 4. Left Hand LED(.hex)

main.py
```python
from microbit import *
import radio
display.off()# Avoid the function conflicts of specific GPIO PINs.
radio.on()
radio.config(channel=41, power=7,group=1)
while True:
    i=radio.receive()
    if  i is not None:
        if i=='-1':
            continue
        elif i=='0':
            pin0.write_digital(1)
            sleep(5)
            pin0.write_digital(0)
        elif i=='1':
            pin1.write_digital(1)
            sleep(5)
            pin1.write_digital(0)
        elif i=='2':
            pin2.write_digital(1)
            sleep(5)
            pin2.write_digital(0)
        elif i=='3':
            pin3.write_digital(1)
            sleep(5)
            pin3.write_digital(0)
        elif i=='4':
            pin6.write_digital(1)
            sleep(5)
            pin6.write_digital(0)
        elif i=='5':
            pin7.write_digital(1)
            sleep(5)
            pin7.write_digital(0)
        elif i=='6':
            pin8.write_digital(1)
            sleep(5)
            pin8.write_digital(0)
        else:
            pass
```

# This is the end of this document along with the whole software part of the project.