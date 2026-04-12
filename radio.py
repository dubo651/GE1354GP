from microbit import *
import radio
display.off()
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
