import pygame
import random
import math
import os

class Butterfly(pygame.sprite.Sprite):
    def __init__(self, x, centerY, butterflyColor, screenSize):
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
      elif butterflyColor == "bloodRed":
        self.image = pygame.image.load(os.path.join(imageDir, "bloodRedButterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      else:
        self.image = pygame.image.load(os.path.join(imageDir, "goldbutterfly.png")).convert()
        self.image.set_colorkey(pygame.Color("black"))
      width, height = self.image.get_size()
      self.image = pygame.transform.scale_by(self.image, (screenSize[0]*0.15)/width)
      self.rect = self.image.get_rect()
      self.mask = pygame.mask.from_surface(self.image)
      self.x = float(x)
      self.centerY = float(centerY)
      self.amplitude = screenSize[1]*0.1
      self.frequency = 0.05
      self.speed = screenSize[0]*0.005
    def update(self):
      self.x += self.speed
      waveY = self.centerY + (self.amplitude * math.sin(self.x * self.frequency))
      self.rect.x = int(self.x)
      self.rect.y = int(waveY)

      if self.rect.x > 2000:
          self.kill()