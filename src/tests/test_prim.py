import pytest
import math
from algorithms import prim
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


def test_passage_class():
    edge = ((1,1),(2,3))
    passage = Passage(edge[0], edge[1], None, None, 2)

    class_info = (passage.a, passage.b, passage.color, passage.screen, passage.w, passage.d)
    d = math.sqrt((1-2)**2+(1-3)**2)
    info = ((1,1), (2,3), None, None, 2, d)

    assert info == class_info


def test_prim_with_two_rooms():
    passages = []
    edges = {((1,1),(2,3))}
    number = 2

    for edge in edges:
        passages.append(Passage(edge[0], edge[1], None, None, 2))

    mst = {((1,1), (2,3))}

    assert mst == prim(passages, number)


def test_prim_with_three_rooms():
    passages = []
    number = 3
    edges = {
        ((1,1),(2,3)),
        ((1,1),(1,4)),
        ((1,4),(2,3))
        }

    for edge in edges:
        passages.append(Passage(edge[0], edge[1], None, None, 2))

    mst = {((2,3),(1,4)),((1,1), (2,3))}

    assert mst == prim(passages, number)


def test_prim_with_ten_rooms():
    passages = []
    number = 10
    edges = {
        ((2, 4), (3, 2)), ((3, 2), (32, 2)), ((2, 3), (2, 4)), 
        ((5, 11), (32, 2)), ((32, 2), (32, 23)), ((2, 3), (3, 2)), 
        ((12, 76), (20, 51)), ((1, 4), (5, 11)), ((5, 11), (32, 23)), 
        ((5, 11), (12, 76)), ((2, 4), (5, 11)), ((1, 1), (2, 3)), 
        ((1, 1), (2, 4)), ((1, 4), (2, 3)), ((5, 11), (20, 51)), 
        ((3, 2), (5, 11)), ((1, 4), (2, 4)), ((20, 51), (32, 23)), 
        ((1, 4), (12, 76)), ((1, 1), (1, 4)), ((12, 76), (32, 23))
             }

    for edge in edges:
        passages.append(Passage(edge[0], edge[1], None, None, 2))

    mst = {
         ((2,4),(2,3)),((2,4),(1,4)),((32, 2), (32, 23)),
         ((32, 23), (20, 51)),((20, 51), (12, 76)),((2, 3), (3, 2)),
         ((2, 3), (1, 1)), ((5,11),(32,2)),((2,4),(5,11))
         }         

    assert mst == prim(passages, number)


def test_through_all_rooms():
    passages = []
    number = 3
    prim_points = set()
    points = set([(1,1), (1,4), (2,3)])
    edges = {
        ((1,1),(2,3)),
        ((1,1),(1,4)),
        ((1,4),(2,3))
        }
    
    for edge in edges:
        passages.append(Passage(edge[0], edge[1], None, None, 2))

    prim_mst = prim(passages, number)
    for passage in prim_mst:
        for point in passage:
            prim_points.add(point)

    assert points == prim_points