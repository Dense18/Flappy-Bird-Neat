from FlappyBirdGame import FlappyBirdGame
import pygame
from settings import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy bird")
    
    game = FlappyBirdGame(screen)
    game.run()

if __name__ == "__main__":
    main()