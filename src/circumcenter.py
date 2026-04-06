
def line_through_two_points(Q, P, a, b, c):
    a = P[1]-Q[1]
    b = Q[0]-P[0]
    c = a * (Q[0]) + b * (Q[1])
    return a, b, c

def perpendicular_bisector_line(Q, P, a, b, c):
    mid = [(Q[0] + P[0])//2, (Q[1] + P[1])//2]
    c = -b*(mid[0]) + a*(mid[1])
    t = a
    a = -b
    b = t
    return a, b, c

def vertex(a1, b1, c1, a2, b2, c2):
    det = a1*b2 - a2*b1
    if det == 0:
        return [(10.0)**19, (10.0)**19]
    else:
        x = (b2*c1 - b1*c2)//det
        y = (a1*c2 - a2*c1)//det
        return (x, y)

def center(Q, P, R):

    a, b, c = 0.0, 0.0, 0.0
    a, b, c = line_through_two_points(Q, P, a, b, c)

    e, f, g = 0.0, 0.0, 0.0
    e, f, g = line_through_two_points(P, R, e, f, g)

    a, b, c = perpendicular_bisector_line(Q, P, a, b, c)
    e, f, g = perpendicular_bisector_line(P, R, e, f, g)

    circumcenter = vertex(a, b, c, e, f, g)
    return circumcenter