'''
Created on 8 Jul 2015

@author: NoNotCar
'''
import math
import random
class Obstacle(object):
    isdeadly=True
    col=(255,0,0)
    ttgo=0
    deadgooff=False
    plaser=False
    hostage=False
    h=16
    w=16
    pmin=60
    pmax=120
    @classmethod
    def generate(cls,obs):
        if cls.ttgo==0:
            obs.append(cls(random.randint(0,240)))
            cls.ttgo=random.randint(cls.pmin,cls.pmax)
        else:
            cls.ttgo-=1
    def __init__(self,y):
        self.x=400
        self.y=y
    def update(self,obs):
        self.x-=1
class Obstacle2(Obstacle):
    @classmethod
    def generate(cls,obs):
        if cls.ttgo==0:
            obs.append(cls())
            cls.ttgo=random.randint(cls.pmin,cls.pmax)
        else:
            cls.ttgo-=1
    def __init__(self):
        self.t=random.randint(0,360)
        self.x=400
        self.y=int(round(100*math.cos(math.radians(self.t))))+128
    def update(self,obs):
        self.t=(self.t+1)%360
        self.x-=1
        self.y=int(round(100*math.cos(math.radians(self.t))))+128
class Asteroid(Obstacle):
    plaser=True
    col=(130,130,130)
    pmin=30
    pmax=60
class MustShoot(Obstacle):
    ttgo=0
    pmin=100
    pmax=200
    @classmethod
    def generate(cls,obs):
        if cls.ttgo==0:
            obs.append(cls(random.randint(16,224)))
            cls.ttgo=random.randint(cls.pmin,cls.pmax)
        else:
            cls.ttgo-=1
    isdeadly=True
    deadgooff=True
    plaser=True
    col=(200,200,0)
class EnemyShip(Obstacle):
    ttgo=0
    plaser=True
    col=(100,255,100)
    @classmethod
    def generate(cls,obs):
        if cls.ttgo==0:
            obs.append(cls(random.randint(16,224)))
            cls.ttgo=random.randint(100,200)
        else:
            cls.ttgo-=1
    def update(self,obs):
        self.x-=1
        if not random.randint(0,120):
            obs.append(ELaser(self.x,self.y+6))
class Ranged(Obstacle):
    plaser=True
    col=(200,255,200)
    @classmethod
    def generate(cls,obs):
        if cls.ttgo==0:
            obs.append(cls(random.randint(16,224)))
            cls.ttgo=random.randint(100,200)
        else:
            cls.ttgo-=1
    def update(self,obs):
        if self.x>300:
            self.x-=1
        elif not random.randint(0,60):
            obs.append(UELaser(self.x+6,self.y+6,random.randint(-30,30)))
class EnemyShip2(Obstacle2):
    pmin=120
    pmax=160
    plaser=True
    col=(0,200,0)
    def update(self,obs):
        self.x-=2
        self.t=(self.t+2)%360
        self.y=int(round(100*math.cos(math.radians(self.t))))+128
        if not random.randint(0,60):
            obs.append(ELaser(self.x,self.y+6))
class ELaser(Obstacle):
    col=(255,0,0)
    w=16
    h=4
    def update(self,obs):
        self.x-=4
    def __init__(self,x,y):
        self.x=x
        self.y=y
class UELaser(Obstacle):
    col=(255,0,0)
    w=4
    h=4
    def update(self,obs):
        self.tick+=4
        self.y=self.sy-int(round(self.tick*math.sin(self.angle)))
        self.x=self.sx-int(round(self.tick*math.cos(self.angle)))
    def __init__(self,x,y,angle):
        self.x=x
        self.y=y
        self.sx=x
        self.sy=y
        self.angle=math.radians(angle)
        self.tick=0
class BigAsteroid(Asteroid):
    w=64
    h=64
    pmin=70
    pmax=120
class SmallAsteroid(Asteroid):
    w=4
    h=4
class Hostage(Obstacle):
    hostage=True
    plaser=True
    col=(255,200,200)