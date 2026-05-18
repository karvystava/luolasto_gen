
import math
import heapq as hq
from formulae import center, manhattan_distance as md


def triangulation(room_points, screen_h, screen_w):

    # supertriangle is the first huge triangle that all points are in and 
    # which will be divided into smaller triangles which will be divided into smaller triangles etc
    # until there are no free points left

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

    # exclude edges connected to the supertriangle
    for tri_edges, tri in triangulation.items():
        add_edges = set([edge for edge in tri_edges if edge[0] not in supertri_points and edge[1] not in supertri_points])
        edges.update(add_edges)

    return edges


def prim(passages, number_of_rooms):

    # find minimum spanning tree: start with random start node, then find cheapest (shortest in this case) edge to next node,
    # then find cheapest next edge connected to either of the nodes now reached etc
    # ! with never connecting to a node that has already been visited

    mst = set()
    vertices = set() # aka nodes

    if len(passages) == 0:
        return mst

    first_vertex = passages[0].a

    # edges = {((x1,y1),(x2,xy)) aka the edge : the node it "starts" from}
    edges = {edge : first_vertex for edge in [edge for edge in passages if edge.a == first_vertex or edge.b == first_vertex]}
    vertex = first_vertex
    while len(mst) < number_of_rooms-1:

        min_edge, vertex = min(edges.items(), key=lambda item: item[0].d)
        new_vertex = min_edge.a if min_edge.a != vertex else min_edge.b

        if new_vertex in vertices:
            edges.pop(min_edge)
            continue

        mst.add((vertex, new_vertex))
        vertices.add(vertex)
        vertices.add(new_vertex)
    
        for edge in [edge for edge in passages if edge.a == new_vertex or edge.b == new_vertex]:
            b = edge.a if edge.a != new_vertex else edge.b

            if b not in vertices:
                edges[edge] = new_vertex

        edges.pop(min_edge)

        vertex = new_vertex

    return mst


def neighbors(pos):

    # help function for A*
    # get valid neighbor positions around a point in the grid

    neighbors = []

    x = pos[0]
    y = pos[1]

    moves = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

    for move in moves:
        a = move[0]
        b = move[1]
        if a < 28 and a > -1 and b < 28 and b > -1: # grid limits (0-27)
            neighbors.append((a, b))

    return neighbors


def a_star(start, goal, grid):

    # find best (cheapest) path between nodes (rooms) in the grid (map)
    # get all paths through the nodes (map) and their cost
    # return cheapest path

    start['h'] = md(start['pos'], goal['pos']) # h aka the heuristic cost function aka md from formulae.py
    start['f'] = start['g'] + start['h']

    open_list = [(start['f'], start['pos'])]
    open_dict = {start['pos']: start}
    closed_set = set()

    while len(open_list) > 0:

        f, c_pos = hq.heappop(open_list)
        current = open_dict[c_pos]

        if current['pos'] == goal['pos']:
            return reconstruct_path(current, grid)
        
        closed_set.add(current['pos'])

        neighbor_positions = neighbors(current['pos'])
        for n_pos in neighbor_positions:
            if n_pos in closed_set:
                continue

            maybe_g = current['g'] + md(current['pos'], n_pos)

            if n_pos not in open_dict:
                h = md(n_pos, goal['pos'])
                n = {'pos':n_pos, 'g': maybe_g, 'h': h, 'parent': current, 'f': maybe_g+h}
                open_list.append((n['f'], n_pos))
                open_dict[n_pos] = n

            elif maybe_g < current['g']:
                n = open_dict[n_pos]
                n['parent'] = current
                n['g'] = maybe_g
                n['f'] = n['g'] + n['h']


def reconstruct_path(current, grid):

    # reconstructing best path given by A* into sets of nodes and edges
    # current = best path according to A*

    path = [] # path in grid terms (to make testing and debugging easier)
    path_as_edges = set() # path as pixel edges for map
    pres = None
    current_length = current['g']

    while current is not None:
        pres = current['pos']

        if grid[pres[1],pres[0]] != 4:
            grid[pres[1],pres[0]] = 1 # add new hallway tile to grid unless in a room

        path.append(current['pos'])
        current = current['parent']

        if current != None:
            # approximated transposing from grid to pixel
            edge = (pres[0]*32+67.75, pres[1]*32+67.75), (current['pos'][0]*32+67.75, current['pos'][1]*32+67.75)
            path_as_edges.add(edge)

    return tuple(path_as_edges), tuple(path), current_length