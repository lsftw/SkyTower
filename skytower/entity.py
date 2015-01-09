# tick() to update game logic, draw() to redraw game state, repeat
import pygame
from pygame import Rect

class Entity:
	_exactPositions = [-1, -1] # Uses floats to handle variable-deltaSecond frames, Rect is integer only
	_hitbox = Rect(-1, -1, -1, -1) # should match exactPositions for first 2 values
	velocities = [0, 0]
	def __init__(self, x, y, width, height):
		self._exactPositions = [x, y]
		self._hitbox = Rect(x, y, width, height)
	def setVelocityX(self, velocity):
		self.velocities[0] = velocity
	def setVelocityY(self, velocity):
		self.velocities[1] = velocity
	def updateHitbox(self):
		intX = int(self._exactPositions[0])
		intY = int(self._exactPositions[1])
		self._hitbox[0] = intX
		self._hitbox[1] = intY
	def setPosition(self, x, y):
		self._exactPositions = (x, y)
		self.updateHitbox()
	def setSize(self, width, height):
		self._hitbox[2] = width
		self._hitbox[3] = height
	def move(self, deltaX, deltaY):
		self._exactPositions[0] += deltaX
		self._exactPositions[1] += deltaY
		self.updateHitbox()
	def tick(self, deltaSeconds):
		self.move(self.velocities[0] * deltaSeconds, self.velocities[1] * deltaSeconds)
	def draw(self, screen):
		pygame.draw.rect(screen, (128, 128, 128), self._hitbox)
