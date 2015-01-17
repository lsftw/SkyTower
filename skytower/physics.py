# Handles and resolves collisions between entities, collisions only occur between a moving collider and a collideable, and only the collider is moved back
# The collider is moved back by interpolating between its old hitbox that didn't collide and its new hitbox that does collide
from entity import *

from enum import Enum

def resolveObstacleCollision(collider, obstacle):
	interpolatedHitbox = interpolateHitbox(collider.oldHitbox, collider._hitbox, obstacle._hitbox)
	collider.setPosition(interpolatedHitbox.left, interpolatedHitbox.top)

def resolvePlatformCollision(collider, platform): # TODO platform collision check
	pass

CollisionType = Enum('CollisionType', 'COLLIDER COLLIDEABLE_OBSTACLE COLLIDEABLE_PLATFORM')
COLLISION_RESOLUTION_FUNCTIONS = {
	# CollisionType.COLLIDER: (lambda x, y: None),
	CollisionType.COLLIDEABLE_OBSTACLE: resolveObstacleCollision,
	CollisionType.COLLIDEABLE_PLATFORM: resolvePlatformCollision
}

def isCollideable(entity):
	return entity.isObstacle or entity.isPlatform

def willCollide(entity1, entity2):
	return entity1._hitbox.colliderect(entity2._hitbox)

def handleCollision(entity1, entity2):
	if entity1 is entity2:
		return
	elif isCollideable(entity1):
		collideable = entity1
		collider = entity2
	elif isCollideable(entity2):
		collideable = entity2
		collider = entity1
	else:
		return

	if willCollide(collider, collideable):
		try:
			resolveCollision = COLLISION_RESOLUTION_FUNCTIONS[collideable.collisionType]
			resolveCollision(collider, collideable)
		except KeyError, e:
			print('Unhandled collision type:', collideable.collisionType.name)

# Hitbox resolution/interpolation functions

def hitboxBetween(hitbox1, hitbox2): # assumes hitboxes are of same size
	middleX = (hitbox1.left + hitbox2.left) / 2
	middleY = (hitbox1.top + hitbox2.top) / 2
	return Rect(middleX, middleY, hitbox1.width, hitbox1.height)

def hitboxEqual(hitbox1, hitbox2):
	return hitbox1.left == hitbox2.left and hitbox1.top == hitbox2.top and hitbox1.width == hitbox2.width and hitbox1.height == hitbox2.height

def noMoreHitboxesBetween(hitbox1, hitbox2):
	middleHitbox = hitboxBetween(hitbox1, hitbox2)
	return hitboxEqual(middleHitbox, hitbox1) or hitboxEqual(middleHitbox, hitbox2)

# find the latest hitbox that doesn't collide by interpolating between old and new hitbox
def interpolateHitbox(oldHitbox, newHitbox, collisionHitbox):
	interpolatedHitboxX = interpolateHitboxOnX(oldHitbox, newHitbox, collisionHitbox)
	interpolatedHitboxY = interpolateHitboxOnY(oldHitbox, newHitbox, collisionHitbox)
	# if collision only occurs along one axis, allow movement on the other axis
	if interpolatedHitboxX is None:
		interpolatedHitbox = interpolatedHitboxY
	elif interpolatedHitboxY is None:
		interpolatedHitbox = interpolatedHitboxX
	else: # collision occurs along both axes, must resolve coordinates together
		interpolatedHitbox = interpolateHitboxOnXY(oldHitbox, newHitbox, collisionHitbox)
	return interpolatedHitbox

# TODO reduce duplicated code for single-coordinate interpolation functions
# TODO don't use sequential interpolation for single-coordinate, use binary interpolation (like XY interpolation function)

def interpolateHitboxOnX(oldHitbox, newHitbox, collisionHitbox): # might fail and return None
	# while newHitbox.x != oldHitbox.x, newHitbox.x move 1px towards oldHitbox.x
	signNum = lambda num: cmp(num, 0)
	deltaX = signNum(oldHitbox.x - newHitbox.x) # interpolate hitbox 1px at a time
	if signNum(deltaX) == 0:
		return None
	interpolatedHitbox = newHitbox.copy()
	while interpolatedHitbox.x != oldHitbox.x and interpolatedHitbox.colliderect(collisionHitbox):
		interpolatedHitbox.x += deltaX
	if interpolatedHitbox.colliderect(collisionHitbox):
		return None
	else:
		return interpolatedHitbox

def interpolateHitboxOnY(oldHitbox, newHitbox, collisionHitbox): # might fail and return None
	# while newHitbox.y != oldHitbox.y, newHitbox.y move 1px towards oldHitbox.y
	signNum = lambda num: cmp(num, 0)
	deltaY = signNum(oldHitbox.y - newHitbox.y) # interpolate hitbox 1px at a time
	if signNum(deltaY) == 0:
		return None
	interpolatedHitbox = newHitbox.copy()
	while interpolatedHitbox.y != oldHitbox.y and interpolatedHitbox.colliderect(collisionHitbox):
		interpolatedHitbox.y += deltaY
	if interpolatedHitbox.colliderect(collisionHitbox):
		return None
	else:
		return interpolatedHitbox

def interpolateHitboxOnXY(oldHitbox, newHitbox, collisionHitbox): # will always return valid hitbox
	validHitbox = oldHitbox.copy() # doesn't collide
	invalidHitbox = newHitbox.copy() # collides
	# binary interpolation search between validHitbox & invalidHitbox for the first hitbox that doesn't collide
	while not noMoreHitboxesBetween(validHitbox, invalidHitbox):
		curHitbox = hitboxBetween(validHitbox, invalidHitbox)
		if curHitbox.colliderect(collisionHitbox):
			invalidHitbox = curHitbox
		else:
			validHitbox = curHitbox
	return validHitbox
