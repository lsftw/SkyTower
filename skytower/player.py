# Entity w/ controls
import pygame

from entity import *

class Player(Entity):
	# speeds in pixels per second
	maxMovementSpeed = 250
	maxJumpSpeed = 450
	staminaCostPerSecondMoving = 10
	staminaCostPerJump = 15
	staminaRegenPerSecond = 20
	maxStamina = 100
	stamina = maxStamina
	def staminaPercentage(self):
		return self.stamina / self.maxStamina
	def performStaminaAction(self, actionFunction, staminaCost):
		actionFunction(self.staminaPercentage())
		self.stamina -= staminaCost
		if self.stamina < 0:
			self.stamina = 0
	def jump(self, percentageEffect):
		self.setVelocityY(-self.maxJumpSpeed * percentageEffect)
	def tryToJump(self):
		if not self.isMidair():
			self.performStaminaAction(self.jump, self.staminaCostPerJump)
	def handleKeys(self, deltaSeconds):
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_LEFT]:
			self.setVelocityX(-self.maxMovementSpeed)
			self.slowMovementWhenTired()
		elif keysPressed[pygame.K_RIGHT]:
			self.setVelocityX(self.maxMovementSpeed)
			self.slowMovementWhenTired()
		else:
			self.setVelocityX(0)
		if keysPressed[pygame.K_UP]:
			self.tryToJump()
	def slowMovementWhenTired(self):
		self.velocities[0] *= self.staminaPercentage()
	def loseStaminaOnMovement(self, deltaSeconds):
		if self.isStationary():
			return
		movementCost = self.staminaCostPerSecondMoving * deltaSeconds
		self.stamina -= movementCost
		if self.stamina < 0:
			self.stamina = 0
	def recover(self, deltaSeconds):
		self.stamina += self.staminaRegenPerSecond * deltaSeconds
		if self.stamina > self.maxStamina:
			self.stamina = self.maxStamina
	def update(self, deltaSeconds):
		self.handleKeys(deltaSeconds)
		Entity.update(self, deltaSeconds)
		self.loseStaminaOnMovement(deltaSeconds)
		self.recover(deltaSeconds)
	def handleKeyUp(self, key):
		pass
	def draw(self, screen):
		pygame.draw.rect(screen, (128, 128, 255), self.getDisplayedHitbox())
