import pygame
import random
import math
import os

class Butterfly(pygame.sprite.Sprite):
    def __init__(self, x, centerY, butterflyColor):
      pygame.sprite.Sprite.__init__(self)
      imageDir = os.path.join(os.path.dirname(__file__),"images")
      self.butterflyColor = butterflyColor
      if butterflyColor == "brown":
        self.image = pygame.image.load(os.path.join(imageDir, "brownbutterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      elif butterflyColor == "yellow":
        self.image = pygame.image.load(os.path.join(imageDir, "yellowbutterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      elif butterflyColor == "orange":
        self.image = pygame.image.load(os.path.join(imageDir, "orangebutterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      elif butterflyColor == "royalBlue":
        self.image = pygame.image.load(os.path.join(imageDir, "bluebutterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      elif butterflyColor == "purple":
        self.image = pygame.image.load(os.path.join(imageDir, "purplebutterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      else:
        self.image = pygame.image.load(os.path.join(imageDir, "goldbutterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      self.image = pygame.transform.scale_by(self.image, 0.5)
      self.rect = self.image.get_rect()
      self.mask = pygame.mask.from_surface(self.image)
      self.x = float(x)
      self.centerY = float(centerY)
      self.amplitude = 50
      self.frequency = 0.05
      self.speed = 2
    def update(self):
      self.x += self.speed
      waveY = self.centerY + (self.amplitude * math.sin(self.x * self.frequency))
      self.rect.x = int(self.x)
      self.rect.y = int(waveY)