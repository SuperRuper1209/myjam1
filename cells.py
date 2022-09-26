import pygame

cellSize = 48  # relative pixel size of cells
cellChars = {}


class AbstractCell:
    def __init__(self, pos):
        self.pos = pos
        self.level = None
        self.initialized = False

    def render(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), (self.pos[0]*(cellSize-1), self.pos[1]*(cellSize-1), cellSize, cellSize), 1)

    def interact(self, interactPos):
        return 0

    def initialize(self, level):
        self.level = level
        self.initialized = True

    def tick(self):
        pass

    def __copy__(self):
        c = type(self)((self.pos[0], self.pos[1]))
        return c


class WallCell(AbstractCell):
    def __init__(self, pos):
        super().__init__(pos)

    def render(self, surf):
        pygame.draw.rect(surf, (90, 90, 90), (self.pos[0]*(cellSize-1), self.pos[1]*(cellSize-1), cellSize, cellSize), 0)
        super().render(surf)

    def interact(self, interactPos):
        return 1


class EnemyCell(AbstractCell):
    def __init__(self, pos):
        super().__init__(pos)
        self.direction = None

    def uploadData(self, direction):
        self.direction = direction

    def render(self, surf):
        pygame.draw.rect(surf, (205, 90, 90), (self.pos[0]*(cellSize-1), self.pos[1]*(cellSize-1), cellSize, cellSize), 0)
        super().render(surf)

    def __copy__(self):
        c = type(self)((self.pos[0], self.pos[1]))
        c.uploadData(self.direction)
        return c

    def interact(self, interactPos):
        return 0

    def tick(self):
        newPos = (self.pos[0]+self.direction[0], self.pos[1]+self.direction[1])
        if type(self.level.grid[newPos[0]][newPos[1]]) == AbstractCell:
            absCell = self.level.grid[newPos[0]][newPos[1]]
            self.level.grid[newPos[0]][newPos[1]] = self
            self.level.grid[self.pos[0]][self.pos[1]] = absCell
            self.pos = newPos
        else:
            self.direction = (-self.direction[0], -self.direction[1])
            self.tick()

