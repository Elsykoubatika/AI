import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add (self, node):
        self.frontier.append(node)
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    
class QueueFrontier(StackFrontier):
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
        
class Maze():
    
    def __init__(self, filname):
        
        # read file and set height and width of maze
        with open(filname) as f:
            contents = f.read()
            
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        
        # determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        # keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(True)
            self.walls.append(row)
        self.solution = None
        
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
    
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        # Ensure actions are valid
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    def solve(self):
        """finds a solution to maze, if one exists"""
        self.num_explored = 0
        
        # initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)
        
        # initialize an empty explored set
        self.explored = set()
        
        # keep looping until solution found
        while True:
            
            # if nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            
            # choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            
            # if node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # mark node as explored
            self.explored.add(node.state)
            
            # add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2
        
        # create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        
        solution = self.solution[1] if self.solution is not None else None
        
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)
                elif (i, j) == self.start:
                    fill = (0, 255, 0)
                elif (i, j) == self.goal:
                    fill = (255, 0, 0)
                elif solution is not None and (i, j) in solution:
                    fill = (255, 255, 0)
                else:
                    fill = (0, 0, 0)

                # draw the cell
                x0 = j * cell_size
                y0 = i * cell_size
                x1 = x0 + cell_size - cell_border
                y1 = y0 + cell_size - cell_border
                draw.rectangle([x0, y0, x1, y1], fill=fill)

        # save the image
        img.save(filename)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze_medium_4.txt")
    m = Maze(sys.argv[1])
    print("Maze:")
    m.print()
    try:
        # Optionnel: BFS pour le plus court chemin
        # Remplace m.solve() par:
        m.solve()  # ou appelle une version BFS si tu l'as codée
        print("Solution:")
        m.print()
    except Exception as e:
        print(e)  # "no solution"
    finally:
        # Toujours sortir une image de debug
        m.output_image("maze_debug.png", show_explored=True)
        print("Image écrite: maze_debug.png")
