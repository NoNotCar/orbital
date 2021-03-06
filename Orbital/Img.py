'''
Created on 7 Sep 2014
Once Seen, Cannot Be Unseen
@author: NoNotCar
'''
import pygame
import os
pygame.init()
pygame.mixer.init()
loc = os.path.dirname(os.getcwd())+"/Assets/"
def imgret2(fil):
    return pygame.transform.scale2x(pygame.image.load(os.path.normpath(loc + fil)).convert_alpha())
def imgret32(fil):
    return pygame.transform.scale(pygame.image.load(loc + fil).convert_alpha(),(32,32))
def imgret32x16(fil):
    return pygame.transform.scale(pygame.image.load(loc + fil).convert_alpha(),(32,16))
def imgretrect(fil,x,y):
    return pygame.transform.scale(pygame.image.load(loc + fil), (x, y))
def imgretsrect(fil,x,y):
    return pygame.transform.smoothscale(pygame.image.load(loc + fil), (x, y))
def imgtransrect(fil,x,y):
    return pygame.transform.scale(fil, (x, y))
def sndget(fil):
    return pygame.mixer.Sound(loc+"Sounds/" + fil)
def imgret(img):
    return pygame.image.load(loc+img).convert_alpha()
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
def musply(mus,loops=-1):
    pygame.mixer.music.load(os.path.normpath(loc+mus))
    pygame.mixer.music.play(loops)
def Fsize(size):
    return pygame.font.Font(pygame.font.get_default_font(), size)
def blitrect(screen,col, x, y, w, h):
    pygame.draw.rect(screen, col, pygame.Rect(x,y,w,h))
def inversecol(col):
    return (0,0,0) if sum(col)>475 else (255, 255, 255)
def bcentre(font,text,surface,offset=0,col=(0,0,0)):
    render=font.render(str(text),True,col)
    textrect=render.get_rect()
    textrect.centerx = surface.get_rect().centerx
    textrect.centery = surface.get_rect().centery+offset
    surface.blit(render,textrect)
pfont = pygame.font.Font(pygame.font.get_default_font(), 30)
pfont2 = pygame.font.Font(pygame.font.get_default_font(), 14)
bfont = pygame.font.Font(pygame.font.get_default_font(), 90)
bufont = pygame.font.Font(pygame.font.get_default_font(), 70)
dfont = pygame.font.Font(pygame.font.get_default_font(), 28)
sfont = pygame.font.Font(pygame.font.get_default_font(), 10)