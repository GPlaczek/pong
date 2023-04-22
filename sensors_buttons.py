import os
import keyboard

import RPi.GPIO as GPIO
import sys
import time
import serial



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
def move_paddle2(pos):
    if keyboard.is_pressed('o'):
        if pos > 0:
            pos -= 10
    if keyboard.is_pressed('l'):
        if pos < Hight-paddlesize:
            pos += 10
    return pos
def move_paddle1(pos):
    if keyboard.is_pressed('w'):
        if pos > 0:
            pos -= 10
    if keyboard.is_pressed('s'):
        if pos < Hight-paddlesize:
            pos += 10
    return pos


if __name__ == '__main__':
    ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
    )
    try:
        while True:
            paddle1pos=move_paddle1(paddle1pos)
            paddle2pos=move_paddle2(paddle2pos)
            # print(paddle1pos,paddle2pos)
            update_ball()
            # print(ballpos)
            print(score)
            ser.write(bytearray("{} {} {} {}\n".format(int(paddle1pos), int(paddle2pos),int(ballpos[0]),int(ballpos[1])), "utf-8"))
            _ = ser.readline()

    except KeyboardInterrupt:
        GPIO.cleanup()


col = 2

ser.write(bytes("33 66 66\n", "utf-8"))
#time.sleep(5)
