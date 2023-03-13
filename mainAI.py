from FlappyBirdGameAI import FlappyBirdGameAI
import pygame
from settings import *
import sys

def main():
    isTrain = True
    if len(sys.argv) == 1: 
        isTrain = True
    elif len(sys.argv) >= 2:
        if sys.argv[1] == "-train": 
            isTrain = True
        elif sys.argv[1] == "-test": 
            isTrain = False
        else:
            print("Unknown parameters!\n Available option arguments are: -train, -test")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy bird")
    
    game = FlappyBirdGameAI(screen)
    game.trainAI() if isTrain else game.testGenome("bestGenome.pickle")

if __name__ == "__main__":
    main()