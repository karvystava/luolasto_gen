import pygame
import sys
from random import randint

class DungeonGen():
    def __init__(self):
        pygame.init()
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.screen_width = 1700
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
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
        self.gen_rooms(20, 20, '#ffffff')

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


    def gen_rooms(self, number_of_rooms, buffer, color):
        print("start of generating")
        rooms = []
        for _ in range(number_of_rooms-1):
            print("start of iteration")
            while True:
                print(rooms)
                print("start of loop")
                again = False
                room_height = randint(20,200)
                room_width = randint(20,200)
                x = randint(20, self.screen_width-buffer-room_width)
                y = randint(20, self.screen_height-buffer-room_height)

                print(room_height, room_width, x, y)
                for room in rooms:
                    x_mez = sorted((x, room["x"]), reverse=True)
                    y_mez = sorted((y, room["y"]), reverse=True)
                    print(x_mez)
                    print(y_mez)
                    print(x_mez[0] - x_mez[1] - room_width)
                    print(y_mez[0] - y_mez[1] - room_height)
                    if x_mez[0] - x_mez[1] - room_width < 0 and y_mez[0] - y_mez[1] - room_height < 0:
                        again = True
                        print("overlap found")
                        break

                if again == True:
                    print("needed new room")
                    continue
                room_dict = {"h":room_height, "w":room_width, "x":x, "y":y}
                rooms.append(room_dict)
                print("room should be good to go")
                break
        
        print("starting to add rooms")
        for room in rooms:
            self.create_room(room["x"], room["y"], room["w"], room["h"], self.screen, color, 'dungeon')
        print("rooms added")


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