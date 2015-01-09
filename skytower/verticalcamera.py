# This Camera will move up & down with the followed entity's center
from pygame import Rect
from camera import *

class VerticalCamera(Camera):
	def update(self): # updates camera position to follow an entity
		if self.followedEntity is not None:
			self.viewBounds = self.moveVerticallyWithFollowed(self.followedEntity._hitbox)
	def moveVerticallyWithFollowed(self, followedRect):
		l, _, w, height = self.viewBounds # only top & height are relevant
		BOTTOM = height
		top = -followedRect.top + height / 2
		top = max(BOTTOM, top)
		return Rect(l, top, w, height)
