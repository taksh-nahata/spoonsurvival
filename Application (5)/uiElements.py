import pygame

class UIElement(pygame.sprite.Sprite):
  def __init__(self,location,size,color,text,textSize,textColor):
    pygame.sprite.Sprite.__init__(self)
    self.color = color
    self.image = pygame.Surface(size)
    self.image.fill(pygame.Color(self.color))
    self.image.set_alpha(128)
    self.rect = self.image.get_rect()
    self.rect.topleft = location
    self.text = text
    self.textColor = textColor
    self.textChanged = False
    self.trackedValue = 0
    self.uiFont = pygame.font.SysFont("Arial", textSize, bold=True)
    self.setText()

  def update(self):
    if self.textChanged:
      self.setText()
      self.textChanged = False

  def setText(self):
    self.image = pygame.Surface(self.image.get_size())
    self.image.fill(pygame.Color(self.color))
    self.image.set_alpha(128)
    textRender = self.uiFont.render(self.text,True,pygame.Color(self.textColor))
    self.image.blit(textRender,(self.image.get_size()[0]/2 - textRender.get_size()[0]/2,self.image.get_size()[1]/2 - textRender.get_size()[1]/2))

  def changeText(self, newText):
    #The setter method so that we dont have to worry about 
    #   calling setText ourselves
    #text should probably be private but I dont want to add 
    #   any confusion
    self.text = newText
    self.textChanged = True
    