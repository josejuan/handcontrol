import time
import random
from servo import Servo
from led_strip import LEDStrip, LEDMode

PIN_LED = 14       # D5 - LED strip
PIN_MENIQUE = 12   # D6 - Servo dedo meñique


def main():
    led = LEDStrip(PIN_LED, num_leds=4)
    # P1 y P2 son puntos de control de la curva de deformación
    servo = Servo(PIN_MENIQUE, p1=50, p2=130)

    start = time.ticks_ms()
    last = start
    last_mode_change = start
    modes = [LEDMode.OFF, LEDMode.RED, LEDMode.GREEN, LEDMode.HSV, LEDMode.RED_HSV]

    # iniciar primer movimiento
    target = random.random() * 180
    speed = abs(target - servo.getAngle()) / 0.5 if target != servo.getAngle() else 0
    servo.setSpeed(speed)
    servo.moveTo(target)
    print("Servo moving to {:.1f} deg at {:.1f} deg/s".format(target, speed))

    while True:
        now = time.ticks_ms()
        dt = time.ticks_diff(now, last) / 1000.0
        t = time.ticks_diff(now, start) / 1000.0
        last = now

        servo.step(t, dt)
        led.step(t, dt)

        if servo.getStatus() == Servo.STOPPED:
            target = random.random() * 180
            speed = abs(target - servo.getAngle()) / 0.5 if target != servo.getAngle() else 0
            servo.setSpeed(speed)
            servo.moveTo(target)
            print("Servo moving to {:.1f} deg at {:.1f} deg/s".format(target, speed))

        if time.ticks_diff(now, last_mode_change) >= 5000:
            mode = random.choice(modes)
            led.setMode(mode)
            print("LED mode ->", mode)
            last_mode_change = now

        time.sleep_ms(20)


if __name__ == "__main__":
    main()
