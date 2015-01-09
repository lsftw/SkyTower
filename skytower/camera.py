# Camera modifies Entity Rect hitboxes to simulate scrolling
from pygame import Rect

class Camera():
	viewBounds = None
	def __init__(self, width, height):
		self.viewBounds = Rect(0, 0, width, height)
	def view(self, rect): # transforms an Entity's game logic position to its position on the screen
		return rect.move(self.viewBounds.topleft)
	def getCenter(self):
		return self.viewBounds.center
	def update(self, followedEntity): # updates camera position to follow an entity
		pass
