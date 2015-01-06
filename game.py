import pygame
import time
import sys
import numpy

running = True
startTime = time.time()

def handleEvents():
	global running
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

# yoyo transition: goes from start to end, then from end to start
def getCurrentTransitionColor(startColor, endColor, transitionTime):
	curTime = time.time()
	timePassedInSeconds = curTime - startTime
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
	pygame.display.flip()

def gameLoop(screen):
	while running:
		handleEvents()
		drawGame(screen)
	sys.exit()

def initGame():
	pygame.init()
	window_size = (800, 600)
	screen = pygame.display.set_mode(window_size)
	pygame.display.set_caption("Cloud Tower")
	return screen

def startGame():
	screen = initGame()
	gameLoop(screen)

startGame()
