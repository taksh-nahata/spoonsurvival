import os
import pygame
import random
import math

from player import Player
from spoon import Spoon
from uiElements import UIElement
from butterfly import Butterfly
from JoystickInterface import JoystickInterface
from minionSpoon import MinionSpoon
class ScrollingMap:
    def __init__(self):
        width = 400
        height = 500
        self.targetFrames = 30
        self.gameOver = False
        self.gameTimer = 0
        self.setup(width, height)   
        self.additionalScore = 0
    #1
    def loadBackground(self):
        #1
        imageDir = os.path.join(os.path.dirname(__file__),"images")
        self.background = pygame.image.load(os.path.join(imageDir, "bg.jpeg")).convert()
      
        self.backgroundLoc = (0, 0)

    #2 
    def loadBackgroundScaled(self):
        self.loadBackground()
        #2
        if(self.background.get_size()[0] < self.screen.get_size()[0] or self.background.get_size()[1] < self.screen.get_size()[1]):
          scaleX = self.screen.get_size()[0] / self.background.get_size()[0]
          scaleY = self.screen.get_size()[1] / self.background.get_size()[1]

          scaleAll = scaleX
          if scaleY > scaleX:
            scaleAll = scaleY
            
          self.background = pygame.transform.scale_by(self.background, scaleAll)

    #3
    def setupScrolling(self):
        self.backgroundTiles = math.ceil(self.screen.get_size()[0] / self.background.get_size()[0]) + 1
        self.scroll = 0


    def setupPlayerAndObstacles(self):
        myX = self.screen.get_size()[0]/2
        myY = self.screen.get_size()[1]/2
        mySpeedX = 10
        mySpeedY = 10
        self.player = Player((myX,myY), self.screen.get_size(), (mySpeedX, mySpeedY))
        self.movingSprites.add(self.player)
        self.allSprites.add(self.player)
        self.spoon = Spoon((130,50), self.screen.get_size(), (5, 5))
        self.allSprites.add(self.spoon)
        self.enemies.add(self.spoon)
    
    def setupUI(self):
      score = self.spoon.score
      rarestButterfly = self.player.rarestButterfly
      difficultyLevel = self.spoon.difficultyLevel
      #location,size,color,text,textSize,textColor
      uiLocH = (0,0)
      uiSize = (400,50)
      uiColor = "black"
      uiText = f"Score: {score} | Rarest Butterfly: {rarestButterfly} | Difficulty Level: {difficultyLevel}"
      uiTextSize = 14
      uiTextColor = "white"
      self.scoreUI = UIElement(uiLocH, uiSize, uiColor, uiText, uiTextSize, uiTextColor)
      self.scoreUI.rect.x=0
      self.scoreUI.rect.y=0
      self.allSprites.add(self.scoreUI)

      
    def setup(self, width, height):
        pygame.init()
        pygame.mixer.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count != 0:
          self.myJoysticks = []
          for stick in range(joystick_count):
            my_joystick = pygame.joystick.Joystick(stick)
            my_joystick.init()
            self.myJoysticks.append(JoystickInterface(my_joystick))
        self.buttons = []
        self.directions = []
      
        self.screen = pygame.display.set_mode((width, height))
        #self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption("Spoon Survival")

        #Set up background
        #2
        self.loadBackgroundScaled()
        #3
        self.setupScrolling()
      
        self.clock = pygame.time.Clock()
        self.running = True
        self.allSprites = pygame.sprite.Group()
        self.movingSprites = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.setupPlayerAndObstacles()
        self.setupUI()
      
    def events(self):
        #process inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        joystick_count = pygame.joystick.get_count()
        if joystick_count != 0:
          self.buttons = self.myJoysticks[0].getButtonsPressed()
          self.directions = self.myJoysticks[0].getJoystickDirections()
          if 9 in self.buttons:
            self.running = False

    #5
    def scrollAtEdge(self):
        #5
        distFromRightEdge = (abs(self.screen.get_size()[0] - self.player.rect.x))
        distFromLeftEdge = (abs(self.player.rect.x))
        if distFromRightEdge < self.player.rect.width + 128 and self.player.velocityX > 0:
            self.scroll -= self.player.velocityX +10
        elif distFromLeftEdge < self.player.rect.width and self.player.velocityX < 0:
            self.scroll -= self.player.velocityX -10
        if abs(self.scroll) > self.background.get_size()[0]:
            self.scroll = 0
          
    def createCollectibles(self,difficultyLevel,gameTimer):
        if difficultyLevel == "EASY":
          if gameTimer % 345 == 0:
            colors = ["brown", "yellow","orange","royalBlue","purple","bloodRed","gold"]
            butterflyColor = random.choices(colors, cum_weights=[75,83,90,96,99,99.9,100])
            centerY = random.randint(65,280)
            self.butterfly = Butterfly(0,centerY,*butterflyColor)
            self.collectibles.add(self.butterfly)
            self.allSprites.add(self.butterfly)
        if difficultyLevel == "MEDIUM":
          if gameTimer % 210 == 0:
            colors = ["brown", "yellow","orange","royalBlue","purple","bloodRed","gold"]
            butterflyColor = random.choices(colors, cum_weights=[35,70,85,94,98,99.6,100])
            centerY = random.randint(65,280)
            self.butterfly = Butterfly(0,centerY,*butterflyColor)
            self.collectibles.add(self.butterfly)
            self.allSprites.add(self.butterfly)

#    def createMinions(self):
      
            
    def update(self):
        self.clock.tick(self.targetFrames)
        difficultyLevel = self.spoon.difficultyLevel
        self.gameTimer += 1

        if(not self.gameOver):
          self.createCollectibles(difficultyLevel,self.gameTimer)
          self.collectibles.update()
          self.spoon.update(self.player.rect.center)
          self.scoreUI.changeText(f"Score: {self.spoon.score} | Rarest Butterfly: {self.player.rarestButterfly} | Difficulty Level: {self.spoon.difficultyLevel}")
          self.scoreUI.update()
          self.gameOver = self.player.update(self.directions, self.buttons, self.enemies, self.collectibles)
          self.scrollAtEdge()
    
    #3
    def drawBackgroundScrolling(self):
        #3
        for lcv in range(-1, self.backgroundTiles):
            curX = lcv * self.background.get_size()[0] + self.scroll
            curY = 0
            self.screen.blit(self.background, (curX, curY))

    def drawThankYouScreen(self):
      colorSurface = pygame.Surface((400,500))
      colorSurface.fill((255,255,255))
      for butterfly in self.player.collectedButterfliesList:
        if butterfly == "brown":
          self.additionalScore += 3
        if butterfly == "yellow":
          self.additionalScore += 5
        if butterfly == "orange":
          self.additionalScore += 8
        if butterfly == "royalBlue":
          self.additionalScore += 15
        if butterfly == "purple":
          self.additionalScore += 35
        if butterfly == "gold":
          self.additionalScore += 200
      self.player.collectedButterfliesList = []
      myFont = pygame.font.SysFont("Arial", 32)
      textSurface1 = myFont.render(f"Raw Score: {self.spoon.score}", True, (0,0,0))
      textSurface2 = myFont.render(f"Additional Score: {self.additionalScore}", True, (0,0,0))
      textSurface3 = myFont.render(f"Total Score: {self.spoon.score + self.additionalScore}", True, (0,0,0))
      textSurface4 = myFont.render(f"Rarest Butterfly: {self.player.rarestButterfly}", True, (0,0,0))
      textSurface5 = myFont.render("Click 'y' to play again.", True, (0,0,0))
      textSurface6 = myFont.render("Click 'n' to exit.", True, (0,0,0))
      textRect1 = textSurface1.get_rect(center=(200,100))
      textRect2 = textSurface2.get_rect(center=(200,150))
      textRect3 = textSurface3.get_rect(center=(200,200))
      textRect4 = textSurface4.get_rect(center=(200,250))
      textRect5 = textSurface5.get_rect(center=(200,300))
      textRect6 = textSurface6.get_rect(center=(200,350))
      self.screen.blit(colorSurface, (0,0))
      self.screen.blit(textSurface1, textRect1)
      self.screen.blit(textSurface2,textRect2)
      self.screen.blit(textSurface3, textRect3)
      self.screen.blit(textSurface4,textRect4)
      self.screen.blit(textSurface5, textRect5)
      self.screen.blit(textSurface6,textRect6)

    def drawStartScreen(self):
      colorSurface = pygame.Surface((400,500))
      colorSurface.fill((255,255,255))
      myFont = pygame.font.SysFont("Arial", 32)
      textSurface = myFont.render("WELCOME TO SPOON SURVIVAL", True, (0,0,0))
      textSurface2 = myFont.render("Game Instructions", True, (0,0,0))
      textSurface3 = myFont.render("Use the Joystick or WASD to move around", True, (0,0,0))
      textSurface4 = myFont.render("Goal: Dodge the spoon for as long as possible", True, (0,0,0))
      textSurface5 = myFont.render("The spoon will chase you", True, (0,0,0))
      textSurface6 = myFont.render("As you go on, the game will get more difficult.", True, (0,0,0))
      textSurface7 = myFont.render("Click y or button 1 to start playing", True, (0,0,0))
      textRect = textSurface.get_rect(center=(200,100))
      textRect2 = textSurface2.get_rect(center=(200,150))
      textRect3 = textSurface3.get_rect(center=(200,200))
      textRect4 = textSurface4.get_rect(center=(200,250))
      textRect5 = textSurface5.get_rect(center=(200,300))
      textRect6 = textSurface6.get_rect(center=(200,350))
      textRect7 = textSurface7.get_rect(center=(200,400))
      self.screen.blit(colorSurface, (0,0))
      self.screen.blit(textSurface, textRect)
      self.screen.blit(textSurface2,textRect2)
      self.screen.blit(textSurface3, textRect3)
      self.screen.blit(textSurface4,textRect4)
      self.screen.blit(textSurface5, textRect5)
      self.screen.blit(textSurface6,textRect6)
      self.screen.blit(textSurface7,textRect7)

  
    def draw(self):
        if not self.gameOver:
          self.drawBackgroundScrolling()
          self.allSprites.draw(self.screen)

        else:
          self.drawThankYouScreen()
          keystate = pygame.key.get_pressed()
          if keystate[pygame.K_y]:
            self.gameOver = False
            self.running  =  True
            main()
          if keystate[pygame.K_n]:
            self.running = False
        
        pygame.display.flip()
        
    def shutdown(self):
        pygame.quit()
        
def main():
    myGame = ScrollingMap()
    
    while(myGame.running):
        myGame.events()
        myGame.update()
        myGame.draw()
        
    myGame.shutdown()
    
main()