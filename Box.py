'''
Created on Feb 6, 2015

@author: SIU853541579
'''
import pygame
import random

class Box():

    def __init__(self, x, y, width, height, vx, vy, color,boxType):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.color = color
        self.boxType = boxType #boxType is to tell if it is the pong or a paddle

    def moveIt(self):
        self.x += self.vx
        self.y += self.vy
        
    def checkBoundHit(self, s_wd, s_ht):
        result = [0,0]
        if(self.x <= 0):
            result[0] = -1
        elif(self.x+self.width >= s_wd):
            result[0] = 1
        
        if(self.y <= 0):
            result[1] = -1
        elif(self.y + self.height >= s_ht):
            result[1] = 1
        return result
    
    def handleBoundHit(self, hitDir, s_width, s_height):
        wallSound = pygame.mixer.Sound("wallSound.ogg")
        if(hitDir[0] == -1):
            self.x = 1 
            self.vx *= -1
        elif(hitDir[0] == 1):
            self.x = s_width - self.width - 1
            self.vx *= -1
        
        if(hitDir[1] == -1):
            wallSound.play()
            self.y = 1
            self.vy *= -1
        elif(hitDir[1] == 1):
            wallSound.play()
            self.y = s_height - self.height - 1
            self.vy *= -1
            
    def toRect(self):
        return (self.x, self.y, self.width, self.height)
    
    def drawIt(self, drawDest):
        pygame.draw.rect(drawDest, self.color, self.toRect())
        
        
    def checkBoxCollision(self, other):
        #min1--------------min1
        #   min2--------------max2
        if(self.x <= (other.x + other.width)) and (other.x <= (self.x + self.width)):
            if(self.y <= (other.y + other.height)) and (other.y <= (self.y + self.height)):
                return True
            else:
                return False
        else:
            return False
        
    def getHitDirection(self, other):
        result = [0,0]
        #everything is from self's perspective
        dTop = abs(self.y - (other.y + other.height))
        dBot = abs((self.y + self.height) - other.y)
        dRight = abs((self.x + self.width) - other.x)
        dLeft = abs(self.x - (other.x + other.width))
        
        if((dTop <= dRight) and (dTop <= dLeft) and (dTop < dBot)):
            #top
            #check for corner collision
            if(dTop == dRight): #right corner collision
                result[0] = 1 
            elif(dTop == dLeft): #left corner collision
                result[0] = -1
            result[1] = -1
        elif((dBot <= dRight) and (dBot <= dLeft)):
            #bottom
            if(dBot == dRight): #right corner collision
                result[0] = 1 
            elif(dBot == dLeft): #left corner collision
                result[0] = -1
            result[1] = 1
        elif(dRight < dLeft):
            #right
            result[0] = 1
        else:
            #left
            result[0] = -1
        return result
    
    #You would reduce HP here too.
    def handleBoxHit(self, other, direction):
        #made the acceleration of the ball 5% only after it this a paddle
        accel = 1.05
        paddleSound = pygame.mixer.Sound("paddleSound.ogg")
        paddleSound.play()
        if(direction[0] == -1):
            self.x = other.x + other.width
            self.vx *= -accel
        elif(direction[0] == 1):
            self.x = other.x - self.width
            self.vx *= -accel
            
        if(direction[1] == -1):
            self.y = other.y + other.height
            self.vy *= -accel
        elif(direction[1] == 1):
            self.y = other.y - self.height
            self.vy *= -accel
        #self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) #just add this to Colors
        
    def runBoxCollision(self, other):
        dir = [0,0]
        #only runs box collision for pong vs paddle, no paddle vs paddle
        if(self.boxType=="pong"):
            if(self.checkBoxCollision(other)):
                dir = self.getHitDirection(other)
                self.handleBoxHit(other, dir)
    
    def update(self, drawDest, s_width, s_height, boxList):
        self.moveIt()
        for otherBox in boxList:
            if(self != otherBox):
                self.runBoxCollision(otherBox)
        self.handleBoundHit(self.checkBoundHit(s_width, s_height), s_width, s_height)
        self.drawIt(drawDest)