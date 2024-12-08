from flask import Flask, render_template, request, jsonify
import heapq
import math

app = Flask(__name__)

class Node:
    def __init__(self, x, y, g=float('inf'), h=0):
        self.x = x
        self.y = y
        self.g = g  
        self.h = h  
        self.f = g + h 
        self.parent = None

def heuristic(node, goal):
    return math.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2)

def get_neighbors(node, grid_size):
    neighbors = []
    directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
    
    for dx, dy in directions:
        new_x = node.x + dx
        new_y = node.y + dy
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            neighbors.append(Node(new_x, new_y))
    return neighbors

def a_star(start_pos, goal_pos, grid_size):
    start = Node(start_pos[0], start_pos[1], 0)
    goal = Node(goal_pos[0], goal_pos[1])
    
    open_set = []
    closed_set = set()
    
    start.h = heuristic(start, goal)
    start.f = start.g + start.h
    
    heapq.heappush(open_set, (start.f, id(start), start))
    
    while open_set:
        current = heapq.heappop(open_set)[2]
        
        if (current.x, current.y) == (goal.x, goal.y):
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]
            
        closed_set.add((current.x, current.y))
        
        for neighbor in get_neighbors(current, grid_size):
            if (neighbor.x, neighbor.y) in closed_set:
                continue
                
            tentative_g = current.g + math.sqrt((current.x - neighbor.x)**2 + 
                                              (current.y - neighbor.y)**2)
            
            if tentative_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                
                heapq.heappush(open_set, (neighbor.f, id(neighbor), neighbor))
    
    return None
@app.route('/')
def nav():
    return render_template('navigation.html')
@app.route('/find')
def index():
    return render_template('index.html')

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()
    start = data['start']
    goal = data['goal']
    grid_size = data['gridSize']
    
    path = a_star((start['x'], start['y']), (goal['x'], goal['y']), grid_size)
    
    return jsonify({'path': path})

if __name__ == '__main__':
    app.run(debug=True, port = 8080)
