"""
SSD1306 OLED Driver for micro:bit
Minimal implementation for 128x64 I2C displays
"""

from microbit import i2c

# I2C Address
ADDR = 0x3C

def initialize():
    """Initialize the OLED display"""
    commands = [
        0xAE,  # Display off
        0xD5, 0x80,  # Set display clock
        0xA8, 0x3F,  # Set multiplex ratio
        0xD3, 0x00,  # Set display offset
        0x40,  # Set start line
        0x8D, 0x14,  # Enable charge pump
        0x20, 0x00,  # Set memory mode
        0xA1,  # Set segment remap
        0xC8,  # Set COM scan direction
        0xDA, 0x12,  # Set COM pins
        0x81, 0xCF,  # Set contrast
        0xD9, 0xF1,  # Set precharge
        0xDB, 0x40,  # Set VCOMH
        0xA4,  # Display resume
        0xA6,  # Normal display
        0xAF   # Display on
    ]
    
    for cmd in commands:
        i2c.write(ADDR, bytes([0x00, cmd]))

def clear_oled():
    """Clear the entire display"""
    for page in range(8):
        i2c.write(ADDR, bytes([0x00, 0xB0 + page]))  # Set page
        i2c.write(ADDR, bytes([0x00, 0x00]))  # Set lower column
        i2c.write(ADDR, bytes([0x00, 0x10]))  # Set higher column
        
        # Clear this page (128 bytes)
        for _ in range(16):
            i2c.write(ADDR, bytes([0x40] + [0x00] * 8))
