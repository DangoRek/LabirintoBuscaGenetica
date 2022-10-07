from os import system, name
from time import sleep
from random import randint
from math import sqrt

SPEED = 10
SLEEP = 1/SPEED

LEVEL_WIDTH = 70
LEVEL_HEIGHT = 30

WALL = '\u2588'
GOAL = '*'
HOME = 'H'
LEFT = '\u25C0'
DOWN = '\u25BC'
RIGHT = '\u25B6'
UP = '\u25B2'
STOP = "$"
EMPTY = ' '

P1_COLOR = '\033[95m'
P2_COLOR = '\033[94m'
P3_COLOR = '\033[96m'
P4_COLOR = '\033[92m'
P5_COLOR = '\033[93m'
P6_COLOR = '\033[91m'
P7_COLOR = '\033[1m'
P8_COLOR = '\033[4m'
NO_COLOR = '\033[0m'

class Simulation:
    def __init__(self, level):
        self.agents = []
        self.level = level
        self.width = len(self.level[0])
        self.height = len(self.level)

        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.level[y][x] == HOME:
                    self.home = (x, y)
                elif self.level[y][x] == GOAL:
                    self.goal = (x, y)

    def gotoxy(self, x, y):
        print("%c[%d;%df" % (0x1B, y, x), end='')

    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def clearAgents(self):
        self.agents = []

    def addAgent(self, agent):
        agent.Start(self)
        agent.Draw()
        self.agents.append(agent);

    def run(self):
        while (True):
            done = 0

            self.draw()
            for agent in self.agents:
                if agent.Done():
                    done += 1
                else:
                    agent.Update()

                agent.Draw()

            if done == len(self.agents):
                break

            sleep(SLEEP)

    def draw(self):
        self.clear()
        for y in range(0, self.height):
            for x in range(0,self.width):
                print(self.level[y][x],end="")
            print("")

class Robot:
    def __init__(self, genes):
        self.x = 0
        self.y = 0
        self.dir = UP
        self.color = '\033[95m'
        self.genes = genes
        self.curr_action = 0

    def Done(self):
        return self.curr_action >= len(self.genes)

    def Start(self, simulation):
        self.x = simulation.home[0]
        self.y = simulation.home[0]
        self.simulation = simulation

    def Move(self, direction):
        dx = self.x
        dy = self.y

        if (direction == UP):
            dy -= 1
            self.dir = UP
        elif (direction == DOWN):
            dy += 1
            self.dir = DOWN
        elif (direction == LEFT):
            dx -= 1
            self.dir = LEFT
        elif (direction == RIGHT):
            dx += 1
            self.dir = RIGHT

        if (self.simulation.level[dy][dx] in (EMPTY, HOME, GOAL)):
            self.x = dx
            self.y = dy

    def Draw(self):
        print("%c[%d;%df" % (0x1B, self.y+1, self.x+1), end='')
        print(self.dir)

    def Update(self):
        self.Move(self.genes[self.curr_action]);
        self.curr_action += 1

    def GetDistance(self):
        dx = abs(self.x - self.simulation.goal[0])
        dy = abs(self.y - self.simulation.goal[1])
        dist = dx + dy
        return dist

###################### Seu trabalho inicia aqui ###############################
# Esse Ã© o desenho do seu level
level = [
    [WALL,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,HOME ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,GOAL ,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL]
]

# O robÃ´ recebe como parÃ¢metro os movimentos (DNA)
# Use um tamanho de DNA apropriado.
movimentosNum=30
robotNum=100
simulation = Simulation(level)
#create 100 random genes
def createRandomGenes():
    dnas = []
    for i in range(robotNum):
        genes = []
        for j in range(movimentosNum):  
            decision = randint(0,3)
            if(i==1 and j%2==0):
                decision = 0
            if(i==2 and j%2==0):
                decision = 1
            if(i==3 and j%2==0):
                decision = 2
            if(i==4 and j%2==0):
                decision = 3
            if decision == 0:
                genes.append(UP)
            elif decision == 1:
                genes.append(DOWN)
            elif decision == 2:
                genes.append(LEFT)
            else:
                genes.append(RIGHT)
        dnas.append(genes)
    return dnas

#create robots with genes
def createRobots(dnas):
    robots = []
    for dna in dnas:
        robots.append(Robot(dna))
    return robots

#insert robots into the Simulation
def insertRobots(robots):
    for robot in robots:
        Simulation.addAgent(simulation,robot)

#chose two best robots
def choseTwoBestRobots(robots):
    bestRobots = []
    bestRobots.append(robots[0])
    bestRobots.append(robots[1])
    for robot in robots:
        if robot.GetDistance() < bestRobots[0].GetDistance():
            bestRobots[0] = robot
        elif robot.GetDistance() < bestRobots[1].GetDistance():
            bestRobots[1] = robot
    return bestRobots

#colect genes from best robots 
def colectGenes(bestRobots):
    dna = []
    for robot in bestRobots:
        genes = []
        for gene in robot.genes:
            genes.append(gene)
        dna.append(genes)
    return dna
#clone dna
def cloneDna(dna):
    newDna = []
    for genes in dna:
        newGenes = []
        for gene in genes:
            newGenes.append(gene)
        newDna.append(newGenes)
    return newDna

#crossover de genes in dna
def crossover(dna):
    clonedDna = cloneDna(dna)
    newGenes = []
    for i in range(movimentosNum):
        if i%2 == 0:
            newGenes.append(clonedDna[0][i])
        else:
            newGenes.append(clonedDna[1][i])
    return newGenes

#cloneGenes
def cloneGenes(genes):
    newGenes = []
    for gene in genes:
        newGenes.append(gene)
    return newGenes

#mutiply genes and randomize them
def mutate(baseGenes):
    newGenes = cloneGenes(baseGenes)
    dnas = []
    for i in range(robotNum):
        genes = []
        for j in range(movimentosNum):  
            decision = randint(0,10)
            if decision == 0:
                genes.append(UP)
            elif decision == 1:
                genes.append(DOWN)
            elif decision == 2:
                genes.append(LEFT)
            elif decision == 3:
                genes.append(RIGHT)
            else:
                genes.append(newGenes[j])
        dnas.append(genes)
    return dnas

dnas = createRandomGenes()
robots = createRobots(dnas)
insertRobots(robots)
simulation.run()
while True:
    robots = choseTwoBestRobots(robots)
    dnas = colectGenes(robots)
    simulation.clearAgents()
    genes = crossover(dnas)
    dnas = mutate(genes)
    robots = createRobots(dnas)
    insertRobots(robots)
    simulation.run()