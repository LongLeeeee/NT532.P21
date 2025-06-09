import lgpio
import time

h = lgpio.gpiochip_open(0)
button_pin = 5

lgpio.gpio_claim_input(h, button_pin)

prev_state = 1
button_pressed = False

try:
    while True:
        state = lgpio.gpio_read(h, button_pin)
        print(f"Button state: {state}")
        if state == 0:
            print("Done")
            time.sleep(0.5)

        time.sleep(0.05)

except KeyboardInterrupt:
    lgpio.gpiochip_close(h)
