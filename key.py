from microbit import *
import music
import radio
import utime
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

# ============ CONFIGURATION ============
trigger= pin8
echo = pin9

# Note frequencies for octaves 2-7 (C to B)
# Format: NOTE_FREQUENCIES[octave][note_index]
NOTE_FREQUENCIES = {
    2: [65, 73, 82, 87, 98, 110, 123],      # C2-B2
    3: [131, 147, 165, 175, 196, 220, 247], # C3-B3
    4: [262, 294, 330, 349, 392, 440, 494], # C4-B4
    5: [523, 587, 659, 698, 784, 880, 988], # C5-B5
    6: [1047, 1175, 1319, 1397, 1568, 1760, 1976], # C6-B6
    7: [2093, 2349, 2637, 2794, 3136, 3520, 3951]  # C7-B7
}

NOTE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# ============ GLOBAL VARIABLES ============
left_octave = 3  # Default octave for left hand
last_left_note = -1
# ============ ULTRASONIC SENSOR FUNCTIONS ============
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

# ============ MUSIC FUNCTIONS ============
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

def play_note(note_index, octave, duration=200):
    """Play a note at given octave"""
    if note_index >= 0 and note_index < 7:
        freq = NOTE_FREQUENCIES[octave][note_index]
        music.pitch(freq, duration)

# ============ OLED DISPLAY FUNCTIONS ============
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

    # Line 4: Controls
    add_text(0, 3, "A:+ B:-")
# ============ BUTTON HANDLERS ============
def handle_buttons(left_octave):
    """Handle octave changes for right hand"""
    if button_a.was_pressed():
        if left_octave < 4:
            return left_octave + 1
        else:
            return 2

    elif button_b.was_pressed():
        if left_octave > 2:
            return left_octave - 1
        else:
            return 4
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
    add_text(0,0,str(distance))

    left_octave = handle_buttons(left_octave)

    # Convert distances to note indices
    note_index = distance_to_note_index(distance)
    radio.send(str(note_index))
    # Play music if notes changed
    if note_index != last_left_note:
        play_note(note_index, left_octave, duration=200)

    # Update display
    if distance >= 0:
        update_display(distance, note_index, left_octave)

    if note_index >= 0:
        display.show(Image.MUSIC_QUAVER)
    else:
        display.show(Image.MUSIC_CROTCHET)

    sleep(100)  # 20Hz update rate

