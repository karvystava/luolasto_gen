import numpy as np
from random import randrange
from algorithms import triangulation, prim, a_star
from items import Room, Passage

class Map():
    def __init__(self, screen, screen_w, screen_h, buffer, room_number, colors):

        self.grid = np.full(784, 2, dtype=int).reshape(28, 28)
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.room_number = room_number
        self.colors = colors
        self.buffer = buffer #16

        self.nodes = []
        self.rooms = [] 
        self.mids = []
        self.passages = {}
        self.tree = {}
        self.hallways = {}
        self.grid_lines = []

        self.create_grid_lines()
        self.create_rooms()
        print(self.grid)
        self.create_passages(triangulation(self.mids, self.screen_h, self.screen_w), colors['tri'])
        self.create_mst(prim(self.passages['psg'], len(self.rooms)), colors['mst'])
        self.create_a_star(colors['hallways'])
        print()
        print(self.grid)


    def create_grid_lines(self):

        grid_x = 52
        grid_y = 52
        for _ in range(29):
            self.grid_lines.append(Passage((grid_x, 20), (grid_x, 980), '#FFFFFF', self.screen, 1))
            self.grid_lines.append(Passage((20, grid_y), (980, grid_y), '#FFFFFF', self.screen, 1))
            grid_x += 32
            grid_y += 32


    def create_rooms(self):

        rooms = []
        for _ in range(self.room_number):
            while True:

                again = False
                h = randrange(48,240,32)
                w = randrange(48,240,32)
                x = randrange(20+16, self.screen_w-20-w, 32)
                y = randrange(20+16, self.screen_h-20-h, 32)

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
            self.rooms.append(Room(room['x'], room['y'], room['w'], room['h'], self.screen, self.colors, self.buffer))
            self.mids.append((room["x"]+room["w"]/2, room["y"]+room["h"]/2))

            x = (room['x']-20)//32
            y = (room['y']-20)//32
            w = (room['w']-16)//32
            h = (room['h']-16)//32
            
            self.grid[y:y+h,x:x+w] = 9
            self.nodes.append({'pos': (x+w//2, y+h//2), 'g': 1000, 'h': 0.0, 'parent': None, 'cost':9})


    def create_passages(self, passages, color):

        self.passages['psg'] = []
        self.passages['edges'] = set()
        for edge in passages:
            self.passages['psg'].append(Passage(edge[0], edge[1], color, self.screen, 2))
            self.passages['edges'].add(edge)

    def create_mst(self, mst, color):

        self.tree['psg'] = []
        self.tree['edges'] = set()
        for edge in mst:
            self.tree['psg'].append(Passage(edge[0], edge[1], self.colors['mst'], self.screen, 2))
            self.tree['edges'].add(edge)

        extra = list(self.passages['edges'] - self.tree['edges'])
        for i in range(len(extra)//5):
            self.tree['psg'].append(Passage(extra[i][0], extra[i][1], color, self.screen, 2))

    def create_a_star(self, color):

        full_path = set()
        for _ in range(len(self.nodes)-1):
            full_path.update(a_star(self.nodes[0], self.nodes[1], self.grid))
            self.nodes.pop(0)

        self.hallways['psg'] = []
        self.hallways['edges'] = set()
        for edge in full_path:
            self.hallways['psg'].append(Passage(edge[0], edge[1], color, self.screen, 20))
            self.hallways['edges'].add(edge)

        return full_path
