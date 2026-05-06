import pytest
from algorithms import triangulation

def test_triangulation_with_three_points():
    points = [(1,1), (1,4), (2,3)]

    edges = {((1,1),(2,3)),((1,1),(1,4)),((1,4),(2,3))}
    tri_edges = triangulation(points, 1000, 1000)
    assert edges == tri_edges

def test_triangulation_with_ten_points():
    points = [
        (1,1), (1,4), (2,3),
        (2,4), (3,2), (5,11),
        (12,76), (20,51), (32,2),
        (32, 23)
        ]

    edges = {
        ((2, 4), (3, 2)), ((3, 2), (32, 2)), ((2, 3), (2, 4)), 
        ((5, 11), (32, 2)), ((32, 2), (32, 23)), ((2, 3), (3, 2)), 
        ((12, 76), (20, 51)), ((1, 4), (5, 11)), ((5, 11), (32, 23)), 
        ((5, 11), (12, 76)), ((2, 4), (5, 11)), ((1, 1), (2, 3)), 
        ((1, 1), (2, 4)), ((1, 4), (2, 3)), ((5, 11), (20, 51)), 
        ((3, 2), (5, 11)), ((1, 4), (2, 4)), ((20, 51), (32, 23)), 
        ((1, 4), (12, 76)), ((1, 1), (1, 4)), ((12, 76), (32, 23))
             }
    
    tri_edges = triangulation(points, 1000, 1000)
    assert edges == tri_edges

def test_triangulation_with_points_in_a_line():
    points = [(3,3), (3,4), (3,5)]

    edges = {
        ((3,3),(3,4)),
        ((3,3),(3,5)),
        ((3,4),(3,5))
    }

    tri_edges = triangulation(points, 1000, 1000)
    assert edges == tri_edges

def test_triangulation_with_no_points():
    points = []

    edges = set()

    tri_edges = triangulation(points, 1000, 1000)
    assert edges == tri_edges