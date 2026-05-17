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
      self.originalImage = pygame.transform.scale_by(self.originalImage, 0.3)
      self.image = self.originalImage
      self.rect = self.image.get_rect(center=location)
      self.mask = pygame.mask.from_surface(self.image)
      self.maxX = screenSize[0]
      self.maxY = screenSize[1]
      self.speedX = speed[0]
      self.speedY = speed[1]
      if self.speedX > 0:
        self.angle = 135
      else:
        self.angle = 225
      self.image = pygame.transform.rotate(self.originalImage, self.angle)
      self.rect = self.image.get_rect(center=self.rect.center)
      self.mask = pygame.mask.from_surface(self.image)

    def update(self, playerPosition):
      self.rect.x += self.speedX
      self.rect.y += self.speedY
      if self.rect.top > (self.maxY+200) or self.rect.bottom<-200 or self.rect.right <-200 or self.rect.left > (self.maxX+200):
        self.kill()