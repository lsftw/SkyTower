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
	CollisionType.COLLIDEABLE_OBSTACLE: resolveObstacleCollision, # obstacles have collision enabled for all directions
	CollisionType.COLLIDEABLE_PLATFORM: resolvePlatformCollision # platforms can be jumped through from below, but can't fall through
}

def isCollideable(entity):
	return entity.collisionType is CollisionType.COLLIDEABLE_OBSTACLE or entity.collisionType is CollisionType.COLLIDEABLE_PLATFORM

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

def interpolateHitboxOnX(oldHitbox, newHitbox, collisionHitbox): # might fail and return None
	# find the latest hitbox that doesn't collide, changing only the x-coordinate
	validX = oldHitbox.x
	invalidX = newHitbox.x
	interpolatedHitbox = newHitbox.copy()
	while abs(validX - invalidX) > 1:
		interpolatedHitbox.x = (validX + invalidX) / 2
		if interpolatedHitbox.colliderect(collisionHitbox):
			invalidX = interpolatedHitbox.x
		else:
			validX = interpolatedHitbox.x
	interpolatedHitbox.x = validX
	if interpolatedHitbox.colliderect(collisionHitbox):
		return None
	else:
		return interpolatedHitbox

def interpolateHitboxOnY(oldHitbox, newHitbox, collisionHitbox): # might fail and return None
	# find the latest hitbox that doesn't collide, changing only the y-coordinate
	validY = oldHitbox.y
	invalidY = newHitbox.y
	interpolatedHitbox = newHitbox.copy()
	while abs(validY - invalidY) > 1:
		interpolatedHitbox.y = (validY + invalidY) / 2
		if interpolatedHitbox.colliderect(collisionHitbox):
			invalidY = interpolatedHitbox.y
		else:
			validY = interpolatedHitbox.y
	interpolatedHitbox.y = validY
	if interpolatedHitbox.colliderect(collisionHitbox):
		return None
	else:
		return interpolatedHitbox

def interpolateHitboxOnXY(oldHitbox, newHitbox, collisionHitbox): # will always return valid hitbox
	validHitbox = oldHitbox.copy() # doesn't collide
	invalidHitbox = newHitbox.copy() # collides
	# binary interpolation search between validHitbox & invalidHitbox for the latest hitbox that doesn't collide
	while not noMoreHitboxesBetween(validHitbox, invalidHitbox):
		curHitbox = hitboxBetween(validHitbox, invalidHitbox)
		if curHitbox.colliderect(collisionHitbox):
			invalidHitbox = curHitbox
		else:
			validHitbox = curHitbox
	return validHitbox
