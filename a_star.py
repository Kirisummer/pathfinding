from typing import Set, List, Dict, Tuple, Callable, NamedTuple

class Point(NamedTuple):
    y: int
    x: int

    def __str__(self):
        return str(tuple(self))


# A* search components
def choose(reach: Set[Point], cost: Callable[[Point], float]) -> Point:
    return min(reach, key=lambda p: cost(p))


def build_path(point: Point, prev: Dict[Point, Point]) -> List[Point]:
    path = []
    while prev.get(point) != None:
        path.append(point)
        point = prev[point]
    return path[::-1]


def update_reach(reach: Set[Point], field: Tuple[str], block: str, point: Point,
       seen: Set[Point], costs: Dict[Point, float], prev: Dict[Point, Point],
       cost: Callable[[Point], float], adjacent: Callable[[Point], Set[Point]]):
    new_reach = {adj for adj in (adjacent(point) - seen) \
                        if field[adj.y][adj.x] not in block}
    for adj in new_reach:
        if adj not in reach:
            prev[adj] = point
            reach.add(adj)
        point_cost = costs.get(point, -1)
        adj_cost = costs.get(point, -1)
        if point_cost + 1 < adj_cost:
            prev[adj] = point
            costs[adj] = point_cost + 1


def find_path(field: Tuple[str], start: Point, end: Point, block: str, 
    cost: Callable[[Point], float], adjacent: Callable[[Point], Set[Point]]):
    ''' Find the best path from start to the end on the field with blocks using cost function with A*
    
    Arguments:
        field: Tuple[str] - a representation the contents of the field
        start: Point - start
        end: Point - goal
        block: str - a string of characters to be used as obstacles
        cost: Callable[[Point], float] - distance to the goal. 
        adjacent: Callable[[Point], Set[Point]] - adjacent points
    '''

    costs = {} # Costs of points
    prev = {}  # Previous points
    reach = {start} # Points that are able to be reached
    seen = set() # Seen points

    while len(reach):
        point = choose(reach, cost)
        if point == end:
            return build_path(point, prev)
        reach.discard(point)
        seen.add(point)
        update_reach(reach, field, block, point, seen, costs, prev, cost, adjacent)
    # If we get there, there is no path
    return None
