# Camera modifies Entity Rect hitboxes to simulate scrolling
# This Camera will move up if the player moves up, but never move down or any other direction
# TODO split game-specific functionality into subclass of this Camera class
from pygame import Rect

class Camera(object):
	viewBounds = None
	def __init__(self, width, height):
		self.viewBounds = Rect(0, 0, width, height)
	def view(self, rect): # transforms an Entity's game logic position to its position on the screen
		#return rect.move(self.viewBounds.topleft)
		return rect
	def getCenter(self):
		return self.viewBounds.center
	def update(self, followedEntity): # updates camera position to follow an entity
		# followedCenterY = followedEntity.getCenter()[1]
		# cameraDiff = followedCenterY - self.viewBounds.centery
		# # if cameraDiff < 0: # if camera too low, since negative is upward
		# self.viewBounds.move_ip(0, cameraDiff)
		# print(cameraDiff)
		#
		#
		#
		#self.viewBounds = self.complex_camera(self.viewBounds, followedEntity._hitbox)
		pass
	def complex_camera(self, camera, target_rect):
		HALF_WIDTH = 400
		HALF_HEIGHT = 300
		WIN_WIDTH = 800
		l, t, _, _ = target_rect
		_, _, w, h = camera
		l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

		l = min(0, l)                           # stop scrolling at the left edge
		l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
		t = max(0, t)							# stop scrolling at the bottom
		t = min(0, t)                           # stop scrolling at the top
		return Rect(l, t, w, h)

