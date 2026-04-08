from random import randint
import sys
import math
import pygame
from circumcenter import center

class DungeonGen():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dungeon Generator")

        self.screen_w = 1000
        self.screen_h = 1000
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.map_surface = pygame.Surface((980, 980))
        self.font = pygame.font.SysFont("Arial", 24)

        self.fps_clock = pygame.time.Clock()
        self.fps = 60

        self.state = 'startscreen'
        self.show_triangulation = True
        self.objects = {'buttons':[],'rooms':[], 'mids':[], 'passages':[]}

        self.create_button(300, 400, 400, 100, self.font, self.screen, 'startscreen', 'Generate a Dungeon', self.new_map)
        self.create_button(30, 60, 100, 30, self.font, self.screen, 'dungeon', 'New', self.new_map)

        self.loop()


    def make_rooms(self, number_of_rooms, buffer, color):
        rooms = []
        for _ in range(number_of_rooms-1):
            while True:
                again = False
                h = randint(70,220)
                w = randint(70,220)
                x = randint(20, self.screen_w-20-w)
                y = randint(20, self.screen_h-20-h)

                for room in rooms:
                    x_mez = sorted([(x, w), (room["x"], room["w"])], key=lambda x:x[0], reverse=True)
                    y_mez = sorted([(y, h), (room["y"], room["h"])], key=lambda x:x[0], reverse=True)
                    if x_mez[0][0] - x_mez[1][0] - x_mez[1][1] < 0 and y_mez[0][0] - y_mez[1][0] - y_mez[1][1] < 0:
                        again = True
                        break

                if again:
                    continue
                room_dict = {"h":h, "w":w, "x":x, "y":y}
                rooms.append(room_dict)
                break

        for room in rooms:
            self.create_room(room["x"], room["y"], room["w"], room["h"], self.screen, color, buffer)
            self.objects['mids'].append((room["x"]+room["w"]/2, room["y"]+room["h"]/2))


    def triangulation(self, room_points):
        supertri_points = ((0,0), (0, self.screen_h*2), (self.screen_w*2,0))
        supertri_edges = (((0,0), (0,self.screen_h*2)), ((0,0), (self.screen_w*2,0)), ((self.screen_w*2,0), (0,self.screen_h*2)))
        supertri_circumcenter = center((0,0), (0, self.screen_h*2), (self.screen_w*2,0))

        supertri = {'circum':(supertri_circumcenter, math.dist((0,0), supertri_circumcenter)), 'points':set(supertri_points)}
        triangulation = {}
        edges = set()
        triangulation[supertri_edges] = supertri

        for point in room_points:

            bad_triangles = set()
            bad_edges = {}
            for triangle in triangulation:
                if math.dist(point, triangulation[triangle]['circum'][0]) <= triangulation[triangle]['circum'][1]:
                    bad_triangles.add(triangle)
                    for edge in triangle:
                        if edge not in bad_edges:
                            bad_edges[edge] = 0
                        bad_edges[edge] += 1

            polygon = set()
            for triangle in bad_triangles:
                for edge in triangle:
                    if bad_edges[edge] == 1:
                        polygon.add(edge)
                triangulation.pop(triangle)

            for edge in polygon:
                new_edges = tuple(sorted((tuple(sorted(edge)), tuple(sorted((edge[0], point))), tuple(sorted((edge[1], point))))))
                new_circ = center(edge[0], edge[1], point)
                triangulation[new_edges] = {'circum':(new_circ, math.dist(new_circ, point)), 'points':set((edge[0], edge[1], point))}

        for triangle in triangulation:
            if len(triangulation[triangle]['points'] - set(supertri_points)) == 3:
                edges.update(triangle)

        return edges


    def create_button(self, x, y, width, height, font, screen, state, button_text='Button', click_function=None, one_press=False):
        self.objects['buttons'].append(Button(x, y, width, height, font, screen, state, button_text, click_function, one_press))

    def create_room(self, x, y, width, height, screen, color, buffer):
        self.objects['rooms'].append(Room(x, y, width, height, screen, color, buffer))

    def create_passages(self, passages):
        for edge in passages:
            self.objects['passages'].append(Passage(edge[0], edge[1], '#80FF00', self.screen, 2))


    def new_map(self):
        self.state = 'dungeon'

        for key in self.objects:
            if key != 'button':
                self.objects[key].clear()


        self.make_rooms(15, 20, '#CCE5FF')
        self.create_passages(self.triangulation(self.objects['mids']))


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
                if self.show_triangulation:
                    room.render_mid()

            for passage in self.objects['passages']:
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
