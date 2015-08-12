'''
Created on 8 Jul 2015

@author: NoNotCar
'''
import pygame
import sys

screen=pygame.display.set_mode((400,256))

import Img
from Enemies import *

class ReducedYellow(MustShoot):
    pmin=200
    pmax=300
def die(screen):
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.fill((0, 0, 0))
    Img.bcentre(Img.bfont, "FOOL", screen, col=(255, 255, 255))
    pygame.display.flip()
    pygame.time.wait(1000)

def Instruct(instructions,time):
    words=instructions.split()
    text=""
    for i in range(len(words)):
        pygame.event.pump()
        if i:
            text+=" "
        text+=words[i]
        screen.fill((255,255,255))    
        Img.bcentre(Img.dfont, text, screen,col=(0,0,0))
        pygame.display.flip()
        pygame.time.wait(time)
class Player(object):
    def __init__(self):
        self.sx=0.0
        self.sy=0.0
        self.ax=128.0
        self.ay=128.0
        self.lasedown=0
    def get_x(self):
        return int(round(self.ax))
    def get_y(self):
        return int(round(self.ay))
    def get_speed(self):
        return self.radius**-1*100*self.speedmult
    def update(self):
        self.ax+=self.sx
        self.ay+=self.sy

levels=(([ReducedYellow],15,1),([Asteroid,ReducedYellow],15,1),([Asteroid,BigAsteroid,ReducedYellow],20,1.5),([BigAsteroid,SmallAsteroid,ReducedYellow],30,2),
([Obstacle,ReducedYellow],30,1),([Obstacle2,ReducedYellow],30,1),([EnemyShip,ReducedYellow],30,1),([Ranged],30,1),([Obstacle,MustShoot],30,1.5),([EnemyShip2],60,2))
level=0
Instruct("ARROWS TO MOVE", 500)
pygame.time.wait(500)
Instruct("SHOOT WITH SPACE",500)
pygame.time.wait(500)
Instruct("MUST SHOOT YELLOW", 500)
while True:
    p=Player()
    c=pygame.time.Clock()
    obstacles=[]
    plasers=[]
    score=0
    tick=0
    cx=128
    cy=128
    cr=50
    dead=False
    if level==4:
        Instruct("RED IS IMMORTAL", 500)
    elif level==len(levels)-1:
        Instruct("ULTIMATE DEFENCE", 1000)
    p.speedmult=levels[level][2]
    Instruct("LEVEL "+str(level+1),500)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
        screen.fill((255,255,255) if level!=len(levels)-1 else (255,150,0))
        for obsc in levels[level][0]:
            obsc.generate(obstacles)
        keys=pygame.key.get_pressed()
        if (p.ax-cx)**2+(p.ay-cy)**2<cr**2:
            if keys[pygame.K_DOWN]:
                p.sy+=0.1
            elif keys[pygame.K_UP]:
                p.sy-=0.1
            if keys[pygame.K_LEFT]:
                p.sx-=0.1
            elif keys[pygame.K_RIGHT]:
                p.sx+=0.1
        else:
            if p.sx>0: p.sx-=0.1
            elif p.sx<0:p.sx+=0.1
            if p.sy>0:p.sy-=0.1
            elif p.sy<0:p.sy+=0.1
            p.sx=round(p.sx,1)
            p.sy=round(p.sy,1)
        if keys[pygame.K_s] and cy<256-cr:
            cy+=1
        elif keys[pygame.K_w] and cy>cr:
            cy-=1
        if keys[pygame.K_a] and cx>cr:
            cx-=1
        elif keys[pygame.K_d] and cx<400-cr:
            cx+=1
        if keys[pygame.K_SPACE] and not p.lasedown:
            plasers.append([p.get_x()-8,p.get_y()-2])
            p.lasedown=20
        if p.lasedown>0:
            p.lasedown-=1
        orects=[]
        plrects=[]
        p.update()
        pygame.draw.circle(screen, (255,255,255),(cx,cy),cr)
        for obstacle in obstacles:
            orects.append((pygame.draw.rect(screen,obstacle.col,pygame.Rect(obstacle.x,obstacle.y,obstacle.w,obstacle.h)),obstacle))
            obstacle.update(obstacles)
        for pos in plasers:
            plrects.append(pygame.draw.rect(screen,(0,0,255),pygame.Rect(pos[0],pos[1],16,4)))
            pos[0]+=4
        prect=pygame.draw.rect(screen,(0,0,0),pygame.Rect(p.get_x()-8,p.get_y()-8,16,16))
        for ore in [o for o in orects if o[1].plaser]:
            for pr in plrects:
                if ore[0].colliderect(pr):
                    obstacles.remove(ore[1])
        for ore in orects:
            if ore[1].isdeadly and ore[0].colliderect(prect):
                die(screen)
                dead=True
        for obstacle in obstacles:
            if obstacle.x<=-obstacle.w:
                if not obstacle.deadgooff:
                    obstacles.remove(obstacle)
                else:
                    die(screen)
                    dead=True
        if p.get_x()<=-16 or p.get_x()>=400 or p.get_y()<=-16 or p.get_y()>=256:
            die(screen)
            dead=True
        if dead:
            break
        for ore in orects:
            if not ore[1].isdeadly and ore[0].colliderect(prect):
                obstacles.remove(ore[1])
        for pos in plasers:
            if pos[0]>400:
                plasers.remove(pos)
        pygame.display.flip()
        c.tick(60)
        if tick==60:
            score+=1
            tick=0
            if score==levels[level][1]:
                Instruct("WELL DONE", 500)
                level+=1
                if level==10:
                    Instruct("YOU WIN!", 2000)
                    sys.exit()
                break
        else:
            tick+=1
    
