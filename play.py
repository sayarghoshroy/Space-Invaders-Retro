import pygame
import time
import random
from aliens import *
from missiles import *

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("font/calibri.ttf", 90)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 137, 0)
neon = (157, 244, 66)
purple = (139, 29, 145)
grey = (86, 86, 86)
orange = (255, 119, 0)

display_width = 1200
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))

ship_pos = 0
boxes = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]

counter = 0
pygame.display.set_caption('Battle of Honor')


def createMissile(type, position):
    if boxes[1][ship_pos] == 0:
        if type == 0:
            kill_fast = inst_kill()
            boxes[0][ship_pos] = kill_fast
        elif type == 1:
            kill_slow = slow_kill()
            boxes[0][ship_pos] = kill_slow


def make_Alien():
    pickOne = []
    i = 5
    while i < 7:
        j = 0
        while j < 8:
            if boxes[i][j] == 0:
                add_to_list = [i, j]
                pickOne.append(add_to_list)
            j = j + 1
        i = i + 1
    randLocation = random.randint(0, len(pickOne) - 1)
    alien_x = pickOne[randLocation][0]
    alien_y = pickOne[randLocation][1]
    Al = aliens()
    boxes[alien_x][alien_y] = Al


def updateAliens():
    global boxes
    i = 5
    while i < 7:
        j = 0
        while j < 8:
            if boxes[i][j] != 0 and boxes[i][j].__class__.__name__ == 'aliens':
                boxes[i][j].timeLeft = boxes[i][j].timeLeft - 1
                if boxes[i][j].timeLeft == 0:
                    boxes[i][j] = 0
            j = j + 1
        i = i + 1
    return


def updateMissiles():
    global boxes
    global counter
    i = 6
    while i >= 0:
        j = 0
        while j < 8:
            if boxes[i][j] != 0 and boxes[
                    i][j].__class__.__name__ == 'inst_kill':
                if i == 6:
                    boxes[i][j] = 0
                elif boxes[i + 1][j] != 0 and boxes[
                        i + 1][j].__class__.__name__ == 'aliens':
                    boxes[i + 1][j] = boxes[i][j] = 0
                    counter = counter + 1
                else:
                    boxes[i + 1][j] = boxes[i][j]
                    boxes[i][j] = 0
            if boxes[i][j] != 0 and boxes[
                    i][j].__class__.__name__ == 'slow_kill':
                if i == 6:
                    boxes[i][j] = 0
                elif i == 5 and boxes[6][j] == 0:
                    boxes[i][j] = 0
                elif boxes[i + 1][j] != 0 and boxes[
                        i + 1][j].__class__.__name__ == 'aliens':
                    boxes[i + 1][j].state = 1
                    boxes[i + 1][j].timeLeft = boxes[i + 1][j].timeLeft + 5
                    boxes[i][j] = 0
                elif boxes[i + 2][j] != 0 and boxes[
                        i + 2][j].__class__.__name__ == 'aliens':
                    boxes[i + 2][j].state = 1
                    boxes[i + 2][j].timeLeft = boxes[i + 2][j].timeLeft + 5
                    boxes[i][j] = 0
                else:
                    boxes[i + 2][j] = boxes[i][j]
                    boxes[i][j] = 0
            j = j + 1
        i = i - 1


def gameOn():
    gameExit = False
    global ship_pos

    make_an_alien = pygame.USEREVENT + 1
    update = pygame.USEREVENT + 2
    pygame.time.set_timer(make_an_alien, 10000)
    pygame.time.set_timer(update, 1000)
    make_Alien()

    while not gameExit:

        for event in pygame.event.get():
            if event.type == make_an_alien:
                make_Alien()
            if event.type == update:
                updateAliens()
                updateMissiles()
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print "Your Final Score: " + str(counter)
                    gameExit = True
                elif event.key == pygame.K_a and ship_pos != 0:
                    ship_pos = ship_pos - 1
                elif event.key == pygame.K_d and ship_pos != 7:
                    ship_pos = ship_pos + 1
                elif event.key == pygame.K_SPACE:
                    createMissile(0, ship_pos)
                elif event.key == pygame.K_s:
                    createMissile(1, ship_pos)

        gameDisplay.fill(black)
        i = 0
        while i < 7:
            j = 0
            while j < 8:
                pygame.draw.rect(gameDisplay, neon, [
                                 j * 60 + 20, i * 60 + 20, 50, 50])
                if boxes[6 - i][j].__class__.__name__ == "aliens":
                    if boxes[6 - i][j].state == 0:
                        pygame.draw.rect(gameDisplay, neon, [
                                         j * 60 + 20, i * 60 + 20, 50, 50])
                        pygame.draw.circle(
                            gameDisplay, red, (j * 60 + 45, i * 60 + 45), 25)
                    elif boxes[6 - i][j].state == 1:
                        pygame.draw.rect(gameDisplay, neon, [
                                         j * 60 + 20, i * 60 + 20, 50, 50])
                        pygame.draw.circle(
                            gameDisplay, green, (j * 60 + 45, i * 60 + 45), 25)
                if boxes[6 - i][j].__class__.__name__ == "inst_kill":
                    pygame.draw.rect(gameDisplay, purple, [
                                     j * 60 + 35, i * 60 + 20, 20, 50])
                if boxes[6 - i][j].__class__.__name__ == "slow_kill":
                    pygame.draw.rect(gameDisplay, orange, [
                                     j * 60 + 35, i * 60 + 20, 20, 50])
                j = j + 1
            i = i + 1
        i = 7
        j = 0
        while j < 8:
            pygame.draw.rect(gameDisplay, neon, [
                             j * 60 + 20, i * 60 + 20, 50, 50])
            j = j + 1
        pygame.draw.polygon(gameDisplay, grey, [(
            ship_pos * 60 + 20, 70 + 7 * 60), (
            ship_pos * 60 + 70, 70 + 7 * 60), (
            ship_pos * 60 + 45, 80 + 6 * 60)])
        text = font.render("Score: " + str(counter), True, white)
        gameDisplay.blit(text, [display_width * 4 / 7, display_height * 1 / 4])
        pygame.display.update()
        clock.tick(45)


gameOn()
