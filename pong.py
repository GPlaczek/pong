import time
import os
import keyboard


Hight=30 #480
Width=100 #640
display_matrix = [[0 for x in range(Width)] for y in range(Hight)]
paddlesize = 5 #int(50)
paddle1pos = [int((Hight+paddlesize)/2),int(5)]
paddle2pos = [int((Hight+paddlesize)/2),int(Width-5)]
ballpos = [Hight/2,Width/2]
ballvec = [0.0,1.0]
def clear():
    for i in range(Hight):
        for j in range(Width):
            display_matrix[i][j] = 0
def display():
    for i in range(Hight):
        for j in range(Width):
            if display_matrix[i][j] == 1:
                print("#",end=""),
            else:
                print(" ",end=""),
        print("")
def add_ball():
    display_matrix[int(round(ballpos[0]))][int(round(ballpos[1]))] = 1
def add_paddle1():
    for i in range(paddlesize):
        display_matrix[int(paddle1pos[0]-paddlesize/2+i)][paddle1pos[1]] = 1
def add_paddle2():
    for i in range(paddlesize):
        display_matrix[int(paddle2pos[0]-paddlesize/2+i)][paddle2pos[1]] = 1
def update_ball():
    if int(round(ballpos[0])) <= 0 or int(round(ballpos[0])) >= Hight-1:
        ballvec[0] *= -1
    if int(round(ballpos[1])) <= 0 or int(round(ballpos[1])) >= Width-1:
        ballvec[1] *= -1
    if int(ballpos[1]) == paddle1pos[1] and ballpos[0] >= paddle1pos[0]-paddlesize/2 and ballpos[0] <= paddle1pos[0]+paddlesize/2:
        ballvec[1] *= -1
        c= ballvec[0]
        ballvec[0] = (ballpos[0]-paddle1pos[0])/(paddlesize/2)
        if int(round(ballvec[0]))==0:
            ballvec[0] = c
    if int(ballpos[1]) == paddle2pos[1] and ballpos[0] >= paddle2pos[0]-paddlesize/2 and ballpos[0] <= paddle2pos[0]+paddlesize/2:
        ballvec[1] *= -1
        ballvec[0] = (ballpos[0]-paddle2pos[0])/(paddlesize/2)
    
    ballpos[0] += ballvec[0]
    ballpos[1] += ballvec[1]
def update():
    update_ball()
    clear()
    add_ball()
    add_paddle1()
    add_paddle2()
def move_paddle2():
    if keyboard.is_pressed('o'):
        if paddle2pos[0] > paddlesize/2:
            paddle2pos[0] -= 1
    if keyboard.is_pressed('l'):
        if paddle2pos[0] < Hight-paddlesize/2:
            paddle2pos[0] += 1
def move_paddle1():
    if keyboard.is_pressed('w'):
        if paddle1pos[0] > paddlesize/2:
            paddle1pos[0] -= 1
    if keyboard.is_pressed('s'):
        if paddle1pos[0] < Hight-paddlesize/2:
            paddle1pos[0] += 1
def reset():
    paddle1pos = [int((Hight+paddlesize)/2),int(2)]
    paddle2pos = [int((Hight+paddlesize)/2),int(Width-2)]
    ballpos = [Hight/2,Width/2]
    ballvec = [1,1]
if __name__ == '__main__':
    add_ball()
    add_paddle1()
    add_paddle2()
    display()
    while(1):
        move_paddle1()
        move_paddle2()
        update()
        os.system('clear')
        display()
        time.sleep(0.05)