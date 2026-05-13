import pygame
import os
import random
import math

class Spoon(pygame.sprite.Sprite):
    def __init__(self, location, screenSize, speed):
      imageDir = os.path.join(os.path.dirname(__file__),"images")
      pygame.sprite.Sprite.__init__(self)
      self.originalImage = pygame.image.load(os.path.join(imageDir, "spoon.png")).convert()
      self.originalImage.set_colorkey(pygame.Color("black"))
      self.image = self.originalImage
      self.rect = self.image.get_rect(center=location)
      self.mask = pygame.mask.from_surface(self.image)
      self.angle = 0
      self.state = "IDLE"
      self.stageTimer = 0
      self.targetX = 0
      self.rect.center = location
      self.maxX = screenSize[0]
      self.maxY = screenSize[1]
      self.speedX = speed[0]
      self.speedY = speed[1]
      self.score = 0
      self.difficultyLevel = "EASY"

    def update(self, playerPosition):
      self.stageTimer += 1
      if self.stageTimer <= 690:
        self.difficultyLevel = "EASY"
      elif self.stageTimer >= 691 and self.stageTimer <= 1590:
        self.difficultyLevel = "MEDIUM"
      elif self.stageTimer >= 1591:
        self.difficultyLevel = "HARD"
      if self.difficultyLevel == "EASY":
        if self.state == "IDLE":
          self.rect.y = -150
          if self.stageTimer %90 == 0:
            self.state = "STALK"
        elif self.state == "STALK":
          self.rect.y = 20
          if self.rect.centerx < playerPosition[0]:
            self.rect.x += self.speedX
            self.angle = -15
          if self.rect.centerx > playerPosition[0]:
            self.rect.x -= self.speedX
            self.angle = 15
          if self.stageTimer % 150 == 0:
            self.targetY = playerPosition[1]
            self.state = "JAB"
        elif self.state == "JAB":
          self.angle += 10
          self.rect.y +=self.speedX *2
          if self.rect.y >= self.targetY or self.rect.bottom >= self.maxY:
            self.state = "RETREAT"
        elif self.state == "RETREAT":
          self.rect.y -= self.speedY
          self.angle = 0
          if self.rect.bottom <= 0:
            self.state = "IDLE"
      elif self.difficultyLevel == "MEDIUM":
        if self.state == "IDLE":
          self.rect.y = -150
          if self.stageTimer %90 == 0:
            self.state = "STALK"
        elif self.state == "STALK":
          self.rect.y = 20
          if self.rect.centerx < playerPosition[0]:
            self.rect.x += self.speedX
            self.angle = -15
          if self.rect.centerx > playerPosition[0]:
            self.rect.x -= self.speedX
            self.angle = 15
          if self.stageTimer % 150 == 0:
            self.targetX = playerPosition[0]
            self.targetY = playerPosition[1]
            self.state = "JAB"
        elif self.state == "JAB":
          self.angle += 10
          self.rect.y +=self.speedY *2
          if self.rect.y >= self.targetY or self.rect.bottom >= self.maxY:
            self.state = "PAUSE"
            self.pauseTimer = 0
            self.baseX = self.rect.centerx
            self.baseY = self.rect.centery
        elif self.state == "PAUSE":
          self.pauseTimer += 1

          self.rect.centerx = self.baseX + random.randint(-4,4)
          self.rect.centery = self.baseY + random.randint(-4,4)

          if self.pauseTimer >= 20:
            self.rect.centerx = self.baseX
            self.rect.centery = self.baseY
            startVector = pygame.Vector2(self.rect.center)
            targetVector = pygame.Vector2(playerPosition[0],playerPosition[1])
            if startVector != targetVector:
              self.dash = (targetVector - startVector).normalize() *(self.speedY*3.5)
            else:
              self.dash = pygame.Vector2(0,self.speedY*3.5)
            self.state = "JAB2"
        elif self.state == "JAB2":
          self.angle += 20
          self.rect.centerx += int(self.dash.x)
          self.rect.centery += int(self.dash.y)
          if self.rect.top >= self.maxY or self.rect.bottom <= 0 or self.rect.right <= 0 or self.rect.left >= self.maxX:
            self.state = "RETREAT"
        elif self.state == "RETREAT":
          self.rect.y -= self.speedY
          self.angle = 0
          if self.rect.bottom <= 0:
            self.state = "IDLE"
      originalCenter = self.rect.center
      self.image = pygame.transform.rotate(self.originalImage, self.angle)
      self.rect = self.image.get_rect(center=originalCenter)
      self.mask = pygame.mask.from_surface(self.image)
      self.score = self.stageTimer // 30
      