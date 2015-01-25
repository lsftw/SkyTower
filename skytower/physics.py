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

def isStandingOn(entity1, entity2):
	isAbove = entity1._hitbox.bottom == entity2._hitbox.top
	isOn = (entity1.getLeft() > entity2.getLeft() and entity1.getLeft() < entity2.getRight()) or (entity1.getRight() > entity2.getLeft() and entity1.getRight() < entity2.getRight())
	return isAbove and isOn

# Hitbox resolution/interpolation functions

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

def interpolate(validState, invalidState, interpolateFunction, validationFunction): # find the latest hitbox that doesn't collide
	middleState = interpolateFunction(validState, invalidState)
	while middleState is not None: # while there exist intermediate states between validState and invalidState
		middleIsValid = validationFunction(middleState)
		if middleIsValid:
			validState = middleState
		else:
			invalidState = middleState
		middleState = interpolateFunction(validState, invalidState)
	if validationFunction(validState):
		return validState
	else:
		return None

def coordinateBetween(validCoordinate, invalidCoordinate):
	middleCoordinate = int((validCoordinate + invalidCoordinate) / 2)
	isNewCoordinate = middleCoordinate != validCoordinate and middleCoordinate != invalidCoordinate
	if isNewCoordinate:
		return middleCoordinate
	else:
		return None

def interpolateHitboxOnX(oldHitbox, newHitbox, collisionHitbox): # might fail and return None
	# find the latest hitbox that doesn't collide, changing only the x-coordinate
	validX = oldHitbox.x
	invalidX = newHitbox.x
	interpolatedHitbox = newHitbox.copy()
	def validationFunction(candidateX):
		interpolatedHitbox.x = candidateX
		return not interpolatedHitbox.colliderect(collisionHitbox)
	interpolatedX = interpolate(validX, invalidX, coordinateBetween, validationFunction)
	if interpolatedX is None:
		return None
	else:
		interpolatedHitbox.x = interpolatedX
		return interpolatedHitbox

def interpolateHitboxOnY(oldHitbox, newHitbox, collisionHitbox): # might fail and return None
	# find the latest hitbox that doesn't collide, changing only the y-coordinate
	validY = oldHitbox.y
	invalidY = newHitbox.y
	interpolatedHitbox = newHitbox.copy()
	def validationFunction(candidateY):
		interpolatedHitbox.y = candidateY
		return not interpolatedHitbox.colliderect(collisionHitbox)
	interpolatedY = interpolate(validY, invalidY, coordinateBetween, validationFunction)
	if interpolatedY is None:
		return None
	else:
		interpolatedHitbox.y = interpolatedY
		return interpolatedHitbox

def hitboxBetween(hitbox1, hitbox2): # assumes hitboxes are of same size
	middleX = (hitbox1.left + hitbox2.left) / 2
	middleY = (hitbox1.top + hitbox2.top) / 2
	middleHitbox = Rect(middleX, middleY, hitbox1.width, hitbox1.height)
	if middleHitbox.left != hitbox1.left and middleHitbox.left != hitbox2.left and middleHitbox.top != hitbox1.top and middleHitbox.top != hitbox2.top:
		return middleHitbox
	else:
		return None

def interpolateHitboxOnXY(oldHitbox, newHitbox, collisionHitbox): # will always return valid hitbox
	validationFunction = lambda hitbox: not hitbox.colliderect(collisionHitbox)
	return interpolate(oldHitbox, newHitbox, hitboxBetween, validationFunction)
