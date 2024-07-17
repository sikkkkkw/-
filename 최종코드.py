import RPi.GPIO as GPIO
import time
import curses
import random

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LEFT SENSOR (라인 트레이서)
left_sensor = 11
right_sensor = 9

# RIGHT WHEEL
pin1 = 23
pin2 = 24
ENA = 18

# LEFT WHEEL
pin3 = 17
pin4 = 27
ENB = 22

# 초음파 센서 핀 설정
TRIG = 20  # 초음파 트리거 핀
ECHO = 21  # 초음파 에코 핀

GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

pwmA = GPIO.PWM(ENA, 90)
pwmA.start(0)

pwmB = GPIO.PWM(ENB, 90)
pwmB.start(0)

speed_turn = 80
speed_go = 80


obstacle_threshold = 25 

current_mode = "manual"

def set_mode(mode):
    global current_mode
    current_mode = mode
    stdscr.clear()
    stdscr.addstr(0, 0, f"Current Mode: {mode.capitalize()}")

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

def turn_right():
    pwmA.ChangeDutyCycle(speed_turn)
    pwmB.ChangeDutyCycle(speed_turn)
    GPIO.output(pin1, False)
    GPIO.output(pin2, True)
    GPIO.output(pin3, True)
    GPIO.output(pin4, False)

def go_forward():
    pwmA.ChangeDutyCycle(speed_go)
    pwmB.ChangeDutyCycle(speed_go)
    GPIO.output(pin1, False)
    GPIO.output(pin2, True)
    GPIO.output(pin3, False)
    GPIO.output(pin4, True)

def backward():
    pwmA.ChangeDutyCycle(speed_go)
    pwmB.ChangeDutyCycle(speed_go)
    GPIO.output(pin1, True)
    GPIO.output(pin2, False)
    GPIO.output(pin3, True)
    GPIO.output(pin4, False)

def random_avoid_obstacle():
    random_direction = random.choice(["left", "right"])
    if random_direction == "left":
        turn_left()
    else:
        turn_right()
    time.sleep(1)  # 랜덤으로 돌기 전에 1초 동안 직진합니다.
    go_forward()  # 랜덤 방향으로 회피 후 다시 직진

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)

try:
    set_mode(current_mode)  # 초기 모드 설정

    while True:
        stdscr.refresh()
        key = stdscr.getch()

        if key == ord('j'):
            set_mode("manual")
        elif key == ord('k'):
            set_mode("line_follower")
        elif key == ord('l'):
            set_mode("ultrasonic")
        elif key == ord('w'):
            go_forward()
        elif key == ord('s'):
            backward()
        elif key == ord('a'):
            turn_right()
            time.sleep(0.2)
            stop()
        elif key == ord('d'):
            turn_left()
            time.sleep(0.2)
            stop()
        elif key == ord('e'):
            stop()
        elif key == ord('q'):
            break

        if current_mode == "manual":
            # 수동 조작 모드
            pass
        elif current_mode == "line_follower":
            # 라인 트레이서 모드
            sensor_right = GPIO.input(right_sensor)
            sensor_left = GPIO.input(left_sensor)

            if sensor_right == GPIO.HIGH and sensor_left == GPIO.HIGH:
                go_forward()
            elif sensor_right == GPIO.HIGH and sensor_left == GPIO.LOW:
                turn_right()
            elif sensor_right == GPIO.LOW and sensor_left == GPIO.HIGH:
                turn_left()
            else:
                stop()
        elif current_mode == "ultrasonic":
            # 초음파 센서 모드
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150

            if distance < obstacle_threshold:
                # 장애물을 감지하면 회피 동작을 수행하지 않고 직진
                random_avoid_obstacle()

finally:
    curses.endwin()
    GPIO.cleanup()
