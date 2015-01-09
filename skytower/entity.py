# update() to update game logic, draw() to redraw game state, repeat
import pygame
from pygame import Rect

# TODO split up functionality into separate classes

class Entity:
	_exactPositions = None # Uses floats to handle variable-deltaSecond frames, Rect is integer only
	_hitbox = None # should match exactPositions for (x, y), but using integers instead
	velocities = None
	container = None
	gravity = True
	canJumpThrough = False # platforms can be jumped through from below
	def __init__(self, x, y, width, height):
		self._exactPositions = [x, y]
		self._hitbox = Rect(x, y, width, height)
		self.velocities = [0, 0]
	# Helper functions for legibility, positions are all using float values
	def getWidth(self):
		return self._hitbox.width
	def getHeight(self):
		return self._hitbox.height
	def getLeft(self):
		return self._exactPositions[0]
	def getRight(self):
		return self._exactPositions[0] + self.getWidth()
	def getTop(self):
		return self._exactPositions[1]
	def getBottom(self):
		return self._exactPositions[1] + self.getHeight()
	def getCenter(self):
		centerX = (self.getLeft() + self.getRight()) / 2
		centerY = (self.getTop() + self.getBottom()) / 2
		return (centerX, centerY)
	def setVelocityX(self, velocity):
		self.velocities[0] = velocity
	def setVelocityY(self, velocity):
		self.velocities[1] = velocity
	# Interactions with other Entity instances
	def isAboveEntity(self, other):
		return self.getBottom() >= other.getTop()
	# Hitbox modifications: all return old hitbox
	def getDisplayedHitbox(self): # use these position & dimensions for display on screen
		return self.container.camera.view(self._hitbox)
	def updateHitbox(self):
		oldHitbox = self._hitbox.copy()
		intX = int(self._exactPositions[0])
		intY = int(self._exactPositions[1])
		self._hitbox[0] = intX
		self._hitbox[1] = intY
		return oldHitbox
	def setPosition(self, x, y):
		self._exactPositions = [x, y]
		return self.updateHitbox()
	def setSize(self, width, height):
		oldHitbox = self._hitbox.copy()
		self._hitbox[2] = width
		self._hitbox[3] = height
		return oldHitbox
	def move(self, deltaX, deltaY):
		self._exactPositions[0] += deltaX
		self._exactPositions[1] += deltaY
		return self.updateHitbox()
	# Time-based
	def getGravity(self, deltaSeconds):
		if self.container is None or not self.gravity:
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
		oldHitbox = self.move(self.velocities[0] * deltaSeconds, self.velocities[1] * deltaSeconds)
		self.preventMovingOutOfBounds()
		return oldHitbox
	def handleCollision(self, selfOldHitbox, other):
		# TODO collision check
		pass
	def handleAllCollisions(self, selfOldHitbox):
		if self.container is not None:
			for entity in iter(self.container.entities):
				if entity is not self:
					self.handleCollision(selfOldHitbox, entity)
	def updatePhysics(self, deltaSeconds):
		self.updateVelocities(deltaSeconds)
		oldHitbox = self.updatePosition(deltaSeconds)
		self.handleAllCollisions(oldHitbox)
	# called by container
	def update(self, deltaSeconds):
		self.updatePhysics(deltaSeconds)
	def draw(self, screen):
		pygame.draw.rect(screen, (128, 255, 128), self.getDisplayedHitbox())
