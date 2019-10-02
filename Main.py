from tkinter import Canvas, messagebox, Tk
from fractions import Fraction


# Redraw the robot using the top point
def draw_robot(canvas, topX, topY, old_lines=None):
    # Calculate left and right points
    rightX = topX + 5
    rightY = topY + 5
    leftX = topX - 5
    leftY = topY + 5
    
    # Delete old lines if they exist
    if old_lines is not None:
        for line in old_lines:
            canvas.delete(line)
    
    # Draw and return new lines
    return [canvas.create_line(topX, topY, rightX, rightY),
            canvas.create_line(rightX, rightY, leftX, leftY),
            canvas.create_line(leftX, leftY, topX, topY)]


def draw_5_sided(canvas, startX, startY):
    top_rightX = startX + 10
    top_rightY = startY + 5
    bottom_rightX = startX + 10
    bottom_rightY = startY + 10
    bottom_leftX = startX - 10
    bottom_leftY = startY + 10
    top_leftX = startX - 10
    top_leftY = startY + 5

    # Draw obstacle
    canvas.create_line(startX, startY, top_rightX, top_rightY)
    canvas.create_line(top_rightX, top_rightY, bottom_rightX, bottom_rightY)
    canvas.create_line(bottom_rightX, bottom_rightY, bottom_leftX, bottom_leftY)
    canvas.create_line(bottom_leftX, bottom_leftY, top_leftX, top_leftY)
    canvas.create_line(top_leftX, top_leftY, startX, startY)

    # Return vertices
    return [(startX, startY), (top_rightX, top_rightY), (bottom_rightX, bottom_rightY),
            (bottom_leftX, bottom_leftY), (top_leftX, top_leftY)]


def draw_4_sided(canvas, startX, startY):
    top_rightX = startX + 10
    top_rightY = startY
    bottom_rightX = startX + 15
    bottom_rightY = startY + 10
    bottom_leftX = startX - 5
    bottom_leftY = startY + 10
    
    # Draw obstacle
    canvas.create_line(startX, startY, top_rightX, top_rightY)
    canvas.create_line(top_rightX, top_rightY, bottom_rightX, bottom_rightY)
    canvas.create_line(bottom_rightX, bottom_rightY, bottom_leftX, bottom_rightY)
    canvas.create_line(bottom_leftX, bottom_leftY, startX, startY)
    
    # Return vertices
    return [(startX, startY), (top_rightX, top_rightY), (bottom_rightX, bottom_rightY), (bottom_leftX, bottom_leftY)]


def draw_3_sided(canvas, startX, startY):
    leftX = startX - 10
    leftY = startY + 10
    rightX = startX + 10
    rightY = startY + 10

    canvas.create_line(startX, startY, rightX, rightY)
    canvas.create_line(rightX, rightY, leftX, leftY)
    canvas.create_line(leftX, leftY, startX, startY)

    return [(startX, startY), (rightX, rightY), (leftX, leftY)]


def draw_virtual_obstacles(maze, obstacle_list, canvas):
    for vert_list in obstacle_list:
        for enum_index, current_vert in enumerate(vert_list):
            # If you are at the last vertex then use first vertex
            if enum_index == len(vert_list) - 1:
                next_vert = vert_list[0]
            else:
                next_vert = vert_list[enum_index + 1]

            if current_vert[0] - next_vert[0] == 0:
                rise = 1 if current_vert[1] - next_vert[1] > 0 else -1
                run = 0

            else:
                slope = Fraction(current_vert[1] - next_vert[1], current_vert[0] - next_vert[0])
                rise = slope.numerator
                run = slope.denominator
            
            if run > 0 and rise == 0 and current_vert[0] - next_vert[0] > 0:
                canvas.create_line(current_vert[0] - 5, current_vert[1] + 5,
                                   next_vert[0] - 5, next_vert[1] + 5, fill="blue")

                canvas.create_line(current_vert[0], current_vert[1],
                                   current_vert[0] - 5, current_vert[1] + 5, fill="blue")
                
                canvas.create_line(next_vert[0] - 5, next_vert[1] + 5, next_vert[0] - 10, next_vert[1], fill="blue")

            elif (run < 0 > rise) or (run > 0 > rise) or \
                    (rise > 0 < current_vert[1] - next_vert[1] and run == 0):
                canvas.create_line(current_vert[0] - 10, current_vert[1],
                                   next_vert[0] - 10, next_vert[1], fill="blue")

                canvas.create_line(next_vert[0], next_vert[1], next_vert[0] - 10, next_vert[1], fill="blue")

            else:
                canvas.create_line(current_vert[0], current_vert[1], next_vert[0], next_vert[1], fill="red")

            x = current_vert[0]
            y = current_vert[1]
            print("Rise: " + str(rise) + "\nRun: " + str(run))
            while x != next_vert[0] and y != next_vert[1]:
                maze[y][x] = 1
                for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    maze
                x += run
                y += rise


def get_path(maze, startX, startY, endX, endY):
    start_node = Node(startX, startY, None)
    end_node = Node(endX, endY, None)

    node_list = []  # List of nodes able to travel to
    closed_list = []  # List of nodes unable to travel to or already visited
    node_list.append(start_node)

    # Loop until no Nodes are left
    while len(node_list) > 0:
        current_index = 0
        current_node = node_list[current_index]

        # Search node_list for the Node with the lowest F
        for enum_index, enum_node in enumerate(node_list):
            if enum_node.f < current_node.f:
                current_node = enum_node
                current_index = enum_index

        node_list.pop(current_index)
        closed_list.append(current_node)

        # End has been reached
        if current_node == end_node:
            return_path = []
            while current_node is not None:
                return_path.append(current_node)
                current_node = current_node.parent
            return return_path[::-1]  # Reverse list and return

        # Find neighboring Nodes
        neighbors = []
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_posX = current_node.posX + new_pos[0]
            node_posY = current_node.posY + new_pos[1]

            # Skip if Node is not in range of the maze or if Node is an obstacle
            if node_posX > (len(maze) - 1) \
                    or \
                    node_posX < 0 \
                    or \
                    node_posY > (len(maze[len(maze) - 1]) - 1) \
                    or \
                    node_posY < 0 \
                    or \
                    maze[node_posX][node_posY] == 1:
                continue

            neighbor_node = Node(node_posX, node_posY, current_node)
            neighbors.append(neighbor_node)

        for new_pos in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_posX = current_node.posX + new_pos[0]
            node_posY = current_node.posY + new_pos[1]

            # Skip if Node is not in range of the maze or if Node is an obstacle
            if node_posX > (len(maze) - 1) \
                    or \
                    node_posX < 0 \
                    or \
                    node_posY > (len(maze[len(maze) - 1]) - 1) \
                    or \
                    node_posY < 0 \
                    or \
                    maze[node_posX][node_posY] == 1:
                continue

            # Can't move diagonally though 2 adjacent obstacles
            if maze[current_node.posX + new_pos[0]][current_node.posY] == 1 \
                    or \
                    maze[current_node.posX][current_node.posY + new_pos[1]] == 1:
                continue

            if

            neighbor_node = Node(node_posX, node_posY, current_node)
            neighbors.append(neighbor_node)

        # Find the next Node to travel to
        for neighbor in neighbors:
            # Skip if neighbor is already in closed list
            if neighbor in closed_list:
                continue

            # Calculate f, g, and h
            neighbor.g = current_node.g + 1
            # Using Pythagorean's Theorem
            neighbor.h = ((neighbor.posX - end_node.posX) ** 2) + \
                         ((neighbor.posY - end_node.posY) ** 2)
            neighbor.f = neighbor.g + neighbor.h

            # Skip if the neighbor is already in open list and has been visited before
            skip_node = False
            for open_node in node_list:
                if neighbor == open_node and neighbor.g > open_node.g:
                    skip_node = True
                    break
            if skip_node:
                continue

            # Add the neighbor to node_list
            node_list.append(neighbor)


def draw_line(canvas, master, oldX, oldY, newX, newY):
    canvas.create_line(oldX, oldY, newX, newY)
    master.update()


class Node:
    def __init__(self, posX, posY, parent):
        self.posX = posX
        self.posY = posY
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return other.posX == self.posX and other.posY == self.posY


def main():
    # Create a Canvas in a 750x750 window
    master = Tk()
    master.geometry("75x75")
    canvas = Canvas(master, width=75, height=75)

    # Create a 750x750 array to store virtual objects
    maze = [[0 for _ in range(75)] for _ in range(75)]

    # Draw robot triangle
    robot_topX = 30
    robot_topY = 19
    canvas.pack()
    draw_robot(canvas, robot_topX, robot_topY)

    # Destination
    destX = 55
    destY = 55
    rightX = destX + 5
    rightY = destY + 5
    leftX = destX - 5
    leftY = destY + 5

    # Draw and return new lines
    canvas.create_line(destX, destY, rightX, rightY)
    canvas.create_line(rightX, rightY, leftX, leftY)
    canvas.create_line(leftX, leftY, destX, destY)

    # Store all obstacle's vertices in a list
    obstacle_list = []

    # Draw obstacle
    obstacle_list.append(draw_5_sided(canvas, 35, 25))

    draw_virtual_obstacles(maze, obstacle_list, canvas)

    path = get_path(maze, robot_topX, robot_topY, destX, destY)

    old_node = path[0]
    for index, node in enumerate(path):
        new_node = node
        master.after(ms=5, func=draw_line(canvas, master, old_node.posX, old_node.posY,
                                          new_node.posX, new_node.posY))
        old_node = new_node

    master.mainloop()


main()
