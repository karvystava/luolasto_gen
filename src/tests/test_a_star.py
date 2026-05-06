import pygame
import numpy as np
from algorithms import a_star, neighbors, reconstruct_path

# neighbors function grid position tests

def test_neighbours_all():
    pos = (4,5)
    neighbors_should_be = [(5,5), (3,5), (4,6), (4,4)]

    assert neighbors(pos) == neighbors_should_be

def test_neighbor_upleft_corner():
    pos = (0,0)
    neighbors_should_be = [(1,0), (0,1)]

    assert neighbors(pos) == neighbors_should_be

def test_neighbor_upright_corner():
    pos = (27,0)
    neighbors_should_be = [(26,0), (27,1)]

    assert neighbors(pos) == neighbors_should_be

def test_neighbor_lowleft_corner():
    pos = (0,27)
    neighbors_should_be = [(1,27), (0,26)]

    assert neighbors(pos) == neighbors_should_be
    
def test_neighbor_lowright_corner():
    pos = (27,27)
    neighbors_should_be = [(26,27), (27,26)]

    assert neighbors(pos) == neighbors_should_be


# More neighbors function tests (up, down, left, right)

def test_no_neighbor_up():
    pos = (10,0)
    neighbors_should_be = [(11,0), (9,0), (10,1)]

    assert neighbors(pos) == neighbors_should_be

def test_no_neighbor_down():
    pos = (10,27)
    neighbors_should_be = [(11,27), (9,27), (10,26)]

    assert neighbors(pos) == neighbors_should_be

def test_no_neighbor_right():
    pos = (27,10)
    neighbors_should_be = [(26,10), (27,11), (27,9)]

    assert neighbors(pos) == neighbors_should_be

def test_no_neighbor_left():
    pos = (0,10)
    neighbors_should_be = [(1,10), (0,11), (0,9)]

    assert neighbors(pos) == neighbors_should_be

# A* tests

def test_a_star_two_rooms_grid():

    grid = np.full(784, 2, dtype=int).reshape(28, 28)
    start = {'pos':(5,3), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    goal = {'pos':(10,6), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    grid[2:5,4:6] = 9
    grid[5:7,9:11] = 9

    path = [
        (9,3),(10,4),(11,6),(7,3),
        (8,3), (10,6), (11,5),
        (10,3),(5,3),(6,3),(11,4)
        ]
    star_path = a_star(start, goal, grid)[1]

    assert tuple(path) == star_path

def test_a_star_two_rooms_screen():

    grid = np.full(784, 2, dtype=int).reshape(28, 28)
    start = {'pos':(5,3), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    goal = {'pos':(10,6), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    grid[2:5,4:6] = 9
    grid[5:7,9:11] = 9

    grid_path = [
        (9,3),(10,4),(11,6),(7,3),
        (8,3), (10,6), (11,5),
        (10,3),(5,3),(6,3),(11,4)
        ]

    path = set()
    for node in grid_path:
        path.add((node[0]*32+67.75, node[1]*32+67.75))

    star_path = set()
    star_path_edges = a_star(start, goal, grid)[0]
    for edge in star_path_edges:
        for node in edge:
            star_path.add(node)
    
    assert path == star_path

def test_a_start_two_rooms_edges():

    grid = np.full(784, 2, dtype=int).reshape(28, 28)
    start = {'pos':(5,3), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    goal = {'pos':(10,6), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    grid[2:5,4:6] = 9
    grid[5:7,9:11] = 9

    path = [
        ((291.75, 163.75), (259.75, 163.75)),
        ((259.75, 163.75), (227.75, 163.75)),
        ((387.75, 163.75), (355.75, 163.75)),
        ((323.75, 163.75), (291.75, 163.75)),
        ((419.75, 195.75), (387.75, 195.75)),
        ((387.75, 259.75), (419.75, 259.75)),
        ((355.75, 163.75), (323.75, 163.75)),
        ((387.75, 195.75), (387.75, 163.75)),
        ((419.75, 227.75), (419.75, 195.75)),
        ((419.75, 259.75), (419.75, 227.75))
    ]

    star_path = a_star(start, goal, grid)[0]

    assert tuple(path) == star_path

def test_a_start_three_rooms_edges():

    grid = np.full(784, 2, dtype=int).reshape(28, 28)
    start = {'pos':(5,3), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    goal = {'pos':(10,6), 'g':1000, 'h':0.0, 'parent':None, 'cost' : 9}
    grid[2:5,4:6] = 9
    grid[5:7,9:11] = 9
    grid[7:8,9:10] = 9

    path = [
        ((291.75, 163.75), (259.75, 163.75)),
        ((259.75, 163.75), (227.75, 163.75)),
        ((387.75, 163.75), (355.75, 163.75)),
        ((323.75, 163.75), (291.75, 163.75)),
        ((419.75, 195.75), (387.75, 195.75)),
        ((387.75, 259.75), (419.75, 259.75)),
        ((355.75, 163.75), (323.75, 163.75)),
        ((387.75, 195.75), (387.75, 163.75)),
        ((419.75, 227.75), (419.75, 195.75)),
        ((419.75, 259.75), (419.75, 227.75))
    ]

    star_path = a_star(start, goal, grid)[0]

    assert tuple(path) == star_path
