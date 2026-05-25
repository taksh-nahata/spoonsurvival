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
        self.gameStart = False
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
        width, height = self.screen.get_size()
        myX = self.screen.get_size()[0]/2
        myY = self.screen.get_size()[1]/2
        mySpeedX = width*0.025
        mySpeedY = height *0.02
        self.player = Player((myX,myY), self.screen.get_size(), (mySpeedX, mySpeedY))
        self.movingSprites.add(self.player)
        self.allSprites.add(self.player)
        self.spoon = Spoon((self.screen.get_size()[0] *0.325,self.screen.get_size()[1]*0.1), self.screen.get_size(), (width*0.0125, height*0.01))
        self.allSprites.add(self.spoon)
        self.enemies.add(self.spoon)
    
    def setupUI(self):
      score = self.spoon.score
      rarestButterfly = self.player.rarestButterfly
      difficultyLevel = self.spoon.difficultyLevel
      #location,size,color,text,textSize,textColor
      uiLocH = (0,0)
      uiSize = (self.screen.get_width(),50)
      uiColor = "black"
      uiText = f"Score: {score} | Rar Butterfly: {rarestButterfly} | Level: {difficultyLevel}"
      uiTextSize = int(self.screen.get_width() *0.025)
      uiTextColor = "white"
      self.scoreUI = UIElement(uiLocH, uiSize, uiColor, uiText, uiTextSize, uiTextColor)
      self.scoreUI.rect.x=0
      self.scoreUI.rect.y=0
      self.allSprites.add(self.scoreUI)

      
    def setup(self, width, height):
        pygame.mixer.pre_init(44100,-16,1,512)
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
          self.directions = self.myJoysticks[0].getJoystickDirection()
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
            centerY = random.randint(int(self.screen.get_size()[1] *0.13),int(self.screen.get_size()[1]*0.56))
            self.butterfly = Butterfly(0,centerY,*butterflyColor, self.screen.get_size())
            self.collectibles.add(self.butterfly)
            self.allSprites.add(self.butterfly)
        if difficultyLevel == "MEDIUM":
          if gameTimer % 210 == 0:
            colors = ["brown", "yellow","orange","royalBlue","purple","bloodRed","gold"]
            butterflyColor = random.choices(colors, cum_weights=[35,70,85,94,98,99.6,100])
            centerY = random.randint(int(self.screen.get_size()[1] *0.13),int(self.screen.get_size()[1]*0.56))
            self.butterfly = Butterfly(0,centerY,*butterflyColor, self.screen.get_size())
            self.collectibles.add(self.butterfly)
            self.allSprites.add(self.butterfly)
        if difficultyLevel == "HARD":
          if gameTimer % 150 == 0:
            colors = ["brown", "yellow","orange","royalBlue","purple","bloodRed","gold"]
            butterflyColor = random.choices(colors, cum_weights=[20,45,65,80,90,96,100])
            centerY = random.randint(int(self.screen.get_size()[1] *0.13),int(self.screen.get_size()[1]*0.56))
            self.butterfly = Butterfly(0,centerY,*butterflyColor, self.screen.get_size())
            self.collectibles.add(self.butterfly)
            self.allSprites.add(self.butterfly)

    def createMinions(self, difficultyLevel, gameTimer):
      if difficultyLevel == "HARD":
        if gameTimer % 90 == 0:
          width = self.screen.get_size()[0]
          height = self.screen.get_size()[1]
          side = random.choice(["left","right"])
          if side == "left":
            startX = random.randint(-50,0)
            startY = random.randint(-50,int(height*0.3))
            speed = (random.randint(5,10), random.randint(5,10))
          if side == "right":
            startX = random.randint(width,width+50)
            startY = random.randint(-50,int(height*0.3))
            speed = (random.randint(-10,-5), random.randint(5,10))
          minion = MinionSpoon((startX,startY), (width, height), speed)
          self.enemies.add(minion)
          self.allSprites.add(minion)
          
    def update(self):
        self.clock.tick(self.targetFrames)
        difficultyLevel = self.spoon.difficultyLevel
        self.gameTimer += 1
        if self.gameStart:
          if(not self.gameOver):
            self.createCollectibles(difficultyLevel,self.gameTimer)
            self.createMinions(difficultyLevel,self.gameTimer)
            self.collectibles.update()
            self.enemies.update(self.player.rect.center)
            self.scoreUI.changeText(f"Score: {self.spoon.score} | Rarest Butterfly: {self.player.rarestButterfly} | Level: {self.spoon.difficultyLevel} | Indestructible: {self.player.indestructible}")
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
      colorSurface = pygame.Surface(self.screen.get_size())
      midX = self.screen.get_size()[0]//2
      screenY = self.screen.get_size()[1]
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
        if butterfly == "bloodRed":
          self.additionalScore += 100
        if butterfly == "gold":
          self.additionalScore += 200
      self.player.collectedButterfliesList = []
      myFont = pygame.font.SysFont("Arial", int(self.screen.get_size()[0]*0.05))
      textSurface1 = myFont.render(f"Raw Score: {self.spoon.score}", True, (0,0,0))
      textSurface2 = myFont.render(f"Additional Score: {self.additionalScore}", True, (0,0,0))
      textSurface3 = myFont.render(f"Total Score: {self.spoon.score + self.additionalScore}", True, (0,0,0))
      textSurface4 = myFont.render(f"Rarest Butterfly: {self.player.rarestButterfly}", True, (0,0,0))
      textSurface5 = myFont.render("Click 'y' or button 1 to play again", True, (0,0,0))
      textSurface6 = myFont.render("Click 'n' or button 9  to exit.", True, (0,0,0))
      textRect1 = textSurface1.get_rect(center=(midX, screenY*0.2))
      textRect2 = textSurface2.get_rect(center=(midX, screenY*0.3))
      textRect3 = textSurface3.get_rect(center=(midX, screenY*0.4))
      textRect4 = textSurface4.get_rect(center=(midX, screenY*0.5))
      textRect5 = textSurface5.get_rect(center=(midX, screenY*0.6))
      textRect6 = textSurface6.get_rect(center=(midX, screenY*0.7))
      self.screen.blit(colorSurface, (0,0))
      self.screen.blit(textSurface1, textRect1)
      self.screen.blit(textSurface2,textRect2)
      self.screen.blit(textSurface3, textRect3)
      self.screen.blit(textSurface4,textRect4)
      self.screen.blit(textSurface5, textRect5)
      self.screen.blit(textSurface6,textRect6)

    def drawStartScreen(self):
      colorSurface = pygame.Surface(self.screen.get_size())
      midX = self.screen.get_size()[0]//2
      screenY = self.screen.get_size()[1]
      colorSurface.fill((255,255,255))
      myFont = pygame.font.SysFont("Arial", int(self.screen.get_size()[0]*0.045))
      textSurface = myFont.render("WELCOME TO SPOON SURVIVAL", True, (0,0,0))
      textSurface2 = myFont.render("Game Instructions:", True, (0,0,0))
      textSurface3 = myFont.render("Use the Joystick or WASD to move around", True, (0,0,0))
      textSurface4 = myFont.render("Use 'h' or button 1 to become invincible", True, (0,0,0))
      textSurface5 = myFont.render("Goal: Dodge the spoon for as long as possible", True, (0,0,0))
      textSurface6 = myFont.render("The spoon will chase you", True, (0,0,0))
      textSurface7 = myFont.render("As you go on, the game will get more difficult.", True, (0,0,0))
      textSurface8 = myFont.render("Click y or button 1 to start playing", True, (0,0,0))
      textRect = textSurface.get_rect(center=(midX, screenY*0.2))
      textRect2 = textSurface2.get_rect(center=(midX, screenY*0.3))
      textRect3 = textSurface3.get_rect(center=(midX, screenY*0.4))
      textRect4 = textSurface4.get_rect(center=(midX, screenY*0.5))
      textRect5 = textSurface5.get_rect(center=(midX, screenY*0.6))
      textRect6 = textSurface6.get_rect(center=(midX, screenY*0.7))
      textRect7 = textSurface7.get_rect(center=(midX, screenY*0.8))
      textRect8 = textSurface7.get_rect(center=(midX, screenY*0.9))
      self.screen.blit(colorSurface, (0,0))
      self.screen.blit(textSurface, textRect)
      self.screen.blit(textSurface2,textRect2)
      self.screen.blit(textSurface3, textRect3)
      self.screen.blit(textSurface4,textRect4)
      self.screen.blit(textSurface5, textRect5)
      self.screen.blit(textSurface6,textRect6)
      self.screen.blit(textSurface7,textRect7)
      self.screen.blit(textSurface8,textRect8)
    def reset(self):
      self.gameOver = False
      self.gameTimer = 0
      self.additionalScore = 0
      self.scroll = 0
      self.allSprites.empty()
      self.movingSprites.empty()
      self.collectibles.empty()
      self.enemies.empty()
      self.setupPlayerAndObstacles()
      self.setupUI()
    for i in range(3):
      for j in range(3):
        if i in rang
    def draw(self):
      if not self.gameStart:
        self.drawStartScreen()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_y] or 3 in self.buttons:
          self.gameStart = True
      else:
        if not self.gameOver:
          self.drawBackgroundScrolling()
          self.allSprites.draw(self.screen)

        else:
          self.drawThankYouScreen()
          keystate = pygame.key.get_pressed()
          if keystate[pygame.K_y] or 3 in self.buttons:
            self.reset()
          if keystate[pygame.K_n] or 9 in self.buttons:
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