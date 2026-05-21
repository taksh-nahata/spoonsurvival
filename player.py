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
      if keystate[pygame.K_h] or 1 in buttons:
        self.indestructible = True
      if self.indestructible == True:
        self.indestructibleTimer += 1
        if self.indestructibleTimer % 90 == 0:
          self.indestructibleTimer = 0
          self.indestructible = False
      
      self.rect.x += self.velocityX
      hits = self.collisionDetectionEnemies(enemies)
      if not self.indestructible:
        if hits:
          self.deathSound.play()
          return True
      collectiblesHits = self.collisionDetectionCollectibles(collectibles)
      for collectible in collectiblesHits:
        self.collectedButterfliesList.append(collectible.butterflyColor)
        for butterfly in self.collectedButterfliesList:
          if butterfly == "gold":
            self.rarestButterfly = butterfly
          else:
            if butterfly == "bloodRed":
              self.rarestButterfly = butterfly
            else:
              if butterfly == "purple":
                self.rarestButterfly = butterfly
              else:
                if butterfly == "royalBlue":
                  self.rarestButterfly = butterfly
                else:
                  self.rarestButterfly = butterfly
                  if butterfly == "orange":
                    self.rarestButterfly = butterfly
                  else:
                    if butterfly == "yellow":
                      self.rarestButterfly = butterfly
                    else:
                      if butterfly == "brown":
                        self.rarestButterfly = butterfly
        collectible.kill()
        self.eatSound.play()
        continue
      
      #self.collisionResponse(enemies, hits, "x")
      
      
      self.rect.y += self.velocityY
      hits = self.collisionDetectionEnemies(enemies)
      if not self.indestructible:
        if hits:
          return True
      
      collectiblesHits = self.collisionDetectionCollectibles(collectibles)
      for collectible in collectiblesHits:
        self.collectedButterfliesList.append(collectible.butterflyColor)
        self.rarestButterfly = collectible.butterflyColor
        collectible.kill()
        continue
      #self.collisionResponse(enemies, hits, "y")

      self.checkScreenBounds()


    def collisionDetectionEnemies(self, enemies):
      hits = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_mask)
      return hits
      
    def collisionDetectionCollectibles(self,collectibles):
      collectiblesHits = pygame.sprite.spritecollide(self,collectibles,False, pygame.sprite.collide_mask)
      return collectiblesHits

   # def collisionResponse(self, enemies, hits, direction):
   #   for enemy in hits:
        
        #if(self.checkIfShouldEat(obstacle)):
        #  obstacle.kill()
        #  continue
        #if direction == "x":
        #  xDif = self.rect.x - obstacle.rect.x
        #  if(xDif < 0): #entering from the left
        #    self.rect.x = obstacle.rect.x - self.rect.width
        #  else:
        #    self.rect.x = obstacle.rect.x + obstacle.rect.width
        #elif direction == "y":
        #  yDif = self.rect.y - obstacle.rect.y
        #  if(yDif < 0): #entering from the top
        #    self.rect.y = obstacle.rect.y - self.rect.height
        #  else:
        #    self.rect.y = obstacle.rect.y + obstacle.rect.height
 
    def checkIfShouldEat(self, obstacle):
      if(obstacle.image.get_at((0,0)) == pygame.Color("yellow")):
          return True
      return False

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