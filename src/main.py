import pygame
import sys
from random import randint
import math
from circumcenter import center

class DungeonGen():
    def __init__(self):
        pygame.init()
        self.show_triangulation = True
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.screen_width = 1000
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont("Arial", 24)
        self.state = 'startscreen'
        self.mapSurface = pygame.Surface((980, 980))
        pygame.display.set_caption("Dungeon Generator")
        self.objects = []
        self.rooms = []
        self.mids = []
        self.passages = []
        self.create_button(300, 400, 400, 100, self.font, self.screen, 'startscreen', 'Generate a Dungeon', self.switchtomap)
        self.create_button(30, 60, 100, 30, self.font, self.screen, 'dungeon', 'New', self.switchtomap)

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

    def switchtomap(self):
        self.rooms.clear()
        self.mids.clear()
        self.passages.clear()
        self.state = 'dungeon'
        self.make_rooms(15, 20, '#CCE5FF')
        self.create_passages(self.triangulation(self.mids),)


    def create_button(self, x, y, width, height, font, screen, state, buttonText='Button', onclickFunction=None, onePress=False):
        self.objects.append(Button(x, y, width, height, font, screen, state, buttonText, onclickFunction, onePress))

    def create_room(self, x, y, width, height, screen, color, buffer):
        self.rooms.append(Room(x, y, width, height, screen, color, buffer))

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
            for room in self.rooms:
                room.render()
                if self.show_triangulation:
                    room.render_mid()
            for passage in self.passages:
                passage.render()

        for object in self.objects:
            if object.state == self.state:
                object.render()

        pygame.display.flip()


    def make_rooms(self, number_of_rooms, buffer, color):
        rooms = []
        for _ in range(number_of_rooms-1):
            while True:
                again = False
                h = randint(70,220)
                w = randint(70,220)
                x = randint(20, self.screen_width-20-w)
                y = randint(20, self.screen_height-20-h)

                for room in rooms:
                    x_mez = sorted([(x, w), (room["x"], room["w"])], key=lambda x:x[0], reverse=True)
                    y_mez = sorted([(y, h), (room["y"], room["h"])], key=lambda x:x[0], reverse=True)
                    if x_mez[0][0] - x_mez[1][0] - x_mez[1][1] < 0 and y_mez[0][0] - y_mez[1][0] - y_mez[1][1] < 0:
                        again = True
                        break

                if again == True:
                    continue
                room_dict = {"h":h, "w":w, "x":x, "y":y}
                rooms.append(room_dict)
                break
        
        for room in rooms:
            self.create_room(room["x"], room["y"], room["w"], room["h"], self.screen, color, buffer)
            self.mids.append((room["x"]+room["w"]/2, room["y"]+room["h"]/2))
    

    def triangulation(self, room_points): 
        supertri_points = ((0,0), (0, self.screen_height*2), (self.screen_width*2,0))
        supertri_edges = (((0,0), (0,self.screen_height*2)), ((0,0), (self.screen_width*2,0)), ((self.screen_width*2,0), (0,self.screen_height*2)))
        supertri_circumcenter = center((0,0), (0, self.screen_height*2), (self.screen_width*2,0))

        supertri = {'circum':(supertri_circumcenter, math.dist((0,0), supertri_circumcenter)), 'points':set(supertri_points)}
        triangulation = {}
        edges = set()
        triangulation[supertri_edges] = supertri

        for point in room_points:

            badTriangles = set()
            badEdges = {}
            for triangle in triangulation:
                if math.dist(point, triangulation[triangle]['circum'][0]) <= triangulation[triangle]['circum'][1]:
                    badTriangles.add(triangle)
                    for edge in triangle:
                        if edge not in badEdges:
                            badEdges[edge] = 0
                        badEdges[edge] += 1

            polygon = set()
            for triangle in badTriangles:
                for edge in triangle:
                    if badEdges[edge] == 1:
                        polygon.add(edge)
                triangulation.pop(triangle)

            for edge in polygon:
                new_edges = tuple(sorted((tuple(sorted(edge)), tuple(sorted((edge[0], point))), tuple(sorted((edge[1], point))))))
                new_circ = center(edge[0], edge[1], point)
                triangulation[new_edges] = {'circum':(new_circ, math.dist(new_circ, point)), 'points':set((edge[0], edge[1], point))}
        
        for triangle in triangulation:
            if len(triangulation[triangle]['points'] - set(supertri_points)) == 3:
                edges.update(triangle)
                print("all edges:", edges)

        print("triangulation done")
        return edges

    def create_passages(self, passages):
        for edge in passages:
            print("edge in question:", edge)
            print("edge[0]:", edge[0])
            print("edge[1]:", edge[1])
            self.passages.append(Passage(edge[0], edge[1], '#80FF00', self.screen, 2))

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
        self.mid = (x+width/2, y+height/2)

    def render(self):
        pygame.draw.rect(self.screen, (0,0,70), self.buffer)
        pygame.draw.rect(self.screen, self.color, self.room)
    
    def render_mid(self):
        pygame.draw.circle(self.screen, '#FF66B2', self.mid, 3)


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