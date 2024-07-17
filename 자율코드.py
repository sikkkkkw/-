import RPi.GPIO as GPIO
import time
import threading
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# init super sonic sensor
trig1 = 19
echo1 = 26

trig2 = 21
echo2 = 20

GPIO.setup(trig1, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)

GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)

# init motor driver
pin1 = 23
pin2 = 24
ENA = 18

pin3 = 17
pin4 = 27
ENB = 22

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwmA = GPIO.PWM(ENA, 90)
pwmA.start(0)

pwmB = GPIO.PWM(ENB, 90)
pwmB.start(0)

speed_turn = 100
time_turn = 0.8

speed_go = 90
speed_back = 90

time_go = 1


def stop():
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)


def turn_left():
    pwmA.ChangeDutyCycle(speed_turn)
    pwmB.ChangeDutyCycle(speed_turn)
    GPIO.output(pin1, True)
    GPIO.output(pin2, False)
    GPIO.output(pin3, False)
    GPIO.output(pin4, True)
    time.sleep(time_turn)
    stop()


def turn_right():
    pwmA.ChangeDutyCycle(speed_turn)
    pwmB.ChangeDutyCycle(speed_turn)
    GPIO.output(pin1, False)
    GPIO.output(pin2, True)
    GPIO.output(pin3, True)
    GPIO.output(pin4, False)
    time.sleep(time_turn)
    stop()


def go_forward():
    pwmA.ChangeDutyCycle(speed_go)
    pwmB.ChangeDutyCycle(speed_go)
    GPIO.output(pin1, False)
    GPIO.output(pin2, True)
    GPIO.output(pin3, False)
    GPIO.output(pin4, True)
    time.sleep(time_go)


def go_backward():
    pwmA.ChangeDutyCycle(speed_back)
    pwmB.ChangeDutyCycle(speed_back)
    GPIO.output(pin1, True)
    GPIO.output(pin2, False)
    GPIO.output(pin3, True)
    GPIO.output(pin4, False)
    time.sleep(time_go)
    stop()


def get_distance(sensor_trig, sensor_echo):
    GPIO.output(sensor_trig, False)
    time.sleep(0.0000001)

    GPIO.output(sensor_trig, True)
    time.sleep(0.0000001)
    GPIO.output(sensor_trig, False)

    while GPIO.input(sensor_echo) == 0:
        pulse_start = time.time()

    while GPIO.input(sensor_echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
    return distance


def loop_driver(nloop, nsec):
    try:
        while True:
            dt1 = get_distance(trig1, echo1)
            dt2 = get_distance(trig2, echo2)
            print("Distance Sensor 1: ", dt1, "cm")
            print("Distance Sensor 2: ", dt2, "cm")
            # less than 5cm, thread ends
            if dt1 < 5 or dt2 < 5:
                break
            # less than 20cm, randomly turn left or right or go back
            if dt1 > 40 and dt2 > 40:
                go_forward()
            if dt1 < 40:
                go_backward()
                turn_left()
            if dt2 < 40:
                go_backward()
                turn_right()
        print("End thread")
    finally:
        stop()
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()


thread_driver = threading.Thread(target=loop_driver, args=(0, 0))
print("Start thread")
thread_driver.start()
thread_driver.join()
print("End app")