# Entity w/ controls
import pygame

from entity import *

class Player(Entity):
	movementSpeed = 250 # pixels per second
	def handleKeys(self, deltaSeconds):
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_LEFT]:
			self.setVelocityX(-self.movementSpeed)
		elif keysPressed[pygame.K_RIGHT]:
			self.setVelocityX(self.movementSpeed)
		else:
			self.setVelocityX(0)
	def tick(self, deltaSeconds):
		self.handleKeys(deltaSeconds)
		Entity.tick(self, deltaSeconds)
	def handleKeyUp(self, key):
		pass
