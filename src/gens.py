from random import randint
import math
from circumcenter import center


def gen_rooms(number_of_rooms, screen_w, screen_h):
    rooms = []
    for _ in range(number_of_rooms-1):
        while True:
            again = False
            h = randint(70,220)
            w = randint(70,220)
            x = randint(20, screen_w-20-w)
            y = randint(20, screen_h-20-h)

            for room in rooms:
                x_mez = sorted([(x, w), (room["x"], room["w"])], key=lambda x:x[0], reverse=True)
                y_mez = sorted([(y, h), (room["y"], room["h"])], key=lambda x:x[0], reverse=True)
                if x_mez[0][0] - x_mez[1][0] - x_mez[1][1] < 0 and y_mez[0][0] - y_mez[1][0] - y_mez[1][1] < 0:
                    again = True
                    break

            if again:
                continue
            room_dict = {"h":h, "w":w, "x":x, "y":y}
            rooms.append(room_dict)
            break

    return rooms


def triangulation(room_points, screen_h, screen_w):
    supertri_points = ((0,0), (0, screen_h*2), (screen_w*2,0))
    supertri_edges = (((0,0), (0,screen_h*2)), ((0,0), (screen_w*2,0)), ((screen_w*2,0), (0,screen_h*2)))
    supertri_circumcenter = center((0,0), (0, screen_h*2), (screen_w*2,0))

    supertri = {'circum':(supertri_circumcenter, math.dist((0,0), supertri_circumcenter)), 'points':set(supertri_points)}
    triangulation = {}
    edges = set()
    triangulation[supertri_edges] = supertri

    for point in room_points:

        bad_triangles = set()
        bad_edges = {}
        for tri_edges, tri in triangulation.items():
            if math.dist(point, tri['circum'][0]) <= tri['circum'][1]:
                bad_triangles.add(tri_edges)
                for edge in tri_edges:
                    if edge not in bad_edges:
                        bad_edges[edge] = 0
                    bad_edges[edge] += 1

        polygon = set()
        for triangle in bad_triangles:
            for edge in triangle:
                if bad_edges[edge] == 1:
                    polygon.add(edge)
            triangulation.pop(triangle)

        for edge in polygon:
            new_edges = tuple(sorted((tuple(sorted(edge)), tuple(sorted((edge[0], point))), tuple(sorted((edge[1], point))))))
            new_circ = center(edge[0], edge[1], point)
            triangulation[new_edges] = {'circum':(new_circ, math.dist(new_circ, point)), 'points':set((edge[0], edge[1], point))}

    for tri_edges, tri in triangulation.items():
        if len(tri['points'] - set(supertri_points)) == 3:
            edges.update(tri_edges)

    return edges


def prim(passages, number_of_rooms):
    mst = set()

    first_vertex = passages[0].a
    print('first vertex:', first_vertex)

    edges = {edge : first_vertex for edge in [edge for edge in passages if edge.a == first_vertex or edge.b == first_vertex]}
    print('first vertex edges', edges)
    vertex = first_vertex

    while len(mst) < number_of_rooms-1:
        print("mst length", len(mst))
        print("room number", number_of_rooms)
        print(min(edges.items(), key=lambda item: item[0].d))
        min_edge, vertex = min(edges.items(), key=lambda item: item[0].d)
        new_vertex = min_edge.a if min_edge.a != vertex else min_edge.b

        mst.add((vertex, new_vertex))
        for edge in [edge for edge in passages if edge.a == new_vertex or edge.b == new_vertex]:
            if (edge.a, edge.b) not in mst or (edge.b, edge.a) not in mst:
                edges[edge] = new_vertex

        edges.pop(min_edge)
        vertex = new_vertex

    return mst