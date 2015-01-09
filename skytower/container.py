# Contains Entity objects, tick() draw() repeat

class Container:
	entities = []
	def addEntity(self, entity):
		self.entities.append(entity)
	def tick(self, deltaSeconds):
		for e in iter(self.entities):
			e.tick(deltaSeconds)
	def draw(self, screen):
		for e in iter(self.entities):
			e.draw(screen)
