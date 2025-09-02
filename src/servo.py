from machine import Pin, PWM

class Servo:
    MOVING = "Moving"
    STOPPED = "Stopped"

    def __init__(self, pin, p1, p2, us_min=600, us_max=2400):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.us_min = us_min
        self.us_max = us_max
        self._update_curve(p1, p2)
        self._current = 0.0
        self._target = 0.0
        self._speed = 0.0
        self._status = self.STOPPED
        # move to 0 degrees on start
        self._write_angle(self._map_angle(self._current))

    def _update_curve(self, p1, p2):
        """Recalculate polynomial coefficients and lookup table."""
        a = 810 + 13.5 * (p1 - p2)
        b = -810 - 22.5 * p1 + 18 * p2
        c = 180 + 9 * p1 - 4.5 * p2
        self._a, self._b, self._c = a, b, c
        self._table = []
        for i in range(181):
            t = i / 180.0
            val = ((a * t + b) * t + c) * t  # cubic polynomial, d=0
            self._table.append(val)

    def _map_angle(self, angle):
        """Map an input angle (0-180) using the lookup table."""
        if angle <= 0:
            return 0.0
        if angle >= 180:
            return 180.0
        i = int(angle)
        frac = angle - i
        y0 = self._table[i]
        y1 = self._table[i + 1]
        return y0 + (y1 - y0) * frac

    def _write_angle(self, angle):
        us = self.us_min + (self.us_max - self.us_min) * angle / 180.0
        self.pwm.duty_ns(int(us * 1000))

    def setSpeed(self, speed):
        self._speed = max(0.0, speed)

    def moveTo(self, angle):
        angle = max(0.0, min(180.0, angle))
        self._target = angle
        if self._speed > 0:
            self._status = self.MOVING
        else:
            self._current = angle
            self._write_angle(self._map_angle(self._current))
            self._status = self.STOPPED

    def getStatus(self):
        return self._status

    def getAngle(self):
        return self._current

    def step(self, t, dt):
        if self._status != self.MOVING:
            return
        diff = self._target - self._current
        step_deg = self._speed * dt
        if abs(diff) <= step_deg:
            self._current = self._target
            self._status = self.STOPPED
        else:
            self._current += step_deg if diff > 0 else -step_deg
        self._write_angle(self._map_angle(self._current))
