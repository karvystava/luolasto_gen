
# find line through points q and p
def line_through_two_points(q, p, a, b, c):
    a = p[1]-q[1]
    b = q[0]-p[0]
    c = a * (q[0]) + b * (q[1])
    return a, b, c

# find perpendicular bisector line for a line through q and p(helper for center)
def perpendicular_bisector_line(q, p, a, b, c):
    mid = [(q[0] + p[0])//2, (q[1] + p[1])//2]
    c = -b*(mid[0]) + a*(mid[1])
    t = a
    a = -b
    b = t
    return a, b, c

# get vertex of two lines (helper for center)
def vertex(a1, b1, c1, a2, b2, c2):
    det = a1*b2 - a2*b1
    if det == 0:
        return ((10.0)**19, (10.0)**19)
    x = (b2*c1 - b1*c2)//det
    y = (a1*c2 - a2*c1)//det
    return (x, y)

# formula to get circumcenter for triangulation
def center(q, p, r):

    a, b, c = 0.0, 0.0, 0.0
    a, b, c = line_through_two_points(q, p, a, b, c)

    e, f, g = 0.0, 0.0, 0.0
    e, f, g = line_through_two_points(p, r, e, f, g)

    a, b, c = perpendicular_bisector_line(q, p, a, b, c)
    e, f, g = perpendicular_bisector_line(p, r, e, f, g)

    circumcenter = vertex(a, b, c, e, f, g)
    return circumcenter


def manhattan_distance(a, b, cost):

    # heuristic cost function for A*
    # manhattan distance because in a grid you can only go straight up, down, left or right
    # added cost to make it very expensive to go through rooms
    # and very cheap to use already established hallways

    xs = abs(a[0]-b[0])
    ys = abs(a[1]-b[1])
    md = (xs + ys) + cost*100000
    return md