
def line_through_two_points(q, p, a, b, c):
    a = p[1]-q[1]
    b = q[0]-p[0]
    c = a * (q[0]) + b * (q[1])
    return a, b, c

def perpendicular_bisector_line(q, p, a, b, c):
    mid = [(q[0] + p[0])//2, (q[1] + p[1])//2]
    c = -b*(mid[0]) + a*(mid[1])
    t = a
    a = -b
    b = t
    return a, b, c

def vertex(a1, b1, c1, a2, b2, c2):
    det = a1*b2 - a2*b1
    if det == 0:
        return [(10.0)**19, (10.0)**19]
    x = (b2*c1 - b1*c2)//det
    y = (a1*c2 - a2*c1)//det
    return (x, y)

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
    xs = abs(a[0]-b[0])
    ys = abs(a[1]-b[1])
    md = (xs + ys) + (1+cost)*100000
    return md