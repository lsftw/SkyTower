# tick() to update game logic, draw() to redraw game state, repeat
import pygame
from pygame import Rect

class Entity:
	_exactPositions = [-1, -1] # Uses floats to handle variable-deltaSecond frames, Rect is integer only
	_hitbox = Rect(-1, -1, -1, -1) # should match exactPositions for first 2 values
	velocities = [0, 0]
	container = None
	def __init__(self, x, y, width, height):
		self._exactPositions = [x, y]
		self._hitbox = Rect(x, y, width, height)
	def getWidth(self):
		return self._hitbox[2]
	def getHeight(self):
		return self._hitbox[3]
	def setVelocityX(self, velocity):
		self.velocities[0] = velocity
	def setVelocityY(self, velocity):
		self.velocities[1] = velocity
	def getLeft(self):
		return self._exactPositions[0]
	def getRight(self):
		return self._exactPositions[0] + self._hitbox[2]
	def getTop(self):
		return self._exactPositions[1]
	def getBottom(self):
		return self._exactPositions[1] + self._hitbox[3]
	def updateHitbox(self):
		intX = int(self._exactPositions[0])
		intY = int(self._exactPositions[1])
		self._hitbox[0] = intX
		self._hitbox[1] = intY
	def setPosition(self, x, y):
		self._exactPositions = [x, y]
		self.updateHitbox()
	def setSize(self, width, height):
		self._hitbox[2] = width
		self._hitbox[3] = height
	def move(self, deltaX, deltaY):
		self._exactPositions[0] += deltaX
		self._exactPositions[1] += deltaY
		self.updateHitbox()
	# Time-based
	def getGravity(self, deltaSeconds):
		if self.container is None:
			return 0
		# TODO cannot just multiply acceleration, would be less accurate as deltaSeconds increase, pos += .5 * a * t^2 instead?
		return self.container.gravity * deltaSeconds
	def isTouchingGround(self):
		return self.getBottom() >= self.container.getBottom() # must have == to work
	def isMidair(self):
		if self.isTouchingGround():
			return False
		return True # TODO change once platforms are added
	def updateVelocities(self, deltaSeconds):
		if self.isMidair(): # fall
			gravity = self.getGravity(deltaSeconds)
			self.velocities[1] += gravity
		elif self.velocities[1] > 0: # land
			self.velocities[1] = 0
	def preventMovingOutOfBounds(self):
		# constrain x
		newPositionX = self._exactPositions[0]
		if self.container.isTooFarLeft(self):
			newPositionX = self.container.getLeft()
		elif self.container.isTooFarRight(self):
			newPositionX = self.container.getRight() - self.getWidth()
		# constrain y
		newPositionY = self._exactPositions[1]
		if self.container.isTooFarUp(self):
			newPositionY = self.container.getTop()
		elif self.container.isTooFarDown(self):
			newPositionY = self.container.getBottom() - self.getHeight()
		# update position to be inside bounds
		self.setPosition(newPositionX, newPositionY)
	def updatePosition(self, deltaSeconds):
		self.move(self.velocities[0] * deltaSeconds, self.velocities[1] * deltaSeconds)
		self.preventMovingOutOfBounds()
	def updatePhysics(self, deltaSeconds):
		self.updateVelocities(deltaSeconds)
		self.updatePosition(deltaSeconds)
	def tick(self, deltaSeconds):
		self.updatePhysics(deltaSeconds)
	def draw(self, screen):
		pygame.draw.rect(screen, (128, 128, 128), self._hitbox)
