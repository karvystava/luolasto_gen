import pygame
import sys
from random import randint

class DungeonGen():
    def __init__(self):
        pygame.init()
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1600,1000))
        self.font = pygame.font.SysFont("Arial", 24)
        self.state = 'startscreen'

        pygame.display.set_caption("Dungeon Generator")
        self.objects = []
        self.create_button(600, 450, 400, 100, self.font, self.screen, 'startscreen', 'Generate a Dungeon', self.switchtomap)

        self.loop()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            for object in self.objects:
                if object.state == self.state:
                    object.process()
            self.display_screen()
            self.fpsClock.tick(self.fps)

    def create_button(self, x, y, width, height, font, screen, state, buttonText='Button', onclickFunction=None, onePress=False):
        self.objects.append(Button(x, y, width, height, font, screen, state, buttonText, onclickFunction, onePress))

    def create_room(self, x, y, width, height, screen, color, state):
        self.objects.append(Room(x, y, width, height, screen, color, state))

    def switchtomap(self):
        self.state = 'dungeon'
        for _ in range(10):
            self.create_room(randint(5, 1000), randint(5, 1000), randint(5, 100), randint(5, 100), self.screen, (0,0,30), 'dungeon')


    def display_screen(self):
        if self.state == 'startscreen':
            self.screen.fill((0,0,70))
            title_txt = "Dungeon Generator (startscreen)"
            title = self.font.render(title_txt, True, (255,0,0))
            self.screen.blit(title, (30,10))
        else:
            self.screen.fill((0,0,70))
            title_txt = "Dungeon Generator (map)"
            title = self.font.render(title_txt, True, (255,0,0))
            self.screen.blit(title, (30,10))

        for object in self.objects:
            if object.state == self.state:
                object.render()

        pygame.display.flip()


class Room():
    def __init__(self, x, y, width, height, screen, color, state):
        self.screen = screen
        self.state = state
        self.room = pygame.Rect((x, y, width, height))
        self.buffer = pygame.Rect((x+5, y+5, width+5, height+5))
        self.color = color

    def process(self):
        pass

    def render(self):
        pygame.draw.rect(self.screen, (0,0,70), self.buffer)
        pygame.draw.rect(self.screen, self.color, self.room)


class Button():
    def __init__(self, x, y, width, height, font, screen, state, buttonText, onclickFunction, onePress):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.screen = screen
        self.state = state

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333'
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

    def render(self):
        self.buttonSurface.blit(self.buttonSurf, [
        self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
        self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)

if __name__ == "__main__":
    DungeonGen()