# Plan for the micro:bit project.
---
## 1. Goal

The Goal for this project is to make two microbits to create music.

## 2. Overall figure 

Requires two ultrasonic sensors and two micro:bits for two hands to cooperate with two hands.

The overall figure for the plan is this:

```
"ultrasonic module"------L1---------left_hand----Right_hand---------L2------"ultrasonic module2"
```

In this figure:

- `ultrasonic module` detect the value of `L1`, which is the distance between left hand and the module.
- `ultrasonic module2` detect the value of `L2`, which is the distance between the right hand and the second module.
- Based on L1 and L2, the micro:bit emits the sound in different frequency.

## 3. Implement scheme for music notes

1. Different music notes should be played based on the distance, the relationship of the two is listed below (just an example);

```
    if dist >= 0 and dist <= 2:
        pass
    elif dist >= 2 and dist <= 5:
        music.play("C4")
    elif dist >= 5 and dist <= 8:
        music.play("D4")
    elif dist >= 8 and dist <= 11:
        music.play("E4")
    elif dist >= 11 and dist <= 14:
        music.play("F4")
    elif dist >= 14 and dist <= 17:
        music.play("G4")
    elif dist >= 17 and dist <= 20:
        music.play("A4")
    elif dist >= 20 and dist <= 23:
        music.play("B4")
    else:
        pass
```
2. Two SSD_1306 OLED is used to show the instant distance of L1 and L2.

Tips: as we know, there is a module called music.PIANO under the bigger library music in micropython, when writing the code, this library can be added to make the sound more lively.

## 4. Implement scheme for octave

Set six different octaves for hands, indexed as 2, 3, 4 for the first micro:bit(left hand) and 5, 6, 7 for the second micro:bit(right hand).

For the two micro:bit, when Button A is pressed, the octave should be increased by 1, and the button B is pressed, the octave should be decreased by 1. As the octave index hits the upper and lower bound, it should remind users with a special message shown on OLED.

Note that every octave needs to be a set of music notes including `C4 - B4`, but in different range of frequency. Adjust the frequency phase to get the best performance.

## 5. Something can be added later on

We are trying to use the light-sensitive resistor to trigger the whole system, that is, just make the fingers get in the way of light, then the whole system can be triggered and worked.

# This is the ending of this document.
