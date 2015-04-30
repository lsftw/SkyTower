# Entity w/ controls
import pygame

from entity import *

class Player(Entity):
	# speeds in pixels per second
	maxMovementSpeed = 250
	maxJumpSpeed = 450
	# Health recovers very slowly, is lost when stamina goes negative, regens when stamina at max
	maxHealth = 100
	health = maxHealth
	healthRegenPerPositiveStamina = .5 / 20
	healthCostPerNegativeStamina = 1.0 / 20
	# TODO add fall damage using negative stamina
	# Stamina actions are less effective on low stamina, and borrows from health if too low
	staminaCostPerSecondMoving = 10
	staminaCostPerJump = 20
	staminaRegenPerSecond = 20
	maxStamina = 100
	stamina = maxStamina
	def staminaPercentage(self):
		return self.stamina / self.maxStamina
	def performStaminaAction(self, actionFunction, staminaCost):
		actionFunction(self.staminaPercentage())
		self.loseStamina(staminaCost)
	def jump(self, percentageEffect):
		self.setVelocityY(-self.maxJumpSpeed * percentageEffect)
	def tryToJump(self):
		if not self.isMidair():
			self.performStaminaAction(self.jump, self.staminaCostPerJump)
	def handleKeys(self, deltaSeconds):
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_LEFT] or keysPressed[pygame.K_a]:
			self.setVelocityX(-self.maxMovementSpeed)
			self.slowMovementWhenTired()
		elif keysPressed[pygame.K_RIGHT] or keysPressed[pygame.K_d]:
			self.setVelocityX(self.maxMovementSpeed)
			self.slowMovementWhenTired()
		else:
			self.setVelocityX(0)
		if keysPressed[pygame.K_UP] or keysPressed[pygame.K_w]:
			self.tryToJump()
	def slowMovementWhenTired(self):
		self.velocities[0] *= self.staminaPercentage()
	def loseStaminaOnMovement(self, deltaSeconds):
		if self.isStationary():
			return
		movementCost = self.staminaCostPerSecondMoving * deltaSeconds
		self.loseStamina(movementCost)
	def gainStamina(self, staminaGain):
		self.stamina += staminaGain
		if self.stamina > self.maxStamina:
			extraStamina = self.stamina - self.maxStamina
			self.gainHealth(self.healthRegenPerPositiveStamina * extraStamina)
			self.stamina = self.maxStamina
	def loseStamina(self, staminaLoss):
		self.stamina -= staminaLoss
		if self.stamina < 0:
			self.health -= self.healthCostPerNegativeStamina * -self.stamina
			self.stamina = 0
	def gainHealth(self, healthGain):
		self.health += healthGain
		if self.health > self.maxHealth:
			self.health = self.maxHealth
	def recover(self, deltaSeconds):
		self.gainStamina(self.staminaRegenPerSecond * deltaSeconds)
	def update(self, deltaSeconds):
		self.handleKeys(deltaSeconds)
		Entity.update(self, deltaSeconds)
		self.loseStaminaOnMovement(deltaSeconds)
		self.recover(deltaSeconds)
	def handleKeyUp(self, key):
		pass
	def draw(self, screen):
		pygame.draw.rect(screen, (128, 128, 255), self.getDisplayedHitbox())
