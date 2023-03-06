from FlappyBirdGame import FlappyBirdGame
from FlappyBirdGameAI import FlappyBirdGameAI
import pygame
from settings import *
import os
import neat

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy bird")
    
    game = FlappyBirdGame(screen)
    game.run()

if __name__ == "__main__":
    main()