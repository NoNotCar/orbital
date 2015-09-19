'''
Created on 13 Aug 2015

@author: NoNotCar
'''
import pygame
# import pygame._view
import sys
import UniJoy

screen = pygame.display.set_mode((400, 256))

import Img
from Enemies import *


def die(screen):
    pygame.mixer.music.stop()
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.fill((0, 0, 0))
    Img.bcentre(Img.bfont, "FOOL", screen, col=(255, 255, 255))
    pygame.display.flip()
    pygame.time.wait(1000)


def Instruct(instructions, time):
    words = instructions.split()
    text = ""
    for i in range(len(words)):
        pygame.event.pump()
        if i:
            text += " "
        text += words[i]
        screen.fill((255, 255, 255))
        Img.bcentre(Img.dfont, text, screen, col=(0, 0, 0))
        pygame.display.flip()
        pygame.time.wait(time)


class Player(object):
    def __init__(self):
        self.radius = 100
        self.angle = 0.0
        self.direction = 1
        self.speedmult = 1
        self.lasedown = 0

    def get_x(self):
        return int(round(self.radius * math.sin(math.radians(self.angle)))) + 128

    def get_y(self):
        return int(round(self.radius * math.cos(math.radians(self.angle)))) + 128

    def get_speed(self):
        return self.radius ** -1 * 100 * self.speedmult


levels = (([Asteroid], 15, 1), ([Asteroid, BigAsteroid], 20, 1.5), ([Hostage, Asteroid], 30, 1),
          ([BigAsteroid, SmallAsteroid], 30, 2), ([MustShoot], 30, 1),
          ([Asteroid, Obstacle], 30, 1), ([Obstacle2], 30, 1), ([EnemyShip], 30, 1), ([Ranged], 30, 1),
          ([Obstacle, MustShoot], 30, 1.5), ([EnemyShip2], 60, 2))
level = 0
jnum = pygame.joystick.get_count()
unijs = [UniJoy.Unijoy(n) for n in range(jnum)]
assert jnum>0,"NOT ENOUGH CONTROLLERS"
Instruct("UP/DOWN TO MOVE", 500)
pygame.time.wait(500)
Instruct("SHOOT WITH A", 500)
while True:
    p = Player()
    c = pygame.time.Clock()
    obstacles = []
    plasers = []
    score = 0
    tick = 0
    dead = False
    if level == 4:
        Instruct("MUST SHOOT YELLOW", 500)
    elif level == 5:
        Instruct("RED IS IMMORTAL", 500)
    elif level == 2:
        Instruct("DON'T SHOOT PINK", 500)
    elif level == len(levels) - 1:
        Instruct("ULTIMATE DEFENCE", 1000)
    p.speedmult = levels[level][2]
    if level != 9:
        Instruct("LEVEL " + str(level + 1), 500)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((255, 255, 255) if level != len(levels) - 1 else (255, 150, 0))
        for obsc in levels[level][0]:
            obsc.generate(obstacles)
        ujdir = 0
        for uj in unijs:
            ujd = uj.getdirstick(1)
            if ujd:
                ujdir -= ujd[1]
        if ujdir < -(jnum // 2):
            if p.radius > 30:
                p.radius -= 1
        elif ujdir > jnum // 2:
            if p.radius < 100:
                p.radius += 1
        if any([uj.get_b("A") for uj in unijs]) and not p.lasedown:
            plasers.append([p.get_x() - 8, p.get_y() - 2])
            p.lasedown = 20
        if p.lasedown > 0:
            p.lasedown -= 1
        pygame.draw.circle(screen, (127, 127, 127), (128, 128), p.radius, 1)
        orects = []
        plrects = []
        for obstacle in obstacles:
            orects.append((pygame.draw.rect(screen, obstacle.col,
                                            pygame.Rect(obstacle.x, obstacle.y, obstacle.w, obstacle.h)), obstacle))
            obstacle.update(obstacles)
        for pos in plasers:
            plrects.append(pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(pos[0], pos[1], 16, 4)))
            pos[0] += 4
        prect = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(p.get_x() - 8, p.get_y() - 8, 16, 16))
        for ore in [o for o in orects if o[1].plaser]:
            for pr in plrects:
                if ore[0].colliderect(pr):
                    obstacles.remove(ore[1])
                    if ore[1].hostage:
                        die(screen)
                        dead = True
        for ore in orects:
            if ore[1].isdeadly and ore[0].colliderect(prect):
                die(screen)
                dead = True
        for obstacle in obstacles:
            if obstacle.x <= -obstacle.w:
                if not obstacle.deadgooff:
                    obstacles.remove(obstacle)
                else:
                    die(screen)
                    dead = True
        if dead:
            break
        for ore in orects:
            if not ore[1].isdeadly and ore[0].colliderect(prect):
                obstacles.remove(ore[1])
        for pos in plasers:
            if pos[0] > 400:
                plasers.remove(pos)
        p.angle = (p.angle - p.get_speed()) % 360
        pygame.display.flip()
        c.tick(60)
        if tick == 60:
            score += 1
            tick = 0
            if score == levels[level][1]:
                pygame.mixer.music.stop()
                Instruct("WELL DONE", 500)
                level += 1
                if level == 10:
                    Instruct("YOU WIN!", 2000)
                    sys.exit()
                break
        else:
            tick += 1
