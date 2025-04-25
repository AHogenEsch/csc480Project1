import sys
import heapq

class State:
    def __init__(self, position, dirty, path=[]):
        self.position = position
        self.dirty = frozenset(dirty)
        self.path = path

    def __eq__(self, other):
        return self.position == other.position and self.dirty == other.dirty

    def __hash__(self):
        return hash((self.position, self.dirty))

def parse_world(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # Read and sanitize columns and rows
        cols_line = file.readline().strip()
        rows_line = file.readline().strip()
        
        if not cols_line.isdigit() or not rows_line.isdigit():
            raise ValueError("First two lines of the file must be integers (columns and rows).")
        
        cols = int(cols_line)
        rows = int(rows_line)
        
        grid = []
        for _ in range(rows):
            line = file.readline()
            if line == '':
                raise ValueError("Not enough rows provided in the world file.")
            grid.append(list(line.strip()))
        
        # Check grid has correct dimensions
        for row in grid:
            if len(row) > cols:
                raise ValueError("A row has more columns than specified.")
        
    dirty = set()
    start = None
    for y in range(rows):
        for x in range(cols):
            if x >= len(grid[y]):
                continue  # Treat missing cells as empty
            cell = grid[y][x]
            if cell == '*':
                dirty.add((x, y))
            elif cell == '@':
                start = (x, y)

    if start is None:
        raise ValueError("No robot start position '@' found in the world file.")
    
    return grid, start, dirty, cols, rows

def get_neighbors(pos, cols, rows, grid):
    x, y = pos
    directions = {'N': (x, y-1), 'S': (x, y+1), 'E': (x+1, y), 'W': (x-1, y)}
    valid = {}
    for action, (nx, ny) in directions.items():
        if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != '#':
            valid[action] = (nx, ny)
    return valid

def uniform_cost_search(grid, start, dirty, cols, rows):
    counter = 0  # Tie-breaker counter
    frontier = [(0, counter, State(start, dirty))]
    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while frontier:
        cost, _, state = heapq.heappop(frontier)
        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        if not state.dirty:
            for action in state.path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        if state.position in state.dirty:
            new_dirty = set(state.dirty)
            new_dirty.remove(state.position)
            counter += 1
            heapq.heappush(frontier, (cost+1, counter, State(state.position, new_dirty, state.path + ['V'])))
            nodes_generated += 1

        for action, new_pos in get_neighbors(state.position, cols, rows, grid).items():
            counter += 1
            new_state = State(new_pos, state.dirty, state.path + [action])
            heapq.heappush(frontier, (cost+1, counter, new_state))
            nodes_generated += 1


def depth_first_search(grid, start, dirty, cols, rows):
    stack = [State(start, dirty)]
    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        if not state.dirty:
            for action in state.path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        if state.position in state.dirty:
            new_dirty = set(state.dirty)
            new_dirty.remove(state.position)
            stack.append(State(state.position, new_dirty, state.path + ['V']))
            nodes_generated += 1

        for action, new_pos in get_neighbors(state.position, cols, rows, grid).items():
            new_state = State(new_pos, state.dirty, state.path + [action])
            stack.append(new_state)
            nodes_generated += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python planner.py [uniform-cost|depth-first] [world-file]")
        sys.exit(1)

    algo = sys.argv[1]
    file_path = sys.argv[2]
    
    try:
        grid, start, dirty, cols, rows = parse_world(file_path)
    except Exception as e:
        print("Error reading world file:", e)
        sys.exit(1)

    if algo == "uniform-cost":
        uniform_cost_search(grid, start, dirty, cols, rows)
    elif algo == "depth-first":
        depth_first_search(grid, start, dirty, cols, rows)
    else:
        print("Unknown algorithm:", algo)
