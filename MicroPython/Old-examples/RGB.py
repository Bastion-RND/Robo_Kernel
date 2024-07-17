import array, time
from machine import Pin
import rp2

led_count = 1 
PIN_NUM = 23 
brightness = 1.0 

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24)

def ws2812():
    
    T1 = 2
    T2 = 5
    T3 = 3
    
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
sm.active(1)
ar = array.array("I", [0 for _ in range(led_count)])

def pixels_show(brightness_input=brightness):
    
    dimmer_ar = array.array("I", [0 for _ in range(led_count)])
    
    for ii,cc in enumerate(ar):
        
        r = int(((cc >> 8) & 0xFF) * brightness_input) 
        g = int(((cc >> 16) & 0xFF) * brightness_input) 
        b = int((cc & 0xFF) * brightness_input)
        
        dimmer_ar[ii] = (g<<16) + (r<<8) + b
        
    sm.put(dimmer_ar, 8)
    time.sleep_ms(1)

def pixels_set(i, color):
    
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
        
def breathing_led(color):
    
    step = 5
    
    breath_amps = [ii for ii in range(0,255,step)]
    
    breath_amps.extend([ii for ii in range(255,-1,-step)])
    
    for ii in breath_amps:
        
        for jj in range(len(ar)):
            
            pixels_set(jj, color)
            
        pixels_show(ii/255)
        time.sleep(0.02)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
white = (255,255,255)
blank = (0,0,0)
colors = [blue,yellow,cyan,red,green,white]

while True:
    
    for color in colors:
        
        breathing_led(color)
        time.sleep(0.1) 