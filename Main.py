from tkinter import Canvas, messagebox, Tk
from fractions import Fraction


# TODO: Make a method to check if a line intercepts an object
# TODO: Check if destination is already accessible
# TODO: If dest is not accessible, check which virtual obstacle vertices can be moved to from the starting position
# TODO: Move to the vertex with the lowest g value
# TODO: Keep searching for next vertex with lowest g until dest is accessible



# Redraw the robot using the top point
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
    return [canvas.create_line(topX, topY, rightX, rightY),
            canvas.create_line(rightX, rightY, leftX, leftY),
            canvas.create_line(leftX, leftY, topX, topY)]


def draw_5_sided(canvas, startX, startY):
    top_rightX = startX + 100
    top_rightY = startY + 50
    bottom_rightX = startX + 100
    bottom_rightY = startY + 100
    bottom_leftX = startX - 100
    bottom_leftY = startY + 100
    top_leftX = startX - 100
    top_leftY = startY + 50

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
    top_rightX = startX + 100
    top_rightY = startY
    bottom_rightX = startX + 150
    bottom_rightY = startY + 100
    bottom_leftX = startX - 50
    bottom_leftY = startY + 100

    # Draw obstacle
    canvas.create_line(startX, startY, top_rightX, top_rightY)
    canvas.create_line(top_rightX, top_rightY, bottom_rightX, bottom_rightY)
    canvas.create_line(bottom_rightX, bottom_rightY, bottom_leftX, bottom_rightY)
    canvas.create_line(bottom_leftX, bottom_leftY, startX, startY)

    # Return vertices
    return [(startX, startY), (top_rightX, top_rightY), (bottom_rightX, bottom_rightY), (bottom_leftX, bottom_leftY)]


def draw_3_sided(canvas, startX, startY):
    leftX = startX - 100
    leftY = startY + 100
    rightX = startX + 100
    rightY = startY + 100

    canvas.create_line(startX, startY, rightX, rightY)
    canvas.create_line(rightX, rightY, leftX, leftY)
    canvas.create_line(leftX, leftY, startX, startY)

    return [(startX, startY), (rightX, rightY), (leftX, leftY)]


def get_slope(startX, startY, endX, endY):
    rise = None
    run = None

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


def make_virtual_obstacles(maze, obstacle_list, canvas):
    line_list = []

    for vert_list in obstacle_list:
        for enum_index, current_vert in enumerate(vert_list):

            # If you are at the last vertex then wrap around to first vertex
            if enum_index == len(vert_list) - 1:
                next_vert = vert_list[0]
            else:
                next_vert = vert_list[enum_index + 1]

            rise, run = get_slope(current_vert[0], current_vert[1], next_vert[0], next_vert[1])

            # Trace right point of robot triangle
            if rise < 0 and run == 0:
                canvas.create_line(current_vert[0] - 50, current_vert[1],
                                   next_vert[0] - 50, next_vert[1], fill="red")

                line_list.append([(current_vert[0] - 50, current_vert[1]),
                                           (next_vert[0] - 50, next_vert[1])])

            # Trace right point of robot triangle
            elif rise < 0 < run:
                canvas.create_line(current_vert[0] - 50, current_vert[1],
                                   next_vert[0] - 50, next_vert[1], fill="red")

                line_list.append([(current_vert[0] - 50, current_vert[1]),
                                           (next_vert[0] - 50, next_vert[1])])

                canvas.create_line(next_vert[0], next_vert[1],
                                   next_vert[0] - 50, next_vert[1], fill="red")

                line_list.append([(next_vert[0], next_vert[1]),
                                           (next_vert[0] - 50, next_vert[1])])

            # Trace top point of robot triangle
            elif rise == 0 and run < 0:
                canvas.create_line(current_vert[0] - 25, current_vert[1] + 25,
                                   next_vert[0] - 25, next_vert[1] + 25, fill="blue")

                line_list.append([(current_vert[0] - 25, current_vert[1] + 25),
                                           (next_vert[0] - 25, next_vert[1] + 25)])

                canvas.create_line(current_vert[0], current_vert[1],
                                   current_vert[0] - 25, current_vert[1] + 25, fill="blue")

                line_list.append([(current_vert[0], current_vert[1]),
                                           (current_vert[0] - 25, current_vert[1] + 25)])

                canvas.create_line(next_vert[0] - 25, next_vert[1] + 25,
                                   next_vert[0] - 50, next_vert[1], fill="blue")

                line_list.append([(next_vert[0] - 25, next_vert[1] + 25),
                                           (next_vert[0] - 50, next_vert[1])])

            # Otherwise, trace left point of robot triangle
            else:
                canvas.create_line(current_vert[0], current_vert[1],
                                   next_vert[0], next_vert[1], fill="green")

                line_list.append([(current_vert[0], current_vert[1]),
                                           (next_vert[0], next_vert[1])])

    return line_list


def find_path(current_point, path, start, end, line_list, g):

    # Check if robot can move to destination immediately
    dest_visible = True
    for line in line_list:
        if check_intercept(current_point, end, line[0], line[1]):
            dest_visible = False
            break

    if dest_visible:
        path.append(end)
        return path

    # Find all visible nodes
    visible_verts = []
    for move_line in line_list:
        node_visible = True
        move_point = move_line[0]

        # Check path to vertex against all other obstacle lines
        for check_line in line_list:
            if check_intercept(current_point, move_point, check_line[0], check_line[1]):
                node_visible = False
                break

        # If no lines intersect then the vertex is visible
        if node_visible:
            visible_verts.append(move_line[0])

    # Find the vertex with the lowest F value
    next_move = visible_verts[0]
    min_f = get_f(current_point, visible_verts[0], end, g)[0]

    for vertex in visible_verts:
        f, g = get_f(current_point, vertex, end, g)
        if f < min_f:
            next_move = vertex
            min_f = f

    path.append(next_move)
    return find_path(next_move, path, start, end, line_list, g)


def get_f(start, vertex, end, g):
    g = ((start[0] - vertex[0]) ** 2) + ((start[1] - vertex[1]) ** 2) + g
    h = ((vertex[0] - end[0]) ** 2) + ((vertex[1] - end[1]) ** 2)
    return g + h, g


def check_intercept(start1, end1, start2, end2):

    # If start or end points are the same, ignore intersection
    if start1 in [start2, end2] or end1 in [start2, end2]:
        return False

    aX = end1[0] - start1[0]
    aY = end1[1] - start1[1]

    bX = start2[0] - end2[0]
    bY = start2[1] - end2[1]

    dX = start2[0] - start1[0]
    dY = start2[1] - start1[1]

    det = aX * bY - aY * bX

    if det == 0:
        return False

    r = (dX * bY - dY * bX) / det
    s = (aX * dY - aY * dX) / det

    return not (r < 0 or r > 1 or s < 0 or s > 1)


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

    # Create a 750x750 array to store virtual objects
    maze = [[0 for _ in range(750)] for _ in range(750)]

    # Draw robot triangle
    robot_leftX = 230
    robot_leftY = 230
    canvas.pack()
    draw_robot(canvas, robot_leftX, robot_leftY)

    # Destination
    destX = 550
    destY = 550
    rightX = destX + 50
    rightY = destY
    topX = destX + 25
    topY = destY - 25

    # Draw and return new lines
    canvas.create_line(topX, topY, rightX, rightY)
    canvas.create_line(rightX, rightY, destX, destY)
    canvas.create_line(topX, topY, destX, destY)

    # Store all obstacle's vertices in a list
    obstacle_list = []

    # Draw obstacle
    obstacle_list.append(draw_3_sided(canvas, 350, 250))

    obstacle_line_list = make_virtual_obstacles(maze, obstacle_list, canvas)

    path = find_path(current_point=(robot_leftX, robot_leftY), path=[(robot_leftX, robot_leftY)],
                     start=(robot_leftX, robot_leftY), end=(destX, destY),
                     line_list=obstacle_line_list, g=0)

    for index, vertex in enumerate(path):
        if index == len(path) - 1:
            break

        next_vertex = path[index + 1]
        canvas.create_line(vertex[0], vertex[1], next_vertex[0], next_vertex[1])


    master.mainloop()


main()
