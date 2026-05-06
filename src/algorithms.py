
import math
from formulae import center, manhattan_distance as md


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
    vertices = set()

    if len(passages) == 0:
        return mst

    first_vertex = passages[0].a

    edges = {edge : first_vertex for edge in [edge for edge in passages if edge.a == first_vertex or edge.b == first_vertex]}
    vertex = first_vertex
    i = 0

    while len(mst) < number_of_rooms-1:
        min_edge, vertex = min(edges.items(), key=lambda item: item[0].d)

        a = vertex
        new_vertex = min_edge.a if min_edge.a != vertex else min_edge.b


        if new_vertex in vertices:
            edges.pop(min_edge)
            continue

        mst.add((vertex, new_vertex))
        vertices.add(vertex)
        vertices.add(new_vertex)
    
        for edge in [edge for edge in passages if edge.a == new_vertex or edge.b == new_vertex]:
            a = new_vertex
            b = edge.a if edge.a != new_vertex else edge.b
            if b not in vertices:
                edges[edge] = new_vertex

        edges.pop(min_edge)


        vertex = new_vertex
        i += 1

    return mst

def neighbors(pos):
    neighbors = []

    x = pos[0]
    y = pos[1]

    moves = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

    for move in moves:
        a = move[0]
        b = move[1]
        if a < 28 and a > -1 and b < 28 and b > -1:
            neighbors.append((a, b))

    return neighbors

def a_star(start, goal, grid):
    
    open_list = [start]
    open_dict = {start['pos']: start}
    closed_list = []

    start['h'] = md(start['pos'], goal['pos'], start['cost'])
    start['f'] = start['g'] + start['h']

    while len(open_list) > 0:
        open_list.sort(key=lambda item : item['f'])

        current = open_list[0]

        if current['pos'] == goal['pos']:
            return reconstruct_path(current, grid)
        
        open_list.pop(0)
        closed_list.append(current)


        neighbor_positions = neighbors(current['pos'])

        for n_pos in neighbor_positions:
            n_cost = grid[n_pos[1],n_pos[0]]

            if n_pos in set([item['pos'] for item in closed_list]):
                continue

            maybe_g = current['g'] + md(current['pos'], n_pos, current['cost'])

            if n_pos not in open_dict:
                h = md(n_pos, goal['pos'], n_cost)
                n = {'pos':n_pos, 'g': maybe_g, 'h': h, 'parent': current, 'f': maybe_g+h, 'cost':n_cost}
                open_list.append(n)
                open_dict[n_pos] = n

            elif maybe_g < open_dict[n_pos]['g']:
                n = open_dict[n_pos]
                n['parent'] = current
                n['g'] = maybe_g
                n['f'] = n['g'] + n['h']


def reconstruct_path(current, grid):

    path = set()
    path_as_edges = set()
    pres = None

    while current is not None:
        pres = current['pos']

        if grid[pres[1],pres[0]] != 9:
            grid[pres[1],pres[0]] = 0

        path.add(current['pos'])
        current = current['parent']

        if current != None:
            edge = (pres[0]*32+67.75, pres[1]*32+67.75), (current['pos'][0]*32+67.75, current['pos'][1]*32+67.75)
            path_as_edges.add(edge)

    return tuple(path_as_edges)