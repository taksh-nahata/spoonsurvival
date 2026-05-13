### DO NOT MODIFY WITHOUT CONSULTING MR. JOHNSON ###
### DOING SO MAY RESULT IN A NONFUNCTIONAL GAME  ###
### WHICH WOULD BE LIKE A ZERO DUDE...           ###
### SO DONT DO THAT :)                           ###

import pygame

class JoystickInterface:
	def __init__(self, joystick):#playerNum):
		self.joystick = joystick
		#if(pygame.joystick.get_count() > playerNum - 1):
		#	self.joystick = pygame.joystick.Joystick(playerNum - 1)
		#	self.joystick.init()
	
	
	def getButtonsPressed(self):
		buttons = []
		if(self.joystick != None):
			for lcv in range(self.joystick.get_numbuttons()):
				if self.joystick.get_button(lcv):
					buttons.append(lcv)
		return buttons

	def getJoystickDirection(self):
		directions = []
		if(self.joystick != None):
			if self.joystick.get_axis(1) < -0.5:
				directions.append("UP")
			elif self.joystick.get_axis(1) > 0.5:
				directions.append("DOWN")
			if self.joystick.get_axis(0) < -0.5:
				directions.append("LEFT")
			elif self.joystick.get_axis(0) > 0.5:
				directions.append("RIGHT")
		return directions
