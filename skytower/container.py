# Contains Entity objects, tick() draw() repeat

class Container:
	entities = []
	gravity = 500 # accelerationY
	_boundaries = [0, 0, 800, 600]
	def addEntity(self, entity):
		self.entities.append(entity)
		entity.container = self
	def tick(self, deltaSeconds):
		for e in iter(self.entities):
			e.tick(deltaSeconds)
	def draw(self, screen):
		for e in iter(self.entities):
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
