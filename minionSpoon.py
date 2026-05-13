import pygame
import os
import random
import math

class MinionSpoon(pygame.sprite.Sprite):
    def __init__(self, location, screenSize, speed):
      imageDir = os.path.join(os.path.dirname(__file__),"images")
      pygame.sprite.Sprite.__init__(self)
      self.originalImage = pygame.image.load(os.path.join(imageDir, "spoon.png")).convert()
      self.originalImage.set_colorkey(pygame.Color("black"))
      self.originalImage = pygame.transform.scale_by(self.originalImage, 0.5)
      self.image = self.originalImage
      self.rect = self.image.get_rect(center=location)
      self.mask = pygame.mask.from_surface(self.image)
      self.angle = 0
      self.stageTimer = 0
      self.state = "NOTNEEDED"
      self.targetX = 0
      self.rect.center = location
      self.maxX = screenSize[0]
      self.maxY = screenSize[1]
      self.speedX = speed[0]
      self.speedY = speed[1]

    def update(self, playerPosition):
      
      originalCenter = self.rect.center
      self.image = pygame.transform.rotate(self.originalImage, self.angle)
      self.rect = self.image.get_rect(center=originalCenter)
      self.mask = pygame.mask.from_surface(self.image)
      self.score = self.stageTimer // 30
      