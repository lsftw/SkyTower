# Contains Entity objects, update() draw() repeat
from verticalcamera import *

class Container:
	entities = None
	gravity = 500 # accelerationY
	_boundaries = None
	camera = None
	def __init__(self, width, height):
		self.entities = []
		self._boundaries = (0, width, -100000, 0)
		self.camera = VerticalCamera(width, height)
	# Entity interaction
	def addEntity(self, entity):
		self.entities.append(entity)
		entity.container = self
	def cameraFollow(self, entity):
		self.camera.followedEntity = entity
	# called every frame
	def update(self, deltaSeconds):
		for e in iter(self.entities):
			e.update(deltaSeconds)
		self.camera.update()
	def draw(self, screen):
		for e in iter(self.entities): # TODO don't draw out of camera bounds entities
			e.draw(screen)
	# spatial boundaries
	def getLeft(self):
		return self._boundaries[0]
	def getRight(self):
		return self._boundaries[1]
	def getTop(self):
		return self._boundaries[2]
	def getBottom(self):
		return self._boundaries[3]
	def isTooFarLeft(self, entity):
		return entity.getLeft() < self.getLeft()
	def isTooFarRight(self, entity):
		return entity.getRight() > self.getRight()
	def isTooFarUp(self, entity):
		return entity.getTop() < self.getTop()
	def isTooFarDown(self, entity):
		return entity.getBottom() > self.getBottom()
