# WiiHid PyRuler

Experiments with PyRuler (CircuitPython on SAMD21) and Wii Nuchuck

## Hardware

I had an [Adafruit PyRuler](https://www.adafruit.com/product/4319) and Wii Nunchuck with a broken plug, and then dicovered the [Adafruit Wii Nunchuck Breakout](https://www.adafruit.com/product/4836). Combined with a desire to re-learn soldering and start doing electronics and microcontroller stuff, I had a mini project to start with. I soldered the Adafruit breakout directly to the PyRuler to get both a Stemma QT (I2C) port and a Wii Accessory "port" to be able to test with a good Nunchuck. Then soldered the damaged Nunchuck to half of a shorty Stemma QT cable to plug it directly into the breakout.

## Software
Duplicated the original PyRuler [CircuitPython](https://circuitpython.org/) program with additions of sending τ (tau) on the "Digikey" touchpadand some tweaks to the LED lighting and key repeats. I used the [WiiChuck Library](https://github.com/jfurcean/CircuitPython_WiiChuck) to read the Nunchuck and then send USB HID commands.

## Notes

It was interesting managing memory in the limited space left on the SAMD21 microcontroller when running CircuitPython. I ended up inlining the specifically needed keycodes just to fit the mouse functionality in. I then had to remove the Windows and Mac keycode sending functions in order to make room for handling a middle click when pressing both Nunchuck buttons. THe middle button stuff could probably use a debouncing, but the Adafruit Debouncer library took too much memory! As did trying to switch to emulating a gamepad with the Adafruit HID library and examples , but also ran into memory limitations. Either could probably be done with some effort, but I'm continuing on with Arduino/PlatformIO on a [QT Py M0](https://www.adafruit.com/product/4600) for further experimentation with Wii Nunchucks and other accessories.

### Further Reading

https://github.com/just6979/WiiHID_QT-Py-M0.pio
