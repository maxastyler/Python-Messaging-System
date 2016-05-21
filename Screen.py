import pygame
import random
from Messenger import *

def coord_transform(SCREEN_SIZE, x, y):
    return x, SCREEN_SIZE[1]-y


class Screen:
    def __init__(self, x, y, size):
        self.x=x
        self.y=y
        self.size=size
        self.surf=pygame.Surface(size)

    def render(self, screen):
        screen.blit(self.surf, (self.x, -self.y))

    def shake(self, messenger, length, max_size):
        for i in range(30, length, 30):
            messenger.schedule(Event("shake", args={"size": (max_size)*(1.-float(i)/float(length))}), i)
        messenger.schedule(Event("shake", args={"size": 0}), length)

    def set_random(self, event):
        self.x=(random.random()-0.5)*event.args["size"]
        self.y=(random.random()-0.5)*event.args["size"]

    def set_zero(self):
        self.x=0
        self.y=0
