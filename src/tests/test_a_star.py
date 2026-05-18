import pygame
import numpy as np
from random import randint
from formulae import manhattan_distance as md
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



def test_a_star_length():

    grid = np.full(784, 2, dtype=int).reshape(28, 28)
    start = {'pos':(randint(0,27),randint(0,27)), 'g':0.0, 'h':0.0, 'parent':None}
    goal = {'pos':(randint(0,27),randint(0,27)), 'g':0.0, 'h':0.0, 'parent':None}

    test_a_star = a_star(start, goal, grid)
    test_path = list(test_a_star[1])
    test_length = test_a_star[2]

    goal_length = 0
    for i in range(len(test_path)-1):
        goal_length += md(test_path[i], test_path[i+1])


    assert goal_length == test_length


