# based on https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/master/Rotary_Encoder/rotary_encoder_volume.py
import rotaryio
import board
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Update to match GP where "SW" from encoder is connected
button = digitalio.DigitalInOut(board.GP6) 
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Update to match GP where "DT" is fisrt and "CLK" is second
encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1)

cc = ConsumerControl(usb_hid.devices)

button_state = None
last_position = encoder.position

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        button_state = None