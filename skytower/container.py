# Contains Entity objects, update() draw() repeat
from camera import *

class Container:
	entities = None
	gravity = 500 # accelerationY
	_boundaries = None
	camera = None
	followedEntity = None
	def __init__(self, width, height):
		self.entities = []
		self._boundaries = (0, 0, width, height)
		self.camera = Camera(width, height)
	# Entity interaction
	def addEntity(self, entity):
		self.entities.append(entity)
		entity.container = self
	def cameraFollow(self, entity):
		self.followedEntity = entity
	# called every frame
	def update(self, deltaSeconds):
		for e in iter(self.entities):
			e.update(deltaSeconds)
		if self.followedEntity is not None:
			self.camera.update(self.followedEntity)
	def draw(self, screen):
		for e in iter(self.entities): # TODO don't draw out of camera bounds entities
			e.draw(screen)
	# spatial boundaries
	def getLeft(self):
		return self._boundaries[0]
	def getRight(self):
		return self._boundaries[2]
	def getTop(self): # TODO later remove top boundary
		return self._boundaries[1]
	def getBottom(self): # TODO later set to 0, after camera centering implemented
		return self._boundaries[3]
	def isTooFarLeft(self, entity):
		return entity.getLeft() < self.getLeft()
	def isTooFarRight(self, entity):
		return entity.getRight() > self.getRight()
	def isTooFarUp(self, entity):
		return entity.getTop() < self.getTop()
	def isTooFarDown(self, entity):
		return entity.getBottom() > self.getBottom()
