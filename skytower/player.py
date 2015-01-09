# Entity w/ controls
import pygame

from entity import *

class Player(Entity):
	movementSpeed = 250 # pixels per second
	jumpSpeed = 500
	def tryToJump(self):
		if not self.isMidair():
			self.setVelocityY(-self.jumpSpeed)
	def handleKeys(self, deltaSeconds):
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_LEFT]:
			self.setVelocityX(-self.movementSpeed)
		elif keysPressed[pygame.K_RIGHT]:
			self.setVelocityX(self.movementSpeed)
		else:
			self.setVelocityX(0)
		if keysPressed[pygame.K_UP]:
			self.tryToJump()
	def tick(self, deltaSeconds):
		self.handleKeys(deltaSeconds)
		Entity.tick(self, deltaSeconds)
	def handleKeyUp(self, key):
		pass
