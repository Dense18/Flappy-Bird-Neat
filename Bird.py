import pygame
from settings import *
import os
"""
    Bird object for handling bird positions and movements
"""
class Bird:
    def __init__(self, x, y, width = 0, height = 0, velocity = 0) -> None:
        self.x = x
        self.y = y

        self.birdImgList = []
        self.birdIndex = 0
        self.loadImages()
        self.currentImg = self.birdImgList[self.birdIndex]

        self.width = self.imgWidth
        self.height = self.imgHeight

        self.gravity = 0.5
        self.velocity = velocity
        self.maxVelocity = 9
        self.minVelocity = -7.5
        self.airResistance = 1
        self.lift = 13

        self.clicked = False

    
    def update(self):
        #gravity
        # self.velocity = min(self.velocity + 0.3, self.maxVelocity)
        # print(self.velocity)

        self.velocity += self.gravity
        self.velocity *= self.airResistance

        if self.velocity > self.maxVelocity: 
            self.velocity = self.maxVelocity
        if self.velocity < self.minVelocity:
            self.velocity = self.minVelocity

        ##Change this so it is not bound
        if self.y + self.height > BACKGROUND_HEIGHT:
            # self.y += self.velocity
            self.y = BACKGROUND_HEIGHT - self.height
        
        if self.y < 0:
            self.y = 0

        self.y += self.velocity

        ## Jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.jump()
            self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.birdIndex = (self.birdIndex + 1) % len(self.birdImgList)
        self.currentImg = self.birdImgList[self.birdIndex]

        #Rotate bird
        self.currentImg = pygame.transform.rotate(self.currentImg, self.velocity * -4)

    def jump(self):
        self.velocity -= self.lift

    def draw(self, screen):
        screen.blit(self.currentImg, (self.x, self.y))
        pass
    
    def loadImages(self):
        for i in range(1, 4):
            birdImg = pygame.image.load(os.path.join(IMAGES_FOLDER, f"bird{i}.png"))
            self.birdImgList.append(birdImg)

        self.imgWidth = self.birdImgList[0].get_width()
        self.imgHeight = self.birdImgList[0].get_height()
    
    def getMask(self):
        return pygame.mask.from_surface(self.currentImg)
            

