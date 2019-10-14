from math import sqrt
from tkinter import Canvas, Tk
from fractions import Fraction
import numpy as np
import matplotlib.path as path
from random import randint, uniform


# TODO: Extend vertex on top to avoid vertex on line

# Draw the robot using the left point
def draw_robot(canvas, leftX, leftY, old_lines=None):
    # Calculate left and right points
    rightX = leftX + 50
    rightY = leftY
    topX = leftX + 25
    topY = leftY - 25
    
    # Delete old lines if they exist
    if old_lines is not None:
        for line in old_lines:
            canvas.delete(line)
    
    # Draw and return new lines
    return [canvas.create_line(topX, topY, rightX, rightY, fill="blue"),
            canvas.create_line(rightX, rightY, leftX, leftY, fill="blue"),
            canvas.create_line(leftX, leftY, topX, topY, fill="blue")]


def draw_5_sided(canvas, startX, startY, scale):
    
    top_rightX = startX + int(100 * scale)
    top_rightY = startY + int(50 * scale)
    bottom_rightX = startX + int(100 * scale)
    bottom_rightY = startY + int(100 * scale)
    bottom_leftX = startX - int(100 * scale)
    bottom_leftY = startY + int(100 * scale)
    top_leftX = startX - int(100 * scale)
    top_leftY = startY + int(50 * scale)
    
    canvas.create_line(startX, startY, top_rightX, top_rightY)
    canvas.create_line(top_rightX, top_rightY, bottom_rightX, bottom_rightY)
    canvas.create_line(bottom_rightX, bottom_rightY, bottom_leftX, bottom_leftY)
    canvas.create_line(bottom_leftX, bottom_leftY, top_leftX, top_leftY)
    canvas.create_line(top_leftX, top_leftY, startX, startY)
    
    return [(startX, startY), (top_rightX, top_rightY), (bottom_rightX, bottom_rightY),
            (bottom_leftX, bottom_leftY), (top_leftX, top_leftY)]


def draw_4_sided(canvas, startX, startY, scale):
    top_rightX = startX + int(100 * scale)
    top_rightY = startY
    bottom_rightX = startX + int(150 * scale)
    bottom_rightY = startY + int(100 * scale)
    bottom_leftX = startX - int(50 * scale)
    bottom_leftY = startY + int(100 * scale)
    
    canvas.create_line(startX, startY, top_rightX, top_rightY)
    canvas.create_line(top_rightX, top_rightY, bottom_rightX, bottom_rightY)
    canvas.create_line(bottom_rightX, bottom_rightY, bottom_leftX, bottom_rightY)
    canvas.create_line(bottom_leftX, bottom_leftY, startX, startY)
    
    return [(startX, startY), (top_rightX, top_rightY), (bottom_rightX, bottom_rightY), (bottom_leftX, bottom_leftY)]


def draw_3_sided(canvas, startX, startY, scale):
    leftX = startX - int(100 * scale)
    leftY = startY + int(100 * scale)
    rightX = startX + int(100 * scale)
    rightY = startY + int(100 * scale)
    
    canvas.create_line(startX, startY, rightX, rightY)
    canvas.create_line(rightX, rightY, leftX, leftY)
    canvas.create_line(leftX, leftY, startX, startY)
    
    return [(startX, startY), (rightX, rightY), (leftX, leftY)]


# Return rise and run for the line connecting the 2 given points
def get_slope(startX, startY, endX, endY):
    # Handle DivideByZero error
    if endX - startX == 0:
        rise = 1 if endY - startY > 0 else -1
        run = 0
    
    else:
        slope = Fraction(endY - startY, endX - startX)
        if endY - startY > 0:
            rise = abs(slope.numerator)
        else:
            rise = -abs(slope.numerator)
        
        if endX - startX > 0:
            run = abs(slope.denominator)
        else:
            run = -abs(slope.denominator)
    
    return rise, run


# Create virtual obstacles surrounding the given obstacles
def make_virtual_obstacles(obstacle_list, canvas, master):
    master_list = []
    
    # Loop through all obstacles
    for vert_list in obstacle_list:
        
        line_list = []  # Store all lines from the virtual obstacles
        
        # Loop through each vertex of each obstacle
        for enum_index, current_vert in enumerate(vert_list):
            
            # If you are at the last vertex then wrap around to first vertex
            if enum_index == len(vert_list) - 1:
                next_vert = vert_list[0]
            else:
                next_vert = vert_list[enum_index + 1]
            
            # Use slope to determine which side of the triangle to trace
            rise, run = get_slope(current_vert[0], current_vert[1], next_vert[0], next_vert[1])
            
            # Trace right point of robot triangle
            if rise < 0 and run == 0:
                draw_line(canvas, current_vert[0] - 50, current_vert[1],
                          next_vert[0] - 50, next_vert[1], fill="red")
                
                line_list.append([(current_vert[0] - 50, current_vert[1]),
                                  (next_vert[0] - 50, next_vert[1])])
            
            # Trace right point of robot triangle
            elif rise < 0 < run:
                master.after(1000, draw_line(canvas, current_vert[0] - 50, current_vert[1],
                                             next_vert[0] - 50, next_vert[1], fill="red"))
                
                line_list.append([(current_vert[0] - 50, current_vert[1]),
                                  (next_vert[0] - 50, next_vert[1])])
                
                master.after(1000, draw_line(canvas, next_vert[0] - 50, next_vert[1],
                                             next_vert[0], next_vert[1], fill="red"))
                
                line_list.append([(next_vert[0] - 50, next_vert[1]),
                                  (next_vert[0], next_vert[1])])
            
            # Trace top point of robot triangle
            elif rise == 0 and run < 0:
                master.after(750, draw_line(canvas, current_vert[0] - 25, current_vert[1] + 25,
                                            next_vert[0] - 25, next_vert[1] + 25, fill="red"))
                
                line_list.append([(current_vert[0] - 25, current_vert[1] + 25),
                                  (next_vert[0] - 25, next_vert[1] + 25)])
                
                master.after(750, draw_line(canvas, current_vert[0], current_vert[1],
                                            current_vert[0] - 25, current_vert[1] + 25, fill="red"))
                
                line_list.append([(current_vert[0], current_vert[1]),
                                  (current_vert[0] - 25, current_vert[1] + 25)])
                
                master.after(750, draw_line(canvas, next_vert[0] - 25, next_vert[1] + 25,
                                            next_vert[0] - 50, next_vert[1], fill="red"))
                
                line_list.append([(next_vert[0] - 25, next_vert[1] + 25),
                                  (next_vert[0] - 50, next_vert[1])])
            
            # Otherwise, trace left point of robot triangle
            else:
                master.after(750, draw_line(canvas, current_vert[0], current_vert[1],
                                            next_vert[0], next_vert[1], fill="red"))
                
                line_list.append([(current_vert[0], current_vert[1]),
                                  (next_vert[0], next_vert[1])])
        
        master_list.append(line_list)
    
    return master_list


def new_path(start, end, obstacle_list):
    open_list = []
    closed_list = []
    
    open_list.append(start)
    
    while len(open_list) > 0:
        lowest_node = open_list[0]
        lowest_index = 0
        for index, node in enumerate(open_list):
            if node.f < lowest_node.f:
                lowest_node = node
                lowest_index = index
        
        open_list.pop(lowest_index)
        closed_list.append(lowest_node)

        # If robot can move to destination, go there and end the path
        dest_visible = True
        for line_list in obstacle_list:
            for line in line_list:
                if check_intercept(lowest_node, end,
                                   Node(line[0][0], line[0][1], None), Node(line[1][0], line[1][1], None)):
                    dest_visible = False
                    break

        if dest_visible:
            result_path = [end]
            current_node = lowest_node
            while current_node is not None:
                result_path.append(current_node)
                current_node = current_node.parent
            return result_path[::-1]
        
        current_point = lowest_node
        
        visible_verts = []
        for line_list in obstacle_list:
            for line in line_list:
                node_visible = True
                move_point = Node(line[0][0], line[0][1], None)
                move_line = current_point, move_point
                
                # Check path to vertex against all other obstacle lines
                for check_line in [line for sublist in obstacle_list for line in sublist]:
                    if check_intercept(current_point, move_point, Node(check_line[0][0], check_line[0][1], None),
                                       Node(check_line[1][0], check_line[1][1], None)):
                        node_visible = False
                        break
                
                # If no lines intersect then the vertex is visible
                if node_visible and not check_inside(move_line, line_list):
                    visible_verts.append(Node(move_point.posX, move_point.posY, current_point))
        
        for vertex in visible_verts:
            if vertex in closed_list:
                continue
            
            vertex.f, vertex.g = get_f(current_point, vertex, end)
            
            skip = False
            for open_vertex in open_list:
                if vertex == open_vertex and vertex.g > open_vertex.g:
                    skip = True
                    break
            if skip:
                continue
            
            open_list.append(vertex)


# Check if a line is inside an obstacle
def check_inside(move_line, line_list):
    # Calculate mid point
    mid_point = ((move_line[0].posX + move_line[1].posX) / 2,
                 (move_line[0].posY + move_line[1].posY) / 2)
    
    # Get ordered list of vertexes
    start_vert = line_list[0][0]
    next_vert = line_list[0][1]
    vert_list = [start_vert]
    
    while len(vert_list) <= len(line_list):
        for line in line_list:
            if line[0] == next_vert:
                vert_list.append(line[0])
                next_vert = line[1]
                break
    
    # Denote lines between vertices
    codes = [path.Path.LINETO for _ in range(len(vert_list))]
    codes[0] = path.Path.MOVETO
    codes[len(codes) - 1] = path.Path.CLOSEPOLY
    
    # Make virtual obstacle from ordered vertices
    obstacle_plot_path = path.Path(np.array(vert_list), codes)
    
    # Check that the point is not inside an obstacle or on an obstacle's edge
    if obstacle_plot_path.contains_point(mid_point) \
            and not point_on_line(mid_point, line_list):
        return True
    else:
        return False


# Return the distance between two points
def get_distance(pointA, pointB):
    return sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)


# Check if a point falls on a virtual obstacle's line
def point_on_line(point, line_list):
    for line in line_list:
        if get_distance(line[0], point) + get_distance(point, line[1]) == get_distance(line[0], line[1]):
            return True
    return False


# Calculate f value using Pythagorean's Theorem
def get_f(start, vertex, end):
    new_g = ((start.posX - vertex.posX) ** 2) + ((start.posY - vertex.posY) ** 2) + start.g
    new_h = ((vertex.posX - end.posX) ** 2) + ((vertex.posY - end.posY) ** 2)
    f = new_g + new_h
    return f, new_g


# Check if two lines intersect
def check_intercept(start1, end1, start2, end2):
    # If start or end points are the same, ignore intersection
    if start1 in [start2, end2] or end1 in [start2, end2]:
        return False
    
    aX = end1.posX - start1.posX
    aY = end1.posY - start1.posY
    
    bX = start2.posX - end2.posX
    bY = start2.posY - end2.posY
    
    dX = start2.posX - start1.posX
    dY = start2.posY - start1.posY
    
    det = aX * bY - aY * bX
    
    if det == 0:
        return False
    
    r = (dX * bY - dY * bX) / det
    s = (aX * dY - aY * dX) / det
    
    return not (r < 0 or r > 1 or s < 0 or s > 1)


def draw_line(canvas, aX, aY, bX, bY, fill):
    canvas.create_line(aX, aY, bX, bY, fill=fill)
    canvas.update()


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
    master.geometry("750x750")
    canvas = Canvas(master, width=750, height=750)
    
    # Draw robot triangle
    robot_leftX = randint(50, 700)
    robot_leftY = randint(50, 200)
    canvas.pack()
    robot_lines = draw_robot(canvas, robot_leftX, robot_leftY)
    
    # Destination
    destX = randint(50, 700)
    destY = randint(550, 700)
    rightX = destX + 50
    rightY = destY
    topX = destX + 25
    topY = destY - 25
    
    # Draw and return new lines
    canvas.create_line(topX, topY, rightX, rightY, fill="green")
    canvas.create_line(rightX, rightY, destX, destY, fill="green")
    canvas.create_line(topX, topY, destX, destY, fill="green")
    
    # Store all obstacle's vertices in a list
    obstacle_list = []
    
    # Create random obstacles
    num_obstacles = randint(3, 5)  # Get a random number of obstacles
    for _ in range(num_obstacles):
        obstacle_type = randint(3, 5)  # Get a random type of obstacle
        obstacleX = randint(150, 600)  # Get a random starting X position
        obstacleY = randint(150, 600)  # Get a random starting y position
        scale = uniform(0.3, 1)
        
        if obstacle_type == 3:
            obstacle_list.append(draw_3_sided(canvas, obstacleX, obstacleY, scale))
        elif obstacle_type == 4:
            obstacle_list.append(draw_4_sided(canvas, obstacleX, obstacleY, scale))
        elif obstacle_type == 5:
            obstacle_list.append(draw_5_sided(canvas, obstacleX, obstacleY, scale))
    
    obstacle_line_list = make_virtual_obstacles(obstacle_list, canvas, master)
    
    return_path = new_path(start=Node(robot_leftX, robot_leftY, None), end=Node(destX, destY, None),
                           obstacle_list=obstacle_line_list)
    
    # Draw path to destination
    for index, vertex in enumerate(return_path):
        if index == len(return_path) - 1:
            break
        
        next_vertex = return_path[index + 1]
        robot_lines = draw_robot(canvas, next_vertex.posX, next_vertex.posY, robot_lines)
        master.after(1000, draw_line(canvas, vertex.posX, vertex.posY, next_vertex.posX, next_vertex.posY, "green"))
    
    master.mainloop()


main()
