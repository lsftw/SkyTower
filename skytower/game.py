import pygame
import time
import sys
import numpy

from gamestate import *
from container import *
from entity import *
from player import *

running = True
gameState = GameState()

def userQuit():
	global running
	running = False

def handleKeyUp(key):
	gameState.handleKeyUp(key)

def handleEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			userQuit()
		if event.type == pygame.KEYUP:
			handleKeyUp(event.key)

# yoyo transition: goes from start to end, then from end to start
def getCurrentTransitionColor(startColor, endColor, transitionTime):
	curTime = time.time()
	timePassedInSeconds = curTime - gameState.startTime
	transitionMultiplier = timePassedInSeconds / transitionTime
	invertTransition = int(transitionMultiplier) % 2 == 1
	transitionMultiplier %= 1
	if invertTransition:
		transitionMultiplier = 1 - transitionMultiplier
	curColor = numpy.subtract(endColor, startColor)
	curColor = numpy.multiply(curColor, transitionMultiplier)
	return curColor

def drawGame(screen):
	# gradually turn screen from black to white then back to black
	black = 0, 0, 0
	white = 255, 255, 255
	TRANSITION_TIME_SECONDS = 10
	curColor = getCurrentTransitionColor(black, white, TRANSITION_TIME_SECONDS)
	screen.fill(curColor)
	gameState.draw(screen)
	pygame.display.flip()

def gameLoop(screen):
	while running:
		handleEvents()
		gameState.tick()
		drawGame(screen)
	sys.exit()

def initDisplay():
	pygame.init()
	window_size = (800, 600)
	screen = pygame.display.set_mode(window_size)
	pygame.display.set_caption("Cloud Tower")
	return screen

def initGame():
	gameState.addPlayer(Player(50, 50, 20, 60))

def startGame():
	screen = initDisplay()
	initGame()
	gameLoop(screen)

if __name__ == "__main__":
	startGame()
