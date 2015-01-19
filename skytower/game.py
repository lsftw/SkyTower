import pygame
import time
import sys
import numpy

from gamestate import *
from container import *
from entity import *
from player import *

windowSize = (800, 600)
backgroundColor = 128, 128, 128

running = True
gameState = GameState(windowSize)

def userQuit():
	global running
	running = False

def handleSpecialKeys(key):
	if key == pygame.K_ESCAPE:
		userQuit()
	elif key == pygame.K_F4:
		userQuit()

def handleKeyUp(key):
	handleSpecialKeys(key)
	gameState.handleKeyUp(key)

def handleEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			userQuit()
		if event.type == pygame.KEYUP:
			handleKeyUp(event.key)

def drawGame(screen):
	screen.fill(backgroundColor)
	gameState.draw(screen)
	pygame.display.flip()

def gameLoop(screen):
	while running:
		handleEvents()
		gameState.update()
		drawGame(screen)
	sys.exit()

def initDisplay():
	pygame.init()
	screen = pygame.display.set_mode(windowSize)
	pygame.display.set_caption("Sky Tower")
	return screen

def initGame():
	gameState.addPlayer(Player(50, -60, 20, 60))
	other = Entity(200, -200, 50, 50)
	other.gravity = False
	other.collisionType = physics.CollisionType.COLLIDEABLE_OBSTACLE
	gameState.addEntity(other)
	other = Entity(400, -200, 200, 50)
	other.gravity = False
	other.collisionType = physics.CollisionType.COLLIDEABLE_OBSTACLE
	gameState.addEntity(other)

def startGame():
	screen = initDisplay()
	initGame()
	gameLoop(screen)

if __name__ == "__main__":
	startGame()
