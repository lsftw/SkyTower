# update() to update game logic, draw() to redraw game state, repeat
import pygame
from pygame import Rect

import physics

class Entity:
	_exactPositions = None # Uses floats to handle variable-deltaSecond frames, Rect is integer only
	_hitbox = None # should match exactPositions for (x, y), but using integers instead
	oldHitbox = None # hitbox last frame, used for resolving collisions
	velocities = None
	container = None
	gravity = True
	collisionType = physics.CollisionType.COLLIDER
	def __init__(self, x, y, width, height):
		self._exactPositions = [x, y]
		self._hitbox = Rect(x, y, width, height)
		self.velocities = [0, 0]
	# Helper functions for legibility, positions are all using float values
	def getWidth(self):
		return self._hitbox.width
	def getHeight(self):
		return self._hitbox.height
	def getExactLeft(self):
		return self._exactPositions[0]
	def getExactRight(self):
		return self._exactPositions[0] + self.getWidth()
	def getExactTop(self):
		return self._exactPositions[1]
	def getExactBottom(self):
		return self._exactPositions[1] + self.getHeight()
	def getLeft(self):
		return self._hitbox.left
	def getRight(self):
		return self._hitbox.right
	def getTop(self):
		return self._hitbox.top
	def getBottom(self):
		return self._hitbox.bottom
	def getExactCenter(self):
		centerX = (self.getLeft() + self.getRight()) / 2
		centerY = (self.getTop() + self.getBottom()) / 2
		return (centerX, centerY)
	def isStationary(self):
		return self.velocities[0] == 0 and self.velocities[1] == 0
	def setVelocityX(self, pixelsPerSecond):
		self.velocities[0] = pixelsPerSecond
	def setVelocityY(self, pixelsPerSecond):
		self.velocities[1] = pixelsPerSecond
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
	def isStandingOnCollideable(self):
		if self.container is not None:
			for entity in iter(self.container.entities):
				if physics.isStandingOn(self, entity):
					return True
		return False
	def isTouchingGround(self):
		atAbsoluteBottom = self.getBottom() >= self.container.getBottom() # must have == to work
		return atAbsoluteBottom
	def isMidair(self):
		if self.isTouchingGround():
			return False
		return not self.isStandingOnCollideable()
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
	def handleAllCollisions(self):
		if self.container is not None:
			for entity in iter(self.container.entities):
				physics.handleCollision(self, entity)
	def updatePhysics(self, deltaSeconds):
		self.updateVelocities(deltaSeconds)
		self.oldHitbox = self.updatePosition(deltaSeconds)
		self.handleAllCollisions()
	# called by container
	def update(self, deltaSeconds):
		self.updatePhysics(deltaSeconds)
	def draw(self, screen):
		pygame.draw.rect(screen, (128, 255, 128), self.getDisplayedHitbox())
