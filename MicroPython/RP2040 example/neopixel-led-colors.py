from machine import Pin
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff, sleep_ms

np = NeoPixel(Pin(22), 1)
brightness = 255
colors = [[brightness, 0, 0],  # red
          [0, brightness, 0],  # green
          [0, 0, brightness],  # blue
          [brightness, brightness, brightness],  # white
          [0, 0, 0]]  # close

timer_start = ticks_ms()
timer_per = 500
i = 0

while True:
    diff = ticks_diff(ticks_ms(), timer_start)
    if diff >= timer_per:
        np[0] = colors[i]
        np.write()
        if i >= len(colors) - 1:
            i = 0
        else:
            i += 1
        timer_start = ticks_ms()
