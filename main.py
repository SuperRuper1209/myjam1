import math
import cells
from cells import *
from copy import deepcopy
import json
from PIL import Image, ImageFilter
from menu import *

pygame.font.init()

roboto_thin = pygame.font.Font("assets/Roboto-Thin.ttf", 100)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenDimensions = screen.get_size()
clock = pygame.time.Clock()
pygame.display.set_caption("the game where you plan and then execute", "haha yes")
pygame.display.set_icon(pygame.image.load("assets/buttons/play_instructions.png"))

cellSize = int(convertDimensions((cellSize, cellSize), screenDimensions)[0])
instructionCellSize = cellSize * 2
cells.cellSize = cellSize

running = True
FPS = 60

buttonImages = {
    "stop": pygame.transform.scale(pygame.image.load("assets/buttons/stop_instructions.png").convert_alpha(),
                                   (instructionCellSize, instructionCellSize)).convert_alpha(),
    "step": pygame.transform.scale(pygame.image.load("assets/buttons/step_instructions.png").convert_alpha(),
                                   (instructionCellSize, instructionCellSize)).convert_alpha(),
    "play": pygame.transform.scale(pygame.image.load("assets/buttons/play_instructions.png").convert_alpha(),
                                   (instructionCellSize, instructionCellSize)).convert_alpha(),
    "back": pygame.transform.scale(backButton, (convertDimensions((60, 60), screen.get_size())))
}


class Player:
    def __init__(self, pos, direction, level):
        self.pos = pos
        self.originalPos = pos

        self.direction = direction
        self.originalDirection = direction

        self.level = level

    def move(self, direction):
        newPos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
        if 0 <= newPos[0] <= len(self.level.grid) and 0 <= newPos[1] <= len(self.level.grid[0]):
            cell = self.level.grid[newPos[0]][newPos[1]]
            interact = cell.interact(self.pos)
            if interact == 0:
                self.pos = newPos

    def render(self, surf):
        renderPos = ((self.pos[0] + 0.5) * (cellSize - 1) + 1, (self.pos[1] + 0.5) * (cellSize - 1) + 1)
        pygame.draw.circle(surf, (0, 0, 0), renderPos, cellSize / 4)
        pygame.draw.line(surf, (125, 125, 255), renderPos, (renderPos[0]+math.cos(self.direction / 180 * math.pi)*cellSize/2.2,
                                                          renderPos[1]+math.sin(self.direction / 180 * math.pi)*cellSize/2.2))


class Level:
    def __init__(self, grid, playerStartPos, finishPos, playerDirection, max_instructions, allowed_instructions):
        self.originalGrid = grid
        self.grid = deepcopy(grid)
        for column in self.grid:
            for cell in column:
                cell.initialize(self)
        self.pixelGridSize = (
            len(self.grid) * cellSize, len(self.grid[0]) * cellSize)
        self.offset = (
            screenDimensions[0] / 2 - self.pixelGridSize[0] / 2, screenDimensions[1] / 2 - self.pixelGridSize[1] / 2)
        self.player = Player(playerStartPos, playerDirection, self)
        self.finishPos = finishPos

        self.allowed_instructions = allowed_instructions
        self.instructionBar = [None for _ in range(0, max_instructions)]

        self.instructionSurf = self.bakeInstructionSurface()
        self.instructionBarSurf = self.bakeBar()

        self.win = False
        self.restart2 = False

    def render(self):
        gridSurf = pygame.Surface(self.pixelGridSize, pygame.SRCALPHA, 32).convert_alpha()
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                self.grid[x][y].render(gridSurf)

        pygame.draw.circle(gridSurf, (0, 255, 0), ((self.finishPos[0]+0.5)*(cellSize-1)+1, (self.finishPos[1]+0.5)*(cellSize-1)+1), cellSize//3)

        return gridSurf

    def reset(self):
        self.grid = deepcopy(self.originalGrid)
        for column in self.grid:
            for cell in column:
                cell.initialize(self)

        self.player = Player(self.player.originalPos, self.player.originalDirection, self)
        self.instructionBar = [None for _ in range(0, len(self.instructionBar))]
        self.instructionBarSurf = self.bakeBar()
        self.win = False
        self.restart2 = False

    def restart(self):
        self.grid = deepcopy(self.originalGrid)
        for column in self.grid:
            for cell in column:
                cell.initialize(self)

        self.player = Player(self.player.originalPos, self.player.originalDirection, self)
        self.win = False
        self.restart2 = False

    def bakeInstructionSurface(self):
        surf = pygame.Surface((min(len(self.allowed_instructions), 3) * instructionCellSize,
                               ((len(self.allowed_instructions) - 1) // 3 + 1) * instructionCellSize), pygame.SRCALPHA,
                              32).convert_alpha()
        for i, instruction in enumerate(self.allowed_instructions):
            x, y = i % 3, i // 3
            pygame.draw.rect(surf, (0, 0, 0), (
                x * (instructionCellSize - 1), y * (instructionCellSize - 1), instructionCellSize, instructionCellSize),
                             1)
            img = instructions["unknown"]
            if instruction in instructions.keys():
                img = instructions[instruction]
            surf.blit(img, (x * (instructionCellSize - 1), y * (instructionCellSize - 1)))

        return surf

    def bakeBar(self):
        surf = pygame.Surface((instructionCellSize * len(self.instructionBar), instructionCellSize), pygame.SRCALPHA,
                              32).convert_alpha()
        for i, instruction in enumerate(self.instructionBar):
            pygame.draw.rect(surf, (0, 0, 0),
                             (i * (instructionCellSize - 1), 0, instructionCellSize, instructionCellSize), 1)
            if instruction is not None:
                img = instructions["unknown"]
                if instruction in instructions.keys():
                    img = instructions[instruction]
                surf.blit(img, (i * (instructionCellSize - 1), 0))
        return surf

    def tick(self):
        listOfCells = []
        for column in self.grid:
            for cell in column:
                listOfCells.append(cell)

        for cell in listOfCells:
            cell.tick()

        if type(self.grid[self.player.pos[0]][self.player.pos[1]]) == EnemyCell:
            self.restart2 = True

        if self.player.pos[0] == self.finishPos[0] and self.player.pos[1] == self.finishPos[1]:
            self.win = True


cellChars["#"] = WallCell
cellChars[" "] = AbstractCell
cellChars["E"] = EnemyCell
levels = []

instructions = {}


def load_level(filename):
    lvl = open("levels/" + filename, "r")
    r = lvl.read()
    lvl.close()
    split = r.split("\n")
    levelLine = 0

    lvlVars = {"max_instructions": 5, "allowed_instructions": ["forward"], "player_direction": 0}

    for i, line in enumerate(split):
        if line == "-":
            levelLine = i + 1
            break
        else:
            var, val = line.split("=")
            lvlVars[var] = json.loads(val)
    split = split[levelLine:]
    lvlSize = (len(split[0]), len(split))
    board = [[None for _ in range(lvlSize[1])] for _ in range(lvlSize[0])]
    startPos = None
    finishPos = None

    enemies = 0

    for x in range(0, lvlSize[0]):
        for y in range(0, lvlSize[1]):
            cell = split[y][x]
            if cell in cellChars.keys():
                board[x][y] = cellChars[cell]((x, y))
            else:
                board[x][y] = cellChars[" "]((x, y))

            if cell == "@":
                startPos = (x, y)
            elif cell == "F":
                finishPos = (x, y)
            elif cell == "E":
                enemies += 1
                direction = lvlVars["enemy"+str(enemies)]["direction"]
                board[x][y].uploadData(direction)

    levels.append(Level(board, startPos, finishPos, lvlVars["player_direction"], lvlVars["max_instructions"], lvlVars["allowed_instructions"]))


def instruction_texture_load(instructionName, textureName):
    img = pygame.image.load("assets/instructions/" + textureName + ".png").convert_alpha()
    instructions[instructionName] = pygame.transform.scale(img, (instructionCellSize, instructionCellSize))


instruction_texture_load("forward", "arrow_right")
instruction_texture_load("turnRight", "turnRight")
instruction_texture_load("turnLeft", "turnLeft")
instruction_texture_load("unknown", "question_mark")
instruction_texture_load("loop", "loop")
instruction_texture_load("loopLimiter", "loopLimiter")
instruction_texture_load("exitLoop", "loopExit")
instruction_texture_load("exitWallLoop", "wallLoopExit")
instruction_texture_load("exitAirLoop", "airLoopExit")

load_level("level1")
load_level("level2")
load_level("level3")
load_level("level4")
load_level("level5")
load_level("level6")
load_level("level7")
load_level("level8")


def game(levelId):
    global running

    initialStuff = {
        "nestedLoopData": [],
        "instructionPointer": -1
    }
    stuff = deepcopy(initialStuff)

    prevTime = time.time() - 1 / FPS

    level: Level = levels[levelId]
    level.reset()

    gridSurf = level.render()
    update = True

    instructionListPos = ((screenDimensions[0] + level.offset[0] + gridSurf.get_width()) / 2, screenDimensions[1] / 2)
    instructionListPos = (instructionListPos[0] - level.instructionSurf.get_width() / 2,
                          instructionListPos[1] - level.instructionSurf.get_height() / 2)
    instructionBarPos = (screenDimensions[0] / 2, (screenDimensions[1] + level.offset[1] + gridSurf.get_height()) / 2)
    instructionBarPos = (instructionBarPos[0] - level.instructionBarSurf.get_width() / 2 - instructionCellSize * 2,
                         instructionBarPos[1] - level.instructionBarSurf.get_height() / 2)

    buttons = (
        (instructionBarPos[0] + level.instructionBarSurf.get_width() + instructionCellSize * 1, instructionBarPos[1]),  # play + stop
        (instructionBarPos[0] + level.instructionBarSurf.get_width() + instructionCellSize * 3, instructionBarPos[1])   # step
    )

    stepMode = 0

    instructionDelay = [0, 0.15]  # instruction delay

    firstFrame = 51

    def process_instruction(level, instr):
        if instr == "forward":
            level.player.move((round(math.cos(level.player.direction / 180 * math.pi)),
                               round(math.sin(level.player.direction / 180 * math.pi))))
            level.tick()
        elif instr == "turnRight":
            level.player.direction += 90
            level.tick()
        elif instr == "turnLeft":
            level.player.direction -= 90
            level.tick()
        elif instr == "loop":
            stuff["nestedLoopData"].append(stuff["instructionPointer"])
        elif instr == "loopLimiter":
            if len(stuff["nestedLoopData"]) > 0:
                stuff["instructionPointer"] = stuff["nestedLoopData"][len(stuff["nestedLoopData"])-1]
        elif instr == "exitLoop" or "exitWallLoop" or "exitAirLoop":
            cond = False
            if instr == "exitWallLoop":
                newPos = (level.player.pos[0]+math.cos(level.player.direction/180*math.pi), level.player.pos[1]+math.sin(level.player.direction/180*math.pi))
                if type(level.grid[round(newPos[0])][round(newPos[1])]) == WallCell:
                    cond = True
            elif instr == "exitAirLoop":
                newPos = (level.player.pos[0]+math.cos(level.player.direction/180*math.pi), level.player.pos[1]+math.sin(level.player.direction/180*math.pi))
                if type(level.grid[round(newPos[0])][round(newPos[1])]) == AbstractCell:
                    cond = True
            if instr == "exitLoop" or cond:
                stuff["nestedLoopData"] = stuff["nestedLoopData"][:-1]
                pointer1 = stuff["instructionPointer"]
                while 1:
                    stuff["instructionPointer"] += 1
                    if level.instructionBar[stuff["instructionPointer"]] == "loopLimiter":
                        pointer1 = stuff["instructionPointer"]
                        break
                    if len(level.instructionBar) == stuff["instructionPointer"]:
                        break
                stuff["instructionPointer"] = pointer1
            level.tick()

    while running:
        dt = time.time() - prevTime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()

                if 0 <= mousePos[0] - buttons[0][0] <= instructionCellSize and 0 <= mousePos[1] - buttons[0][1] <= instructionCellSize:
                    if stuff["instructionPointer"] == -1:
                        stuff["instructionPointer"] = 0
                        stepMode = 0
                    else:
                        level.restart()
                        stuff = deepcopy(initialStuff)
                        update = True
                        stuff["instructionPointer"] = -1
                elif 0 <= mousePos[0] - buttons[1][0] <= instructionCellSize and 0 <= mousePos[1] - buttons[1][1] <= instructionCellSize:
                    if stuff["instructionPointer"] == -1:
                        stuff["instructionPointer"] = 0
                        stepMode = 1
                        process_instruction(level, level.instructionBar[stuff["instructionPointer"]])
                        update = True
                    else:
                        if stuff["instructionPointer"] < len(level.instructionBar)-1:
                            stuff["instructionPointer"] += 1
                            process_instruction(level, level.instructionBar[stuff["instructionPointer"]])
                            update = True
                        else:
                            level.restart()
                            stuff = deepcopy(initialStuff)
                            update = True
                            stuff["instructionPointer"] = -1

                if stuff["instructionPointer"] == -1:
                    if 0 <= mousePos[0] - instructionListPos[0] <= level.instructionSurf.get_width() and 0 <= mousePos[
                        1] - \
                            instructionListPos[1] <= level.instructionSurf.get_height():
                        relativePos = (mousePos[0] - instructionListPos[0], mousePos[1] - instructionListPos[1])
                        cellPos = (relativePos[0] // instructionCellSize, relativePos[1] // instructionCellSize)
                        if cellPos[0] + cellPos[1] * 3 <= len(level.allowed_instructions) - 1:
                            instr = level.allowed_instructions[int(cellPos[0] + cellPos[1] * 3)]
                            for i, v in enumerate(level.instructionBar):
                                if v is None:
                                    level.instructionBar[i] = instr
                                    break
                            level.instructionBarSurf = level.bakeBar()
                    elif 0 <= mousePos[0] - instructionBarPos[0] <= level.instructionBarSurf.get_width() and 0 <= \
                            mousePos[1] - \
                            instructionBarPos[1] <= level.instructionBarSurf.get_height():
                        cellPos = int((mousePos[0] - instructionBarPos[0]) // instructionCellSize)
                        level.instructionBar[cellPos] = None
                        level.instructionBarSurf = level.bakeBar()

        if stepMode == 0 and stuff["instructionPointer"] != -1:
            instructionDelay[0] += dt
            if instructionDelay[0] >= instructionDelay[1]:
                instructionDelay[0] = 0
                if stuff["instructionPointer"] < len(level.instructionBar):
                    process_instruction(level, level.instructionBar[stuff["instructionPointer"]])
                    update = True
                    stuff["instructionPointer"] += 1

        if level.restart2:
            level.restart()
            stuff = deepcopy(initialStuff)
            stuff["instructionPointer"] = -1

        screen.fill((255, 255, 255))

        if update:
            gridSurf = level.render()
            level.player.render(gridSurf)

        screen.blit(level.instructionBarSurf, instructionBarPos)
        if stuff["instructionPointer"] > -1:
            pygame.draw.rect(screen, (0, 255, 0), (
                instructionBarPos[0] + (instructionCellSize - 1) * min(stuff["instructionPointer"], len(level.instructionBar)-1) - 4, instructionBarPos[1] - 4,
                instructionCellSize + 8, instructionCellSize + 8), 5)

        screen.blit(gridSurf, level.offset)
        screen.blit(level.instructionSurf, instructionListPos)

        if stuff["instructionPointer"] == -1:
            screen.blit(buttonImages["play"], (buttons[0][0], buttons[0][1]))
            screen.blit(buttonImages["step"], (buttons[1][0], buttons[1][1]))
        else:
            screen.blit(buttonImages["stop"], (buttons[0][0], buttons[0][1]))
            if stepMode == 1:
                screen.blit(buttonImages["step"], (buttons[1][0], buttons[1][1]))

        hover = 0 <= pygame.mouse.get_pos()[0] <= buttonImages["back"].get_width() + 4 and 0 <= pygame.mouse.get_pos()[
            1] <= buttonImages["back"].get_height() + 4
        backButtonColor = (255, 255, 255)
        if hover:
            backButtonColor = (200, 200, 200)

        screen.fill(backButtonColor,
                    (0, 0, buttonImages["back"].get_width() + 4, buttonImages["back"].get_height() + 4))
        screen.blit(buttonImages["back"], (2, 2))
        pygame.draw.rect(screen, (0, 0, 0),
                         (0, 0, buttonImages["back"].get_width() + 4, buttonImages["back"].get_height() + 4), 2)

        if firstFrame > 0:
            blackOverlay = pygame.Surface(screenDimensions, pygame.SRCALPHA, 32)
            blackOverlay.fill((0, 0, 0, 255 * firstFrame / 51))
            screen.blit(blackOverlay, (0, 0))
            firstFrame -= 1

        if hover and pygame.mouse.get_pressed()[0]:
            lastImg = screen.copy()
            for a in range(0, 101):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return -1

                b = a / 100
                screen.blit(lastImg, (0, 0))
                surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
                surf.fill((0, 0, 0, b * 255))
                screen.blit(surf, (0, 0))
                pygame.display.update()
                time.sleep(0.5 / 101)
            return -2

        if level.win:
            break

        pygame.display.update()
        prevTime = time.time()
        update = False
        clock.tick(FPS)

    if running:
        data = pygame.image.tostring(screen, "RGB")

        origImg = Image.frombytes("RGB", screenDimensions, data)
        txt = roboto_thin.render('Level completed!', True, (50, 155, 50))
        width = convertDimensions(txt.get_size(), screenDimensions)[0]
        height = width/(txt.get_width()/txt.get_height())
        txt = pygame.transform.scale(txt, (width, height))

        lastImg = None
        for i in range(0, 7):
            br = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    br = True
                    break
            if br:
                break
            lastImg = pygame.image.fromstring(origImg.filter(ImageFilter.GaussianBlur(radius=i)).tobytes(), screenDimensions, "RGB")
            screen.blit(lastImg, (0, 0))
            pygame.display.update()
            time.sleep(.1)

        for a in range(0, 101):
            br = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    br = True
                    break
            if br:
                break

            b = a/100*math.pi
            b = (-math.cos(b)+1)/2

            screen.blit(lastImg, (0, 0))
            screen.blit(txt, (screenDimensions[0] / 2 - txt.get_width() / 2, (screenDimensions[1] / 2 + txt.get_height()/2) * b - txt.get_height()))
            pygame.display.update()
            time.sleep(1/101)

        for i in range(0, 50):
            br = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    br = True
                    break
            if br:
                break
            time.sleep(1/50)

        for a in range(0, 101):
            br = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    br = True
                    break
            if br:
                break

            b = a/100
            screen.blit(lastImg, (0, 0))
            screen.blit(txt, (screenDimensions[0]/2 - txt.get_width()/2, (screenDimensions[1] / 2 - txt.get_height()/2)))
            surf = pygame.Surface(screenDimensions, pygame.SRCALPHA, 32)
            surf.fill((0, 0, 0, b*255))
            screen.blit(surf, (0, 0))
            pygame.display.update()
            time.sleep(0.5/101)
        return levelId+1
    else:
        return -1


while running:
    ret = menu(screen)
    if ret == -1:
        running = False
    else:
        while running:
            ret = game(ret)
            if len(levels) == ret:
                ret = creditsMenu2(screen)
                if ret == -1:
                    running = False
                break
            if ret == -1:
                running = False
            elif ret == -2:
                break
