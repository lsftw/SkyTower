import pygame
import time
import sys

running = True
startTime = time.time()

def handleEvents():
	global running
	for event in pygame.event.get():  # go through every event that frame.
		if event.type == pygame.QUIT:
			running = False  # if the user tries to quit the app, set running to false in order to exit the loop

# yoyo transition: goes from start to end, then from end to start
def getCurrentTransitionColor(startColor, endColor, transitionTime):
	curTime = time.time()
	timePassedInSeconds = curTime - startTime
	transitionMultiplier = timePassedInSeconds / transitionTime
	invertTransition = int(transitionMultiplier) % 2 == 1
	transitionMultiplier %= 1
	if invertTransition:
		transitionMultiplier = 1 - transitionMultiplier
	curColor = endColor[0] - startColor[0], endColor[1] - startColor[1], endColor[2] - startColor[2]
	curColor = curColor[0]*transitionMultiplier, curColor[1]*transitionMultiplier, curColor[2]*transitionMultiplier
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
