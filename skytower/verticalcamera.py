# This Camera will move up & down with the followed entity's center
from pygame import Rect
from camera import *

class VerticalCamera(Camera):
	def update(self, followedEntity): # updates camera position to follow an entity
		self.viewBounds = self.moveVerticallyWithFollowed(followedEntity._hitbox)
		# print(self.viewBounds)
	def moveVerticallyWithFollowed(self, followedRect):
		l, _, w, h = self.viewBounds
		BOTTOM = 0
		t = -followedRect.top + h / 2
		t = max(BOTTOM, t)
		return Rect(l, t, w, h)
