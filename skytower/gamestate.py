import time

from container import *

class GameState:
	container = None
	player = None
	startTime = 0
	lastTickTime = startTime
	def __init__(self, (width, height)):
		self.container = Container(width, height)
		self.startTime = time.time()
		self.lastTickTime = self.startTime
	def addPlayer(self, player): # players have keyboard controls and are followed by the camera
		self.player = player
		self.addEntity(player)
		self.container.cameraFollow(player)
	def addEntity(self, entity):
		self.container.addEntity(entity)
	def handleKeyUp(self, key):
		self.player.handleKeyUp(key)
	# called every frame
	def update(self):
		curTime = time.time()
		deltaSeconds = curTime - self.lastTickTime
		self.lastTickTime = curTime
		self.container.update(deltaSeconds)
	def draw(self, screen):
		self.container.draw(screen)
