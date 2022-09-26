import pygame
from utils import *
import time

titleImg = pygame.image.load('assets/title.png')
clock = pygame.time.Clock()

pygame.font.init()

mainFont = pygame.font.Font('assets/Roboto-Thin.ttf', 300)

backButton = pygame.image.load("assets/buttons/back.png")


class button:
    def __init__(self, borderColor=(0, 0, 0), borderSize=1, text="", backgroundColor=(255, 255, 255),
                 textColor=(0, 0, 0), font=mainFont, size=(400, 100), pos=(0, 0)):
        self.borderColor = borderColor
        self.borderSize = borderSize
        self.text = text
        self.textColor = textColor
        self.font = font
        self.backgroundColor = backgroundColor
        self.size = size
        self.pos = pos

        self.badPress = False

    def render(self):
        pos = pygame.mouse.get_pos()

        hover = 0 <= pos[0] - self.pos[0] <= self.size[0] and 0 <= pos[1] - self.pos[1] <= self.size[1]
        pressed = pygame.mouse.get_pressed()[0]

        backgroundColor = self.backgroundColor

        if not pressed:
            self.badPress = False

        if pressed and not hover:
            self.badPress = True
        elif pressed is True and hover is True and self.badPress is True:
            pressed = False

        if hover:
            backgroundColor = (self.backgroundColor[0] + 25, self.backgroundColor[1] + 25, self.backgroundColor[2] + 25)
            if pressed:
                backgroundColor = (
                    self.backgroundColor[0] + 50, self.backgroundColor[1] + 50, self.backgroundColor[2] + 50)

        surf = pygame.Surface(self.size)
        surf.fill(backgroundColor)
        if self.borderSize > 0:
            pygame.draw.rect(surf, self.borderColor, (0, 0, self.size[0], self.size[1]), self.borderSize)
        txtR = self.font.render(self.text, True, self.textColor)
        height = self.size[1] - self.borderSize * 2 - 10
        width = height / (txtR.get_height() / txtR.get_width())
        txtR = pygame.transform.scale(txtR, (width, height))

        surf.blit(txtR, (self.size[0] / 2 - width / 2, self.size[1] / 2 - height / 2))

        if hover:
            if pressed:
                return surf, 2
            return surf, 1

        return surf, 0


def creditsMenu(screen: pygame.Surface):
    firstFrame = 51
    backButtonResized = pygame.transform.scale(backButton, (convertDimensions((60, 60), screen.get_size())))
    textColor = (0, 0, 0)

    creditsText = [
        mainFont.render("Developer: SuperRuper1209", True, textColor),
        mainFont.render("Made for: private game jam :cat_normal:", True, textColor),
        mainFont.render("Inspiration: Pastaconton(tonnolife)", True, textColor),
        mainFont.render("Best game: this one", True, textColor)
    ]

    surf = pygame.Surface((screen.get_width() * 0.95, screen.get_height() * 0.65), pygame.SRCALPHA, 32)
    textHeight = surf.get_height() / 7
    for i, text in enumerate(creditsText):
        creditsText[i] = pygame.transform.scale(text, (textHeight / (text.get_height() / text.get_width()), textHeight))
        surf.blit(creditsText[i], (0, i * textHeight * 2))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        screen.fill((179, 215, 255))
        screen.blit(surf,
                    (screen.get_width() / 2 - surf.get_width() / 2, screen.get_height() / 2 - surf.get_height() / 2))

        hover = 0 <= pygame.mouse.get_pos()[0] <= backButtonResized.get_width() + 4 and 0 <= pygame.mouse.get_pos()[
            1] <= backButtonResized.get_height() + 4
        backButtonColor = (255, 255, 255)
        if hover:
            backButtonColor = (200, 200, 200)

        screen.fill(backButtonColor, (0, 0, backButtonResized.get_width() + 4, backButtonResized.get_height() + 4))
        screen.blit(backButtonResized, (2, 2))
        pygame.draw.rect(screen, (0, 0, 0),
                         (0, 0, backButtonResized.get_width() + 4, backButtonResized.get_height() + 4), 2)

        if firstFrame > 0:
            blackOverlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
            blackOverlay.fill((0, 0, 0, 255 * firstFrame / 51))
            screen.blit(blackOverlay, (0, 0))
            firstFrame -= 1

        pygame.display.update()

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
            return

        clock.tick(60)


def creditsMenu2(screen: pygame.Surface):
    firstFrame = 51
    backButtonResized = pygame.transform.scale(backButton, (convertDimensions((60, 60), screen.get_size())))
    textColor = (0, 0, 0)

    creditsText = [
        mainFont.render("Developer: SuperRuper1209", True, textColor),
        mainFont.render("Made for: private game jam :cat_normal:", True, textColor),
        mainFont.render("Inspiration: Pastaconton(tonnolife)", True, textColor),
        mainFont.render("Best game: this one", True, textColor)
    ]

    thxForPlaying = mainFont.render("THANKS FOR PLAYING!", True, (25, 100, 25))

    surf = pygame.Surface((screen.get_width() * 0.95, screen.get_height()), pygame.SRCALPHA, 32)
    textHeight = surf.get_height()*0.5 / 7
    for i, text in enumerate(creditsText):
        creditsText[i] = pygame.transform.scale(text, (textHeight / (text.get_height() / text.get_width()), textHeight))
        surf.blit(creditsText[i], (textHeight, i * textHeight * 2+textHeight))

    surf.blit(pygame.transform.scale(thxForPlaying, (surf.get_height()*0.5*0.35/(thxForPlaying.get_height()/thxForPlaying.get_width()), surf.get_height()*0.5*0.35)), (surf.get_width()*0.5-(surf.get_height()*0.5*0.35/(thxForPlaying.get_height()/thxForPlaying.get_width()))/2, surf.get_height()*0.8))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        screen.fill((179, 215, 255))
        screen.blit(surf,
                    (screen.get_width() / 2 - surf.get_width() / 2, screen.get_height() / 2 - surf.get_height() / 2))

        hover = 0 <= pygame.mouse.get_pos()[0] <= backButtonResized.get_width() + 4 and 0 <= pygame.mouse.get_pos()[
            1] <= backButtonResized.get_height() + 4
        backButtonColor = (255, 255, 255)
        if hover:
            backButtonColor = (200, 200, 200)

        screen.fill(backButtonColor, (0, 0, backButtonResized.get_width() + 4, backButtonResized.get_height() + 4))
        screen.blit(backButtonResized, (2, 2))
        pygame.draw.rect(screen, (0, 0, 0),
                         (0, 0, backButtonResized.get_width() + 4, backButtonResized.get_height() + 4), 2)

        if firstFrame > 0:
            blackOverlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
            blackOverlay.fill((0, 0, 0, 255 * firstFrame / 51))
            screen.blit(blackOverlay, (0, 0))
            firstFrame -= 1

        pygame.display.update()

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
            return

        clock.tick(60)


def levelSelect(screen: pygame.Surface):
    firstFrame = 51
    backButtonResized = pygame.transform.scale(backButton, (convertDimensions((60, 60), screen.get_size())))
    textColor = (0, 0, 0)


def menu(screen: pygame.Surface):  # -1 = quit, other is level id
    titleResized = pygame.transform.scale(titleImg, convertDimensions(titleImg.get_size(), screen.get_size()))
    titlePos = (
        screen.get_size()[0] / 2 - titleResized.get_width() / 2,
        screen.get_size()[1] * 0.2 - titleResized.get_height() / 2)
    firstFrame = 51

    buttonSize = convertDimensions((350, 100), screen.get_size())
    playButton = button(pos=(screen.get_size()[0] / 2 - buttonSize[0] / 2, screen.get_size()[1] * 0.4),
                        size=buttonSize,
                        text="play",
                        backgroundColor=(50, 125, 50))
    creditsButton = button(
        pos=(screen.get_size()[0] / 2 - buttonSize[0] / 2,
             screen.get_size()[1] * 0.4 + buttonSize[1] * 2 - buttonSize[1] / 2),
        size=buttonSize,
        text="credits",
        backgroundColor=(50, 125, 50))
    exitButton = button(
        pos=(screen.get_size()[0] / 2 - buttonSize[0] / 2,
             screen.get_size()[1] * 0.4 + buttonSize[1] * 3.5 - buttonSize[1] / 2),
        size=buttonSize,
        text="exit",
        backgroundColor=(125, 50, 50))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        buttonRendered, buttonState = playButton.render()
        exitButtonRendered, exitButtonState = exitButton.render()
        creditsButtonRendered, creditsButtonState = creditsButton.render()

        screen.fill((179, 215, 255))
        screen.blit(titleResized, titlePos)
        screen.blit(buttonRendered, playButton.pos)
        screen.blit(creditsButtonRendered, creditsButton.pos)
        screen.blit(exitButtonRendered, exitButton.pos)

        if firstFrame > 0:
            blackOverlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
            blackOverlay.fill((0, 0, 0, 255 * firstFrame / 51))
            screen.blit(blackOverlay, (0, 0))
            firstFrame -= 1

        pygame.display.update()

        if exitButtonState == 2:
            return -1
        elif creditsButtonState == 2:
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
            ret = creditsMenu(screen)
            firstFrame = 51
            if ret == -1:
                return ret
        elif buttonState == 2:
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
            return 0

        clock.tick(60)
