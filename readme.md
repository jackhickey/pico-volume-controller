# Pi Pico Volume Controller

## Background

This guide is a Pi Pico version of a [giant media control volume knob from the prusa website](https://blog.prusaprinters.org/3d-print-an-oversized-media-control-volume-knob-arduino-basics_30184/)

While [Arduino IDE support for Pi Pico](https://www.seeedstudio.com/blog/2021/01/29/arduino-ide-support-announced-for-the-raspberry-pi-pico/) was announced, there's no sign of a release yet. Without the ardunio support rotary encoder c++ libraries _or_ decent support in [microPython](https://micropython.org)(which comes pre-installed on the pico), the beta [CircuitPython](https://circuitpython.org) build seems to be the way to go!

## Hardware

- [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/)
- KY-040 Rotary Encoder (Others should work, but tested with this style)
- Some cables to attach your Rotary Encoder to your Pico 🤔


### Rough pin mapping

| KY-040 | Pico Pi                      |
|--------|------------------------------|
| GND    | Any GND on pi                |
| +      | 3v3                          |
| SW     | Any GP pin                   |
| DT     | Any GP pin _x_               |
| CLK    | Next sequential GP pin _x+1_ |



## Install Circuit Python
_Once released_ adafruit-circuitpython-raspberry_pi_pico-en_US-6.2.0-beta.4.uf2 will contain `rotaryio` support for pi pico.

For now, grab the latest build from their s3 builds bucket [here](https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/raspberry_pi_pico/en_US/).

To install
- connect the pi pico while holding the `BOOTSEL` botton.
- a storage device called `RPI-RP2` should auto-mount
- copy the `.uf2` file to the root of `RPI-RP2`. The pico will automatically install ciruit pyton and reboot

The pico should reconnect, this time mounted as `CIRCUITPY`. It will contain `boot_out.txt`, `code.py` and a `lib` directory.

## Install adafruit_hid.consumer_control

Not all adafruit libraries come packaged with CircuitPython (I assume to keep build size down 🧐)

- Download the latest Bundle Version 6.x from https://circuitpython.org/libraries
- Unzip, and copy the `adafruit_hid` directory inside the `lib` directory on your pico

## Update code to match pinout

Depending on which pins you connect to on your Pico, update the `GPx` references in `code.py` to match your setup.

## Copy code to Pico

Finally, replace the `code.py` on the Pico with your updated `code.py`. Once saved, your media control + volume knob should now function!


## References
- [3D print a media control volume knob for your computer and learn Arduino basics](https://blog.prusaprinters.org/3d-print-an-oversized-media-control-volume-knob-arduino-basics_30184/)
- [Circuit Python Rotary Encoder guide](https://learn.adafruit.com/rotary-encoder/circuitpython)
