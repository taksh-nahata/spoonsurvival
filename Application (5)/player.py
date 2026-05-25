import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, location, screenSize, speed):
      imageDir = os.path.join(os.path.dirname(__file__),"images")
      soundDir = os.path.join(os.path.dirname(__file__),"sounds")
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load(os.path.join(imageDir, "dragonfly.png")).convert()
      self.eatSound = pygame.mixer.Sound(os.path.join(soundDir,"crunch.wav"))
      self.deathSound = pygame.mixer.Sound(os.path.join(soundDir,"death.wav"))
      width, height = self.image.get_size()
      self.image = pygame.transform.scale_by(self.image, (screenSize[0]*0.15)/width)
      self.image.set_colorkey(pygame.Color("black"))
      self.rect = self.image.get_rect()
      self.mask = pygame.mask.from_surface(self.image)
      self.rect.center = location
      self.maxX = screenSize[0]
      self.maxY = screenSize[1]
      self.collectedButterfliesList = []
      self.speedX = speed[0]
      self.speedY = speed[1]
      self.velocityX = 0
      self.velocityY = 0
      self.rarestButterfly = ""
      self.indestructible = False
      self.indestructibleTimer = 0
      self.cooldownTimer = 0
      self.allowIndestructible = True

    def update(self, directions, buttons, enemies, collectibles):
      imageDir = os.path.join(os.path.dirname(__file__),"images")
      self.velocityX = 0
      self.velocityY = 0

      keystate = pygame.key.get_pressed()
      if keystate[pygame.K_a] or keystate[pygame.K_LEFT] or "LEFT" in directions:
        self.velocityX = -1 * self.speedX
      if keystate[pygame.K_d] or keystate[pygame.K_RIGHT] or "RIGHT" in directions:
        self.velocityX = self.speedX
      if keystate[pygame.K_w] or keystate[pygame.K_UP] or "UP" in directions:
        self.velocityY = -1 * self.speedY
      if keystate[pygame.K_s] or keystate[pygame.K_DOWN] or "DOWN" in directions:
        self.velocityY = self.speedY
        
      if self.allowIndestructible:
        if keystate[pygame.K_h] or 3 in buttons:
          self.indestructible = True

      #Make them indes for 45 frames, once that expires start the cooldown 
      if self.indestructible == True:
        self.indestructibleTimer += 1
        if self.indestructibleTimer % 45 == 0:
          self.indestructibleTimer = 0
          self.indestructible = False
          self.allowIndestructible = False
          
      if self.indestructible == True:
        originalCenter = self.rect.center
        self.image = pygame.image.load(os.path.join(imageDir, "dragonflyInvincible.png")).convert()
        width, height = self.image.get_size()
        self.image = pygame.transform.scale_by(self.image, (self.maxX*0.15)/width)
        self.image.set_colorkey(pygame.Color("black"))
        self.rect = self.image.get_rect(center=originalCenter)
        self.mask = pygame.mask.from_surface(self.image)
      else:
        originalCenter = self.rect.center
        self.image = pygame.image.load(os.path.join(imageDir, "dragonfly.png")).convert()
        width, height = self.image.get_size()
        self.image = pygame.transform.scale_by(self.image, (self.maxX*0.15)/width)
        self.image.set_colorkey(pygame.Color("black"))
        self.rect = self.image.get_rect(center=originalCenter)
        self.mask = pygame.mask.from_surface(self.image)
      
      if self.allowIndestructible == False:
        self.cooldownTimer += 1
        if self.cooldownTimer > 450:
          self.allowIndestructible = True
          self.cooldownTimer = 0

          
      self.rect.x += self.velocityX
      hits = self.collisionDetectionEnemies(enemies)
      if not self.indestructible:
        if hits:
          self.deathSound.play()
          return True
      collectiblesHits = self.collisionDetectionCollectibles(collectibles)
      if collectiblesHits:
        self.eatSound.play()
        for collectible in collectiblesHits:
          self.collectedButterfliesList.append(collectible.butterflyColor)
          self.updateRarestButterfly(collectible.butterflyColor)
          collectible.kill()
      
      self.rect.y += self.velocityY
      hits = self.collisionDetectionEnemies(enemies)
      if not self.indestructible:
        if hits:
          self.deathSound.play()
          return True
      
      collectiblesHits = self.collisionDetectionCollectibles(collectibles)
      if collectiblesHits:
        self.eatSound.play()
        for collectible in collectiblesHits:
          self.collectedButterfliesList.append(collectible.butterflyColor)
          self.updateRarestButterfly(collectible.butterflyColor)
          collectible.kill()
        
      self.checkScreenBounds()


    def collisionDetectionEnemies(self, enemies):
      hits = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_mask)
      return hits
      
    def collisionDetectionCollectibles(self,collectibles):
      collectiblesHits = pygame.sprite.spritecollide(self,collectibles,False, pygame.sprite.collide_mask)
      return collectiblesHits

    def updateRarestButterfly(self, butterfly):
      butterflyScores = {
        "gold": 7,
        "bloodRed": 6,
        "purple": 5,
        "royalBlue": 4,
        "orange": 3,
        "yellow": 2,
        "brown": 1,
        "": 0
      }
      newButterflyScore = butterflyScores.get(butterfly,0)
      currentScore = butterflyScores.get(self.rarestButterfly, 0)

      if newButterflyScore > currentScore:
        self.rarestButterfly = butterfly
    def checkScreenBounds(self):
      #Comment out for #6
      #Should comment from here 
      if(self.rect.right > self.maxX):
          self.rect.right = self.maxX
      if(self.rect.left < 0):
          self.rect.left = 0
      #To here
      
      if(self.rect.bottom > self.maxY):
          self.rect.bottom = self.maxY
      if(self.rect.top < 0):
          self.rect.top = 0