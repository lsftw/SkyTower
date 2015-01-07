import time

from container import *

class GameState:
	container = Container()
	player = None
	startTime = time.time()
	lastTickTime = startTime
	def addPlayer(self, player):
		self.player = player
		self.addEntity(player)
	def addEntity(self, entity):
		self.container.addEntity(entity)
	def handleKeyUp(self, key):
		self.player.handleKeyUp(key)
	def tick(self):
		curTime = time.time()
		deltaSeconds = curTime - self.lastTickTime
		self.lastTickTime = curTime
		self.container.tick(deltaSeconds)
	def draw(self, screen):
		self.container.draw(screen)
