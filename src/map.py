import numpy as np
from random import randrange
from algorithms import triangulation, prim, a_star
from items import Room, Passage

class Map():
    def __init__(self, screen, screen_w, screen_h, buffer, room_number, colors):

        # grid + inherited dimensions etc
        self.grid = np.zeros((28, 28), dtype=int)
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.room_number = room_number
        self.colors = colors
        self.buffer = buffer #16

        # map objects the algorithms need
        self.nodes = []
        self.rooms = [] 
        self.mids = []
        self.passages = {}
        self.tree = {}
        self.hallways = {}
        self.grid_lines = []

        # create map objects with algorithms
        self.create_grid_lines()
        self.create_rooms()
        self.create_passages(triangulation(self.mids, self.screen_h, self.screen_w), colors['tri']) # make passages with triangulation
        self.create_mst(prim(self.passages['psg'], len(self.rooms))) # make minimum spanning tree in triangulation with Prim
        self.create_a_star(colors['hallways']) # make hallways between mst edges with A* in regards to grid


    # divide map surface into grid lines to help visualize
    def create_grid_lines(self):

        grid_x = 52
        grid_y = 52
        for _ in range(29):
            self.grid_lines.append(Passage((grid_x, 20), (grid_x, 980), '#FFFFFF', self.screen, 1))
            self.grid_lines.append(Passage((20, grid_y), (980, grid_y), '#FFFFFF', self.screen, 1))
            grid_x += 32
            grid_y += 32


    # generate random room dimensions with regards to margin (20), buffer (16), 28x28 grid (divisible by 32)
    def create_rooms(self):

        rooms = []
        for _ in range(self.room_number):
            while True:

                again = False

                h = randrange(48,240,32)
                w = randrange(48,240,32)
                x = randrange(20+16, self.screen_w-20-w, 32)
                y = randrange(20+16, self.screen_h-20-h, 32)

                for room in rooms: # make sure rooms don't overlap

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

            # create class Room objects and store middle points for visualization
            self.rooms.append(Room(room['x'], room['y'], room['w'], room['h'], self.screen, self.colors, self.buffer))
            self.mids.append((room["x"]+room["w"]/2, room["y"]+room["h"]/2))

            # translate room dimensions and position from pixels to grid
            x = (room['x']-20)//32
            y = (room['y']-20)//32
            w = (room['w']-16)//32
            h = (room['h']-16)//32
            
            cost = 4
            self.grid[y:y+h,x:x+w] = cost # add rooms to grid
            #self.nodes.append({'pos': (x+w//2, y+h//2), 'g': 1000, 'h': 0.0, 'parent': None, 'cost':cost}) # store middle points as nodes for algorithms
 

    def create_room_node(self, point):
        x = int((point[0]-20)//32-1)
        y = int((point[1]-20)//32-1)
        node = {'pos': (x, y), 'g': 1000, 'h': 0.0, 'parent': None, 'cost':4}
        return node

    # store passages as both Passage class objects and just edges for Prim  
    def create_passages(self, passages, color):
 
        self.passages['psg'] = []
        self.passages['edges'] = set()
        for edge in passages:
            self.passages['psg'].append(Passage(edge[0], edge[1], color, self.screen, 2))
            self.passages['edges'].add(edge)


    # store tree as both Passage class objects and just edges for A*
    def create_mst(self, mst):

        self.tree['psg'] = []
        self.tree['edges'] = []
        edge_list = []
        for edge in mst:
            edge_list.append(edge)
            self.tree['psg'].append(Passage(edge[0], edge[1], self.colors['mst'], self.screen, 2))
            start_node = self.create_room_node(edge[0])
            end_node = self.create_room_node(edge[1])
            grid_edge = (start_node, end_node)
            self.tree['edges'].append(grid_edge)

        # add few extra passages from triangulation to make loops
        extra = []
        j = 0
        k = 0
        extra_num = randrange(0, (len(self.passages['edges']) - (len(edge_list)))//7+2) if len(edge_list) > 5 else 0
        passage_list = list(self.passages['edges'])
        while k < extra_num and extra_num != 0:
            edge1 = (passage_list[j][0], passage_list[j][1])
            edge2 = (passage_list[j][1], passage_list[j][0])
            if edge1 not in edge_list and edge2 not in edge_list:
                extra.append(passage_list[j])
                k += 1
            j += 1

        i = 0
        for i in range(extra_num):
            self.tree['psg'].append(Passage(extra[i][0], extra[i][1], '#FAD9D9', self.screen, 2))
            start_node = self.create_room_node(extra[i][0])
            end_node = self.create_room_node(extra[i][1])
            self.tree['edges'].append((start_node, end_node))

    # store hallways as both Passage class objects and just edges
    def create_a_star(self, color):

        full_grid_path = set()
        full_path = set()

        for edge in self.tree['edges']: # make A* path between all nodes
            path = a_star(edge[0], edge[1], self.grid)
            full_path.update(path[0])
            full_grid_path.update(path[1])

        self.hallways['psg'] = []
        self.hallways['edges'] = set()
        for edge in full_path:
            self.hallways['psg'].append(Passage(edge[0], edge[1], color, self.screen, 20))
            self.hallways['edges'].add(edge)

        return full_path
