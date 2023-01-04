import RPi.GPIO as GPIO
import sys
import time
import serial

import os
import keyboard

GPIO.setmode(GPIO.BOARD)

ECHO_1 = 11
TRIGGER_1 = 7

ECHO_2 = 24
TRIGGER_2 = 18

GPIO.setup(TRIGGER_1, GPIO.OUT)
GPIO.setup(ECHO_1, GPIO.IN)
GPIO.setup(TRIGGER_2, GPIO.OUT)
GPIO.setup(ECHO_2, GPIO.IN)


Hight=480
Width=640
paddlesize = 120 
paddle1pos = int((Hight)/2)
paddle2pos = int((Hight)/2)
ballpos = [Width/2,Hight/2]
ballvec = [10.0,10.0]
ballsize=40
score=[0,0]
def reset():
    global paddle1pos 
    global paddle2pos
    global ballpos
    global ballvec
    paddle1pos = int((Hight)/2)
    paddle2pos = int((Hight)/2)
    ballpos = [Width/2,Hight/2]
    ballvec = [10.0,10.0]
def update_ball():
    global ballpos
    global ballvec
    x=ballpos[0]+ballvec[0]
    y=ballpos[1]+ballvec[1]
    if x<0 or x>Width-ballsize:
        score[(ballpos[0]>Width/2)]+=1
        reset()
    elif y<0 or y>Hight-ballsize:
        ballvec[1]*=-1
    elif ballpos[0]<=60 and y>paddle1pos-ballsize and y<paddle1pos+120:
        ballvec[0]*=-1
        c= ballvec[1]
        ballvec[1] = (ballpos[1]-paddle1pos)/(paddlesize/2)*10
        if int(round(ballvec[1]))==0:
            ballvec[1] = c
    elif ballpos[0]>=580-ballsize and y>paddle2pos-ballsize and y<paddle2pos+120:
        ballvec[0]*=-1
        c= ballvec[1]
        ballvec[1] = (ballpos[1]-paddle2pos)/(paddlesize/2)*10
        if int(round(ballvec[1]))==0:
            ballvec[1] = c
    ballpos[1] += ballvec[1]
    ballpos[0] += ballvec[0]
def distance(echo, trigger):
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.00001)

    GPIO.output(trigger, GPIO.LOW)
    
    StartTime = time.time()
    StopTime = time.time()

    i = 0
    while GPIO.input(echo) == 0:
        StartTime = time.time()
        i+=1
        if i > 1000:
            return -1;

    i = 0
    while GPIO.input(echo) == 1:
        StopTime = time.time()
        i+=1
        if i > 1000:
            return -1;

    return ((StopTime - StartTime) * 34300) / 2
def move_paddle1(pos):
    global paddle1pos
    if pos<15:
        if paddle1pos > 0:
            paddle1pos -= 20
    elif pos>25:
        if paddle1pos < Hight-paddlesize:
            paddle1pos += 20

def move_paddle2(pos):
    global paddle2pos
    if pos<15:
        if paddle2pos > 0:
            paddle2pos -= 20
    elif pos>25:
        if paddle2pos < Hight-paddlesize:
            paddle2pos += 20

if __name__ == '__main__':
    ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
    )
    GPIO.output(TRIGGER_1, GPIO.LOW)
    GPIO.output(TRIGGER_2, GPIO.LOW)
    time.sleep(2)
    try:
        while True:
            dist1 = distance(ECHO_1, TRIGGER_1)
            while dist1 == -1:
                dist1 = distance(ECHO_1, TRIGGER_1)
            
            dist2 = distance(ECHO_2, TRIGGER_2)
            while dist2 == -1:
                dist2 = distance(ECHO_2, TRIGGER_2)
            update_ball()
            # print(dist1,dist2)
            move_paddle1(dist1)
            move_paddle2(dist2)
            print(score)
            ser.write(bytearray("{} {} {} {}\n".format(int(paddle2pos), int(paddle1pos),int(ballpos[0]),int(ballpos[1])), "utf-8"))
            _ = ser.readline()
            # print(dist1, dist2)
            # ser.write(bytearray("{} {} 1\n".format(int(dist1), int(dist2)), "utf-8"))

    except KeyboardInterrupt:
        GPIO.cleanup()


col = 2

# ser.write(bytes("33 66 66\n", "utf-8"))
#time.sleep(5)
