#Snake Abgabge OOS WS 21/22
#Author Hendrik Müller
#Music: https://www.chosic.com/free-music/all/  John_Bartmann_-_11_-_Iyanetha

#from _typeshed import Self
#import math
import random
import pygame
from pygame import mixer
import tkinter as tk
from tkinter import *
from tkinter import messagebox

#initialisierung für PyGame
pygame.init()

#Abspielen der Hintergrund musik. Play(-1) steht dabei dafür, das die musik durchgehen im hintergund wiederholt wird
mixer.music.load('Data/Sound/background.mp3')
mixer.music.play(-1)

#die Klasse Cube stellt das "Spielfeld" dar. 
class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(50,205,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
        
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))

        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))

        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))

        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))


        self.body[-1].dirny = dy
        self.body[-1].dirnx = dx
        
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

#das zeichnen der Linien auf dem "Spielfeld"
def drawGrid(w, rows, surface):
    roomBetween = w // rows

    y = 0
    x = 0
    for l in range(rows):
        y = y + roomBetween
        x = x + roomBetween
        
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((128,128,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()


def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)
    
#die Logik der Message Box welche am ende des Spiel angezeigt wird
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    response = messagebox.askretrycancel(subject, content)
    Label(root,).pack()
    if response == 1:
        Label(root, text= "Okay!").pack()
    else:
        raise SystemExit
    try:
        root.destroy()
    except:
        pass

#die main methode
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((50,205,50), (10,10))
    snack = cube(randomSnack(rows, s), color=(250,128,114))
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(100)
        clock.tick(10)
        s.move()
        #Logik des fressens + Sound
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(250,128,114))
            chomp_sound = mixer.Sound('Data/Sound/impactcrunch01.mp3.flac')
            chomp_sound.play()
        # Definition des Game Over
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Punktzahl: ', len(s.body))
                message_box('Verloren', 'Versuch`s noch einmal!')
                s.reset((10,10))
                break
            
        redrawWindow(win)

    pass



main()