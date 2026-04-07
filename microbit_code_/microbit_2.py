from microbit import *
import radio
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text


TRIG_PIN = pin1
ECHO_PIN = pin2
last_right_note = -1

NOTE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']


right_octave = 5  

NOTE_FREQUENCIES = {
    2: [65, 73, 82, 87, 98, 110, 123],      
    3: [131, 147, 165, 175, 196, 220, 247], 
    4: [262, 294, 330, 349, 392, 440, 494], 
    5: [523, 587, 659, 698, 784, 880, 988], 
    6: [1047, 1175, 1319, 1397, 1568, 1760, 1976], 
    7: [2093, 2349, 2637, 2794, 3136, 3520, 3951]  
}

NOTE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']


def get_distance():
    """Read distance from ultrasonic sensor in cm"""
    TRIG_PIN.write_digital(0)
    sleep_us(2)
    TRIG_PIN.write_digital(1)
    sleep_us(10)
    TRIG_PIN.write_digital(0)
    
    # Wait for echo
    timeout = 30000  
    start = running_time()
    while ECHO_PIN.read_digital() == 0:
        if running_time() - start > timeout:
            return -1
    
    pulse_start = running_time()
    
    while ECHO_PIN.read_digital() == 1:
        if running_time() - pulse_start > timeout:
            return -1
    
    pulse_end = running_time()
    
    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 0.0343) / 2
    
    return round(distance, 1)

# Note conversion
def distance_to_note_index(dist):
    """Convert distance to note index (0-6 for C-B, -1 for no note)"""
    if dist < 0 or dist <= 2:
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

# OLED
def update_display(distance, note_index, octave):
    """Update OLED with current state"""
    clear_oled()
    

    add_text(0, 0, f"Distance: {distance}cm")
    

    if note_index >= 0:
        note_name = NOTE_NAMES[note_index]
        add_text(0, 1, f"Note: {note_name}{octave}")
    else:
        add_text(0, 1, "Note: ---")
    

    add_text(0, 2, f"Octave: {octave}")
    

    add_text(0, 3, "A:+ B:-")

# Button contorl
def handle_buttons(right_octave):
    """Handle octave changes for right hand"""
    if button_a.was_pressed():
        if right_octave < 7:
            return right_octave +1
        else:
            return 5
    
    if button_b.was_pressed():
        if right_octave > 5:
            right_octave -= 1
        else:
            return 7

# Main
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
    
    distance = get_distance()

    
    right_octave = handle_buttons(right_octave)

    
    note_index = distance_to_note_index(distance)
    radio.send(str(note_index))
    if note_index != last_right_note:
        play_note(note_index, right_octave, duration=200)
        last_right_note = note_index

    
    if distance >= 0:
        update_display(distance, note_index, right_octave)

    
    if note_index >= 0:
        display.show(Image.MUSIC_QUAVER)
    else:
        display.show(Image.MUSIC_CROTCHET)

    sleep(50) 
