import pytest
import math
from random import randint
from map import Map
from algorithms import prim, triangulation
from items import Passage

def test_prim_with_no_rooms():
    passages = []
    number = 0
    mst = set()

    assert mst == prim(passages, number)


def test_prim_with_one_room():
    passages = []
    number = 1
    mst = set()

    assert mst == prim(passages, number)


def test_edge_number():
    colors = {
        'bg': '#000000',
        'rooms': '#FFFFFF', 
        'hallways': "#FFFFFF", #FAD9D9 
        'mst': '#FF007F', 
        'tri':'#80FF00'
        }
    
    room_amount = randint(1,50)
    test_map = Map(None, 1000, 1000, 16, room_amount, colors)
    test_prim = prim(test_map.passages['psg'], room_amount)

    assert room_amount-1 == len(test_prim)


def test_prim_with_ten_rooms():
    passages = []
    number = 10
    edges = {
        ((1, 1), (1, 2)), ((1, 1), (2, 3)), ((1, 1), (4, 3)), 
        ((1, 2), (2, 3)), ((2, 3), (4, 3)), ((2, 3), (6, 5)), 
        ((4, 3), (6, 5)), ((4, 3), (9, 5)), ((6, 5), (9, 5)), 
        ((6, 5), (12, 8)), ((9, 5), (12, 8)), ((9, 5), (16, 8)), 
        ((12, 8), (16, 8)), ((12, 8), (20, 12)), ((16, 8), (20, 12)),
        ((16, 8), (25,12)), ((20,12),(25,12)) 
             }

    for edge in edges:
        passages.append(Passage(edge[0], edge[1], None, None, 2))

    mst = {
        ((4, 3), (2, 3)), ((2, 3), (1, 2)), ((20, 12), (25, 12)), 
        ((4, 3), (6, 5)), ((12, 8), (16, 8)), ((16, 8), (20, 12)), 
        ((1, 2), (1, 1)), ((9, 5), (12, 8)), ((6, 5), (9, 5))
        }
    test_prim = prim(passages, number)

    assert test_prim == mst


def test_through_all_rooms():

    node_set = set()
    while True:
        if len(node_set) == 200:
            break
        node_set.add((randint(1,1000), randint(1,1000)))

    nodes = list(node_set)
    all_edges_tri = triangulation(nodes, 1000, 1000)

    all_edges = []
    for edge in all_edges_tri:
        all_edges.append(Passage(edge[0], edge[1], None, None, 2))

    edges = prim(all_edges, 200)

    d = DFS(nodes)

    for edge in edges:
        d.add_edge(edge[0], edge[1])

    assert d.search(nodes[0]) == set(nodes)
    

class DFS():
    def __init__(self, nodes):
        self.nodes = nodes
        self.graph = {node: [] for node in nodes}

    def add_edge(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)

    def visit(self, node):
        if node in self.visited:
            return
        self.visited.add(node)

        for next_node in self.graph[node]:
            self.visit(next_node)

    def search(self, start_node):
        self.visited = set()
        self.visit(start_node)
        return self.visited