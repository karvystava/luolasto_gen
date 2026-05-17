import pytest
from algorithms import triangulation


def test_triangulation_with_ten_points():
    points = [
        (3,2), (7,1), (8,3),
        (4,4), (6,4), (5,6),
        (3,7), (8,6), (4,8),
        (7,8)
        ]
    
    tri_edges = triangulation(points, 1000, 1000)

    assert ((3,2), (7,1)) in tri_edges or ((7,1), (3,2)) in tri_edges
    assert ((8,3), (7,1)) in tri_edges or ((7,1), (8,3)) in tri_edges
    assert ((6,4), (7,1)) in tri_edges or ((7,1), (6,4)) in tri_edges

    assert ((4,4), (6,4)) in tri_edges or ((6,4), (4,4)) in tri_edges
    assert ((4,4), (3,2)) in tri_edges or ((3,2), (4,4)) in tri_edges
    assert ((4,4), (3,7)) in tri_edges or ((3,7), (4,4)) in tri_edges
    assert ((4,4), (5,6)) in tri_edges or ((5,6), (4,4)) in tri_edges

    assert ((8,3), (6,4)) in tri_edges or ((6,4), (8,3)) in tri_edges
    assert ((8,6), (6,4)) in tri_edges or ((6,4), (8,6)) in tri_edges
    assert ((5,6), (6,4)) in tri_edges or ((6,4), (5,6)) in tri_edges
    assert ((3,2), (6,4)) in tri_edges or ((6,4), (3,2)) in tri_edges

    assert ((3,2), (3,7)) in tri_edges or ((3,7), (3,2)) in tri_edges
    assert ((5,6), (3,7)) in tri_edges or ((3,7), (5,6)) in tri_edges
    assert ((4,8), (3,7)) in tri_edges or ((3,7), (4,8)) in tri_edges

    assert ((4,8), (5,6)) in tri_edges or ((5,6), (4,8)) in tri_edges
    assert ((4,8), (7,8)) in tri_edges or ((7,8), (4,8)) in tri_edges

    assert ((5,6), (7,8)) in tri_edges or ((7,8), (5,6)) in tri_edges
    assert ((8,6), (7,8)) in tri_edges or ((7,8), (8,6)) in tri_edges

    assert ((8,6), (5,6)) in tri_edges or ((5,6), (8,6)) in tri_edges
    assert ((8,6), (8,3)) in tri_edges or ((8,3), (8,6)) in tri_edges


def test_triangulation_with_no_points():
    points = []
    edges = set()
    tri_edges = triangulation(points, 10, 10)
    assert edges == tri_edges