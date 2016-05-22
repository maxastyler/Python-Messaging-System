import pygame
from pygame.color import THECOLORS
import sys
from Messenger import *
from Screen import *
import numpy as np
import random

SCREEN_SIZE=(500, 500)
circ_max=np.sqrt(SCREEN_SIZE[0]**2+SCREEN_SIZE[1]**2)*2.
FPS=60.
circs=[]

class Circle:
    def __init__(self, x, y, radius, colour):
        self.x=x
        self.y=y
        self.radius=radius
        self.colour=colour

    def render(self, screen):
        pygame.draw.circle(screen, self.colour, (int(np.round(self.x)), int(np.round(SCREEN_SIZE[1]-self.y))), int(np.round(self.radius)))

def pygame_coords(x, y):
    return x, SCREEN_SIZE[1]-y

cursor=[SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2]


def add_circ(event):
    circs.append(Circle(cursor[0], cursor[1], 0, (random.random()*255, random.random()*255, random.random()*255)))
    messenger.schedule(Event("circ"), 50.)

def main():
    window = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Messaging System Test")

    global messenger
    messenger=Messenger()

    screen=Screen( 0, 0, SCREEN_SIZE)

    clock=pygame.time.Clock()

    circs.append(Circle(SCREEN_SIZE[0]/2., SCREEN_SIZE[1]/2., 0, (random.random()*255, random.random()*255, random.random()*255)))

    running=True
    messenger.add_listener(Listener("circ",add_circ))
    messenger.add_listener(Listener("shake", screen.set_random))
    add_circ(1)
    while running:

        dt=clock.tick(FPS)
        messenger.update(dt)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False
                break

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            vel=0.3
        elif keys[pygame.K_LCTRL]:
            vel=0.05
        else:
            vel=0.1
        if keys[pygame.K_ESCAPE]:
            running=False
            break
        if keys[pygame.K_SPACE]:
            messenger.clear_events("shake")
            screen.shake(messenger, 1000, 70)
        if keys[pygame.K_a]:
            if cursor[0]>=0:
                cursor[0]-=vel*dt
        if keys[pygame.K_d]:
            if cursor[0]<=SCREEN_SIZE[0]:
                cursor[0]+=vel*dt
        if keys[pygame.K_w]:
            if cursor[1]<=SCREEN_SIZE[1]:
                cursor[1]+=vel*dt
        if keys[pygame.K_s]:
            if cursor[1]>=0:
                cursor[1]-=vel*dt

        window.fill(THECOLORS['black'])
        screen.surf.fill(THECOLORS['white'])
        for circ in circs:
            circ.render(screen.surf)
            circ.radius+=0.1*dt
        if len(circs)>130:
            circs.pop(0)
        screen.render(window)
        pygame.display.update()

    pygame.quit()

if __name__=='__main__':
    sys.exit(main())
