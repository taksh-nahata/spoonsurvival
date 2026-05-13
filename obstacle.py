import pygame
import random
import math

class Obstacle(pygame.sprite.Sprite):
        
    def __init__(self, squareSize, location, color, speed, direction, maxLoc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(squareSize)
        if(color == "random"):
          color = self.getRandomColor()
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.speed = speed
        self.direction = math.radians(direction)
        self.maxX = maxLoc[0]
        self.maxY = maxLoc[1]
        
    def update(self):
        if(self.speed > 0):
          self.rect.y += self.speed * math.sin(self.direction)
          self.rect.x += self.speed * math.cos(self.direction)
          if(self.rect.left > self.maxX):
            #self.resetLoc("right")
            self.bounce()
          elif(self.rect.right < 0):
            #self.resetLoc("left")
            self.bounce()
          elif(self.rect.bottom < 0):
            #self.resetLoc("top")
            self.bounce()
          elif(self.rect.top > self.maxY):
            #self.resetLoc("bottom")
            self.bounce()
          
    def resetLoc(self, dir):
        self.rect.y = 0  
        self.rect.x = self.maxX * random.random()
        self.direction = math.radians(random.random()*360)
        if(dir == "top"):
          self.rect.y = self.maxY

    def bounce(self):
        self.direction = (self.direction + math.pi) % (2*math.pi)
    
    def getRandomColor(self):
        return random.choice(list(pygame.color.THECOLORS.items()))[0]
    