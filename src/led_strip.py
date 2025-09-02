from machine import Pin
import neopixel
import time

class LEDMode:
    OFF = 0
    RED = 1
    GREEN = 2
    HSV = 3
    RED_HSV = 4

class LEDStrip:
    def __init__(self, pin, num_leds=1):
        self.strip = neopixel.NeoPixel(Pin(pin), num_leds)
        self.num_leds = num_leds
        self.mode = LEDMode.OFF
        self.hue = 0.0
        self._blink_init()

    def _blink_init(self):
        for _ in range(2):
            self._fill((255, 255, 255))
            time.sleep_ms(100)
            self._fill((0, 0, 0))
            time.sleep_ms(100)

    def _fill(self, color):
        for i in range(self.num_leds):
            self.strip[i] = color
        self.strip.write()

    def setMode(self, mode):
        self.mode = mode
        if mode == LEDMode.OFF:
            self._fill((0, 0, 0))
        elif mode == LEDMode.RED:
            self._fill((255, 0, 0))
        elif mode == LEDMode.GREEN:
            self._fill((0, 255, 0))
        # dynamic modes will be handled in step()

    def step(self, t, dt):
        if self.mode == LEDMode.HSV:
            self.hue = (self.hue + dt / 5) % 1.0  # slow cycle ~5s
            rgb = self._hsv_to_rgb(self.hue, 1.0, 1.0)
            self._fill(rgb)
        elif self.mode == LEDMode.RED_HSV:
            self.hue = (self.hue + dt / 5) % 1.0
            hue = self.hue * 0.1  # restrict to red tones
            rgb = self._hsv_to_rgb(hue, 1.0, 1.0)
            self._fill(rgb)

    def _hsv_to_rgb(self, h, s, v):
        i = int(h * 6)
        f = h * 6 - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - f * s))
        t = int(255 * v * (1 - (1 - f) * s))
        v = int(255 * v)
        i %= 6
        if i == 0:
            return (v, t, p)
        if i == 1:
            return (q, v, p)
        if i == 2:
            return (p, v, t)
        if i == 3:
            return (p, q, v)
        if i == 4:
            return (t, p, v)
        if i == 5:
            return (v, p, q)
