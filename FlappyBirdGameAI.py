from FlappyBirdGame import FlappyBirdGame
import pygame
import neat
import pickle
from model.Bird import Bird
import os
from settings import *
from FlappyBirdUIAI import FlappyBirdUIAI
from model.Pipe import Pipe

class FlappyBirdGameAI(FlappyBirdGame):
    """
        Class to train and test an AI for Flappy bird game using NEAT
    """
    def __init__(self, screen) -> None:
        FlappyBirdGame.__init__(self, screen)
        self.isRunning = True
        self.game = self
        self.UI = FlappyBirdUIAI(self)

        self.toDraw = True
        self.generation = -1
        self.pipeInd = 0
        self.start = True

        self.isTraining = True

        self.setUpNeatConfig()

    def run(self, genomes, config):
        self.generation += 1
        for id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.birdList.append(Bird(self.screen.get_width()//2, self.screen.get_height()//2))
            self.genomes.append(genome)
        
        self.score = 0
        self.reset()
        while self.isRunning and len(self.birdList) > 0:
            self.loop()
    
    ## Override method
    def reset(self):
        gen = self.generation
        toDraw = self.toDraw
        isRunning = self.isRunning

        self.__init__(self.screen)


        self.generation = gen
        self.toDraw = toDraw
        self.isRunning = isRunning

    def loop(self):
        self.update()
        if self.toDraw: self.draw()

    def removeOutOfBoundBirds(self):
        for bird in self.birdList:
            if bird.y + bird.height > BACKGROUND_HEIGHT or bird.y < 0:
                self.nets.pop(self.birdList.index(bird))
                self.genomes.pop(self.birdList.index(bird))
                self.birdList.pop(self.birdList.index(bird))
    
    def update(self):
        self.getEvents()
        self.updateScroll()

        self.pipeInd = self.getClosestPipeIndex()
        self.updateBird()
        self.updatePipes()
        self.removeOutOfBoundBirds()

        if self.isTraining and self.score > 8000:
            self.isRunning = False

    ## Override Method
    def updatePipes(self):
        for pipe in self.pipeList:
            pipe.update(self.scrollSpeed)

            for bird in self.birdList:
                if pipe.collideBird(bird):
                    if self.isTraining:
                        self.genomes[self.birdList.index(bird)].fitness -=1
                        self.genomes.pop(self.birdList.index(bird))
                    self.nets.pop(self.birdList.index(bird))
                    self.birdList.pop(self.birdList.index(bird))
            
            if not pipe.passed and self.bird.x + self.bird.width > pipe.x and self.bird.x + self.bird.width < pipe.x + pipe.width:
                pipe.passed = True
                if self.isTraining:
                    for genome in self.genomes:
                        genome.fitness += 5
                self.pipeList.append(Pipe(self.screen.get_width()))
                self.score += 1

            if pipe.x + pipe.width < 0:
                self.pipeList.remove(pipe)

    def updateBird(self):
        ## Reward bird for each frame it stays alive
        for x, bird in enumerate(self.birdList): 
            if self.isTraining:
                if self.genomes != None:
                    self.genomes[x].fitness += 0.1
            bird.update()

            deltaX = bird.x + bird.width - self.pipeList[self.pipeInd].x 
            deltaYTop = bird.y - self.pipeList[self.pipeInd].height
            deltaYBottom =  bird.y - self.pipeList[self.pipeInd].bottom
            output = self.nets[self.birdList.index(bird)].activate((deltaX, deltaYTop, deltaYBottom))
            if output[0] >= 0.5:
                bird.jump()

    ##Overriding the method
    def draw(self):
        self.UI.draw()
    
    ##Overriding the method
    def getEvents(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.isRunning = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.toDraw = not self.toDraw
    
    def removeOutOfBoundBirds(self):
        for bird in self.birdList:
            if bird.y + bird.height > BACKGROUND_HEIGHT or bird.y < 0:
                self.nets.pop(self.birdList.index(bird))
                self.genomes.pop(self.birdList.index(bird))
                self.birdList.pop(self.birdList.index(bird))
    
    def getClosestPipeIndex(self):
        birdX = self.birdList[0].x
        distanceList = [pipe.x + pipe.width - birdX for pipe in self.pipeList]  #Calculate the x distance between the bird and each pipe
        return distanceList.index(min(i for i in distanceList if i >= 0))
    
    """""""""""""""""""""""""""""
             AI functions
    """""""""""""""""""""""""""""

    def evalGenomes(self, genomes, config):
        """
            Function used to evaluated each generation of the Neat algorithm
        """
        self.nets = []
        self.birdList = []
        self.genomes = []
        self.run(genomes, config)
        
    def runNeat(self, config):
        """
            Run NEAT algorithm based on the [config] file
        """
        p = neat.Population(config)

        ## Print out the statistics of the neat progress to the terminal
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        #Run for up to 30 generations
        winner = p.run(self.evalGenomes, 30)
        print('\nBest genome:\n{!s}'.format(winner))
        with open("bestGenome.pickle", "wb") as f:
            pickle.dump(winner, f)
    
    def trainAI(self):
        """
            Train a new AI using NEAT algorithm
        """
        self.runNeat(self.config)
    
    def testGenome(self, file):
        """
            Test a genome from the specific [file] onto the game
        """
        with open(file, "rb") as f:
            bestGenome = pickle.load(f)
        bestNet = neat.nn.FeedForwardNetwork.create(bestGenome, self.config)
        self.testAI(bestNet)
    
    def testAI(self, net):
        """
            Test a genome given a neural network [net]
        """
        run = True
        self.birdList = []
        self.nets = []
        self.birdList.append(Bird(self.screen.get_width()//2, self.screen.get_height()//2))
        self.nets.append(net)
        self.isTraining = False
        while(run):
            self.clock.tick(60)
            self.update()
            if self.toDraw: self.draw()

    
    def setUpNeatConfig(self):
        """
            Sets up the configuration for NEAT
        """
        localDir = os.path.dirname(__file__)
        configPath = os.path.join(localDir, "config-flappybird.txt")
        
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                configPath)