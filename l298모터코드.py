# -*- coding: utf-8 -*-

# 라즈베리파이 GPIO 패키지 
import RPi.GPIO as GPIO
from time import sleep

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWARD = 2

# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 5    # BCM5 29 pin
ENB = 27   # BCM27 13 pin

#GPIO PIN
IN1 = 11   # BCM11 23 pin
IN2 = 9    # BCM9 21 pin
IN3 = 10   # BCM10 19 pin
IN4 = 22   # BCM22 15 pin


class motor:
    def __init__(self, inPin1, inPin2, inPin3, inPin4, enAPin, enBPin):
        
        # GPIO 모드 설정 
        GPIO.setmode(GPIO.BCM)
        
        self.motorPin = [[enAPin, inPin1, inPin2],[enBPin, inPin3, inPin4]]
        self.pwm = []
        self.pwm.append(self.setPinConfig(CH1))
        self.pwm.append(self.setPinConfig(CH2))

    # 핀 설정 함수
    def setPinConfig(self, ch):
        EN = self.motorPin[ch][0]
        INA = self.motorPin[ch][1]
        INB = self.motorPin[ch][2]

        GPIO.setup(EN, GPIO.OUT)
        GPIO.setup(INA, GPIO.OUT)
        GPIO.setup(INB, GPIO.OUT)
        # 100khz 로 PWM 동작 시킴 
        pwm = GPIO.PWM(EN, 100) 
        # 우선 PWM 멈춤.   
        pwm.start(0) 
        return pwm

    # 모터 제어 함수
    def setMotorControl(self, ch, speed, stat):
        
        EN = self.motorPin[ch][0]
        INA = self.motorPin[ch][1]
        INB = self.motorPin[ch][2]

        #모터 속도 제어 PWM
        self.pwm[ch].ChangeDutyCycle(speed)  
        
        if stat == FORWARD:
            GPIO.output(INA, HIGH)
            GPIO.output(INB, LOW)
            
        #뒤로
        elif stat == BACKWARD:
            GPIO.output(INA, LOW)
            GPIO.output(INB, HIGH)
            
        #정지
        elif stat == STOP:
            GPIO.output(INA, LOW)
            GPIO.output(INB, LOW)

            
    # 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
    def setMotor(self, ch, speed, stat):
        self.setMotorContorl(self.pwm[ch], self.motorPin[ch][1], self.motorPin[ch][2], speed, stat)

    def __del__(self):
        # 종료
        GPIO.cleanup()

if __name__ == "__main__":
    mt = motor(IN1, IN2, IN3, IN4, ENA, ENB)
    mt.setMotorControl(CH1, 100, FORWARD)
    mt.setMotorControl(CH2, 100, FORWARD)
    a = input('exit')
