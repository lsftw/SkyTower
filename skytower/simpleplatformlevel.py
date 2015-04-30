from levelgenerator import *

class SimplePlatformLevel(LevelGenerator):
	def generateLevel(self, gameState):
		# self.addPlatform(gameState, 200, -150, 50, 25)
		# self.addPlatform(gameState, 400, -150, 200, 25)
		self.zigZagPlatformStairs(gameState);
	def zigZagPlatformStairs(self, gameState):
		for j in range(1, 10):
			for i in range(1, 4):
				if j % 2 == 0:
					x = 800 - i*200
					y = 200 - j*300 - i*50
				else:
					x = 0 + i*200
					y = 200 - j*300 - i*50
				self.addPlatform(gameState, x, y, 100, 25)
	def addPlatform(self, gameState, x, y, w, h):
		platform = Entity(x, y, w, h)
		platform.gravity = False
		platform.collisionType = physics.CollisionType.COLLIDEABLE_OBSTACLE
		gameState.addEntity(platform)

