import pytest
from formulae import center, line_through_two_points, perpendicular_bisector_line, vertex, manhattan_distance

def test_center():
    q = (1,2)
    p = (2,6)
    r = (6,2)

    center_should_be = (3,3)
    form_center = center(q, p, r)

    assert center_should_be == form_center

def test_line_through_two_points():
    a, b, c = 0.0, 0.0, 0.0
    q = (1,2)
    p = (2,6)

    form_line = line_through_two_points(q, p, a, b, c)
    line_should_be = 4, -1, 2

    assert line_should_be == form_line

def test_perpendicular_bisector_line():
    q = (1,2)
    r = (6,2)
    a = 4
    b = -1
    c = 2

    bisector = perpendicular_bisector_line(q, r, a, b, c)
    bisector_should_be = 1, 4, 11

    assert bisector_should_be == bisector

def test_vertex():
    a = 1
    b = 4
    c = 17
    e = 5
    f = 0
    g = 15

    form_vertex = vertex(a, b, c, e, f, g)
    vertex_should_be = (3,3)

    assert vertex_should_be == form_vertex


#def test_md():
#    a = (5, 4)
#    b = (4, 6)
#    cost = 9

#    md_should_be = 3 + 9*100000
#    form_md = manhattan_distance(a, b)

#    assert md_should_be == form_md