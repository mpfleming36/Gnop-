'''
CS 391
Mike Fleming
Lab 1: Pong

'''
import pygame
import sys
import random

from Box import *
from Colors import *
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
scoreBoard = pygame.font.SysFont("monospace", 30)
redScore = 0
blueScore = 0
maxScore = 11
xDefault = SCREEN_WIDTH/2-5
yDefault = SCREEN_HEIGHT/2-5
paddleDefault = (SCREEN_HEIGHT/2)-25
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ballvx = random.randint(2,4)*((-1)**random.randint(0,1))
ballvy = random.randint(2,4)*((-1)**random.randint(0,1))


boxList = []
boxList.append(Box(xDefault,yDefault,10,10,ballvx,ballvy,Color.white,"pong")) #ball
boxList.append(Box(10, paddleDefault, 10, 50, 0, 0, Color.red,"paddle")) #left padde
boxList.append(Box(SCREEN_WIDTH-20, paddleDefault, 10, 50, 0, 0, Color.blue,"paddle")) #right paddle

#Assigning Box objects to their proper names
pongBall = boxList[0]
redPaddle = boxList[1]
bluePaddle = boxList[2]

while(True):
    screen.fill(Color.black)
    pygame.draw.line(screen, Color.white, (SCREEN_WIDTH/2-1,0),(SCREEN_WIDTH/2-1,SCREEN_HEIGHT),2)
    keyboard = pygame.key.get_pressed()
    scoreSound = pygame.mixer.Sound("scoreSound.ogg")
    
    #red up and down
    if(keyboard[pygame.K_w]):
        redPaddle.y -=4
    if(keyboard[pygame.K_s]):
        redPaddle.y +=4
    
    #blue up and down
    if(keyboard[pygame.K_o]):
        bluePaddle.y -=4
    if(keyboard[pygame.K_l]):
        bluePaddle.y +=4
    
    #score board
    score = False
    if (pongBall.x <= 5):
        blueScore += 1
        score = True
    elif (pongBall.x >= (SCREEN_WIDTH-15) ):
        redScore += 1
        score = True
        
    #resets if there is a score
    if score == True:
        scoreSound.play()
        pongBall.x = xDefault
        pongBall.y = yDefault
        pongBall.vx = random.randint(2,4)*((-1)**random.randint(0,1))
        pongBall.vy = random.randint(2,4)*((-1)**random.randint(0,1))
        redPaddle.y = paddleDefault
        bluePaddle.y = paddleDefault
    
    #prints score
    redlabel = scoreBoard.render(str(redScore), 1, Color.red)
    bluelabel = scoreBoard.render(str(blueScore), 1, Color.blue)
    screen.blit(redlabel, (100, 0))
    screen.blit(bluelabel, (300, 0))
    
    #checks for winner, prints winner, and stops ball movement.
    if (blueScore == maxScore) or (redScore == maxScore):
        winner = ""
        if blueScore == maxScore:
            winner ="Blue"
        elif redScore == maxScore:
            winner ="Red"
        winLabel = scoreBoard.render(winner+" Wins!", 1, Color.white)
        screen.blit(winLabel, (SCREEN_WIDTH/2-70, SCREEN_HEIGHT/2))
        pongBall.x = xDefault
        pongBall.y = yDefault
        pongBall.vx = 0
        pongBall.vy = 0
        
    #updates for ball and box
    for i in range(0,3):
        boxList[i].update(screen, SCREEN_WIDTH, SCREEN_HEIGHT,boxList)
        
    msElapsed = clock.tick(30) #SYNC RATE 30 FPS

    pygame.display.update() #SYNC 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();