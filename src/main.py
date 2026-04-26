import sys
import pygame
import math
import numpy as np
from gens import gen_rooms, triangulation, prim

class DungeonGen():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dungeon Generator")

        self.screen_w = 1000
        self.screen_h = 1000
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.map_surface = pygame.Surface((980, 980))
        self.font = pygame.font.SysFont("Arial", 24)
        self.grid = np.zeros((30, 30), dtype=int)

        self.fps_clock = pygame.time.Clock()
        self.fps = 60

        self.state = 'startscreen'
        self.show_mid = False
        self.show_triangulation = False
        self.show_prim = True
        self.number_of_rooms = 20
        self.objects = {'buttons':[],'rooms':[], 'mids':[], 'passages':{}, 'tree':{}}

        self.create_button(300, 400, 400, 100, self.font, self.screen, 'startscreen', 'Generate a Dungeon', self.new_map)
        self.create_button(30, 60, 100, 30, self.font, self.screen, 'dungeon', 'New', self.new_map)

        self.loop()


    def make_rooms(self, rooms, buffer, color):
        for room in rooms:
            self.create_room(room["x"], room["y"], room["w"], room["h"], self.screen, color, buffer)
            self.objects['mids'].append((room["x"]+room["w"]/2, room["y"]+room["h"]/2))
            print(room['x'])
            print(room['x']+buffer)
            print((room['x']+40)/32)

    def create_button(self, x, y, width, height, font, screen, state, button_text='Button', click_function=None, one_press=False):
        self.objects['buttons'].append(Button(x, y, width, height, font, screen, state, button_text, click_function, one_press))

    def create_room(self, x, y, width, height, screen, color, buffer):
        self.objects['rooms'].append(Room(x, y, width, height, screen, color, buffer))

    def create_passages(self, passages):
        self.objects['passages']['psg'] = []
        self.objects['passages']['edges'] = set()
        for edge in passages:
            self.objects['passages']['psg'].append(Passage(edge[0], edge[1], '#80FF00', self.screen, 2))
            self.objects['passages']['edges'].add(edge)

    def create_mst(self, mst):
        self.objects['tree']['psg'] = []
        self.objects['tree']['edges'] = set()
        for edge in mst:
            self.objects['tree']['psg'].append(Passage(edge[0], edge[1], '#FF007F', self.screen, 2))
            self.objects['tree']['edges'].add(edge)

        extra = list(self.objects['passages']['edges'] - self.objects['tree']['edges'])
        for i in range(len(extra)//5):
            self.objects['tree']['psg'].append(Passage(extra[i][0], extra[i][1], '#FF007F', self.screen, 2))



    def new_map(self):
        self.state = 'dungeon'

        for key, obs in self.objects.items():
            if key != 'buttons':
                obs.clear()


        self.make_rooms(gen_rooms(self.number_of_rooms, self.screen_h, self.screen_w), 16, '#CCE5FF')
        print(self.grid)
        self.create_passages(triangulation(self.objects['mids'], self.screen_h, self.screen_w))
        self.create_mst(prim(self.objects['passages']['psg'], len(self.objects['rooms'])))


    def loop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            for button in self.objects['buttons']:
                if button.state == self.state:
                    button.process()

            self.display_screen()
            self.fps_clock.tick(self.fps)


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

            for room in self.objects['rooms']:
                room.render()
                if self.show_mid:
                    room.render_mid()

            if self.show_triangulation:
                for passage in self.objects['passages']['psg']:
                    passage.render()

            if self.show_prim:
                for passage in self.objects['tree']['psg']:
                    passage.render()

            

        for button in self.objects['buttons']:
            if button.state == self.state:
                button.render()

        pygame.display.flip()


class Passage():
    def __init__(self, a, b, color, screen, width):
        self.a = a
        self.b = b
        self.color = color
        self.screen = screen
        self.w = width
        self.color = color
        self.d = math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    def render(self):
        pygame.draw.line(self.screen, self.color, self.a, self.b, self.w)


class Room():
    def __init__(self, x, y, width, height, screen, color, buffer):
        self.screen = screen
        self.room = pygame.Rect((x+buffer, y+buffer, width-buffer, height-buffer))
        self.buffer = pygame.Rect((x, y, width+buffer, height+buffer))
        self.color = color
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.mid = (x+width/2, y+height/2)

    def render(self):
        pygame.draw.rect(self.screen, (0,0,70), self.buffer)
        pygame.draw.rect(self.screen, self.color, self.room)

    def render_mid(self):
        pygame.draw.circle(self.screen, '#FF66B2', self.mid, 3)


class Button():
    def __init__(self, x, y, width, height, font, screen, state, button_text, click_function, one_press):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.click_function = click_function
        self.one_press = one_press
        self.already_pressed = False
        self.screen = screen
        self.state = state

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333'
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.button_surf = font.render(button_text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])
                if self.one_press:
                    self.click_function()
                elif not self.already_pressed:
                    self.click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

    def render(self):
        self.button_surface.blit(self.button_surf, [
        self.button_rect.width/2 - self.button_surf.get_rect().width/2,
        self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])
        self.screen.blit(self.button_surface, self.button_rect)


if __name__ == "__main__":
    DungeonGen()
