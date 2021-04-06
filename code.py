# based on https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/master/Rotary_Encoder/rotary_encoder_volume.py
import rotaryio
import board
import digitalio
import usb_hid
import time
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Update to match GP where "SW" from encoder is connected
button = digitalio.DigitalInOut(board.GP3)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Update to match GP where "DT" is fisrt and "CLK" is second
encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP5)

cc = ConsumerControl(usb_hid.devices)

button_state = None
last_position = encoder.position

# Setup as keyboard
# configure device as keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

def open_app(app):
	kbd.send(Keycode.COMMAND, Keycode.SPACE)
	time.sleep(0.2)
	layout.write(app)
	time.sleep(0.2)
	kbd.send(Keycode.ENTER)
    
def open_site(site):
    open_app("chrome")
    kbd.send(Keycode.COMMAND, Keycode.T)
    layout.write(site)
    kbd.send(Keycode.ENTER)

    
def button_pressed():
    return button.value == False and button_state is None
    
def button_released():
    return button.value == True and button_state == "pressed"


# State for handling clicks
click_count = 0
dbl_click_start_time = 0.0



# config in seconds
dbl_click_max_time = .750
dbl_click_debounce_time = 0.1
timer_compensation = 0.1

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    click_triggered = False

# handling rotation and volume change
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position

# general button state    
    if button_pressed():
        button_state = "pressed"

    if button_released():
        button_state = None
        click_count += 1
        print("click_count", click_count)
        time.sleep(dbl_click_debounce_time)
        if click_count == 1 and dbl_click_start_time == 0.0:
            dbl_click_start_time = time.monotonic()
# handling clicking

    if dbl_click_start_time != 0.0:
        time_since_last_click = time.monotonic() - dbl_click_start_time
        ## Double Click
        if click_count > 1 and time_since_last_click >= timer_compensation and time_since_last_click <= dbl_click_max_time:
            print("DOUBLE click")
            print("time since last click", time_since_last_click)
            print("click_count value", click_count)
            open_site("https://www.giantbomb.com")
            print("setting click count to zero from..", click_count)
            click_count = 0
            dbl_click_start_time = 0.0
            
        ## Single Click
        if click_count == 1 and time_since_last_click > dbl_click_max_time:
            print("SINGLE click")
            print("time since last click", time_since_last_click)
            print("")
            print("setting click count to zero from..", click_count)
            cc.send(ConsumerControlCode.PLAY_PAUSE)
            click_count = 0
            dbl_click_start_time = 0.0
            


