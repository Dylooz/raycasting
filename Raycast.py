import math
import numpy
import pygame

CONFIG = {
    "START_POS": (400, 400),
    "PLAYER_COLOUR": (0, 0, 255),
    "PLAYER_RADIUS": 10,
    "FOV": (math.pi / 2),
    "RESOLUTION": 0.25,
    "ROTATE_SPEED": (math.pi / 360),
    "MOVE_SPEED": 0.5,
    "VIEW_DIST": 300
}

WIDTH = 800

KEYS = {
    1073741904: False, # left
    1073741903: False, # right
           119: False, # w
            97: False, # a
           115: False, # s
           100: False  # d
}

KEY_OPP = {
    1073741904: [1073741903],
    1073741903: [1073741904],
           119: [115],
            97: [100],
           115: [119],
           100: [97]
}

def unitVector(a):
    return numpy.array([math.cos(a), math.sin(a)])

class Player():
    def __init__(self, x=CONFIG["START_POS"][0], y=CONFIG["START_POS"][1]):
        self.pos = numpy.array([float(x), float(y)])
        self.dir = 0
        self.numRays = math.floor(CONFIG["RESOLUTION"] * WIDTH)
        self.rays = []

        for i in range(0, self.numRays):
            self.rays.append(unitVector((i * CONFIG["FOV"] / self.numRays) - (CONFIG["FOV"] / 2)) * CONFIG["VIEW_DIST"]) 

        print(self.rays)
    
    def render(self, colour=CONFIG["PLAYER_COLOUR"], radius=CONFIG["PLAYER_RADIUS"], showFacing=True):
        for ray in self.rays:
            pygame.draw.line(screen, (0, 255, 0), tuple(self.pos), tuple(self.pos + ray))
        pygame.draw.circle(screen, colour, tuple(self.pos), radius)
        if showFacing:
            pygame.draw.line(screen, (0, 0, 0), tuple(self.pos), tuple(self.pos + unitVector(self.dir) * radius))

    def rotateLeft(self, angle=CONFIG["ROTATE_SPEED"]):
        self.dir = (self.dir - angle) % (2 * math.pi)
        self.rays = []
        for i in range(0, self.numRays):
            self.rays.append(unitVector(self.dir + (i * CONFIG["FOV"] / self.numRays) - (CONFIG["FOV"] / 2)) * CONFIG["VIEW_DIST"])

    def rotateRight(self, angle=CONFIG["ROTATE_SPEED"]):
        self.dir = (self.dir + angle) % (2 * math.pi)
        self.rays = []
        for i in range(0, self.numRays):
            self.rays.append(unitVector(self.dir + (i * CONFIG["FOV"] / self.numRays) - (CONFIG["FOV"] / 2)) * CONFIG["VIEW_DIST"])

    def move(self, angle, dist=CONFIG["MOVE_SPEED"]):
        self.pos += (unitVector(angle % (2 * math.pi)) * dist)

    def moveForward(self, dist=CONFIG["MOVE_SPEED"]):
        self.move(self.dir, dist)

    def moveLeft(self, dist=CONFIG["MOVE_SPEED"]):
        self.move(self.dir - (math.pi / 2), dist)

    def moveBackward(self, dist=CONFIG["MOVE_SPEED"]):
        self.move(self.dir + (math.pi), dist)

    def moveRight(self, dist=CONFIG["MOVE_SPEED"]):
        self.move(self.dir + (math.pi / 2), dist)


def preload():
    pass

def processEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
        elif event.type == pygame.KEYDOWN:
            k = event.key
            if k in KEYS.keys():
                KEYS[k] = True
                for ko in KEY_OPP[k]:
                    KEYS[ko] = False
        elif event.type == pygame.KEYUP:
            k = event.key
            if k in KEYS.keys():
                KEYS[k] = False

def update():
    if KEYS[1073741904]:
        player.rotateLeft()
    if KEYS[1073741903]:
        player.rotateRight()
    if KEYS[119]:
        player.moveForward()
    if KEYS[97]:
        player.moveLeft()
    if KEYS[115]:
        player.moveBackward()
    if KEYS[100]:
        player.moveRight()

def draw():
    screen.fill((255, 255, 255), (0, 0, WIDTH, 800))
    player.render()
    screen.fill((255, 255, 255), (WIDTH, 0, 2 * WIDTH, 800))
    pygame.display.flip()

def gameLoop():
    global screen
    screen = pygame.display.set_mode([1600, 800])
    global player
    player = Player()

    running = True
    while running:
        
        processEvents()
        update()
        draw()


def main():
    pygame.init()

    gameLoop()

    pygame.quit()


if __name__ == "__main__":
    main()
