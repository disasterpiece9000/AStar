from tkinter import Canvas, messagebox, Tk
from fractions import Fraction


# Redraw the robot using the top point
def draw_robot(topX, topY, old_lines=None):
    # Calculate left and right points
    leftX = topX - 50
    leftY = topY + 50
    rightX = topX + 50
    rightY = topY + 50
    
    # Delete old lines if they exist
    if old_lines is not None:
        for line in old_lines:
            canvas.delete(line)
    
    # Draw and return new lines
    return [canvas.create_line(topX, topY, rightX, rightY),
            canvas.create_line(rightX, rightY, leftX, leftY),
            canvas.create_line(leftX, leftY, topX, topY)]


def draw_4_sided(startX, startY):
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


def draw_virtual_obstacles(obstacle_list):
    for vert_list in obstacle_list:
        for index, current_vert in enumerate(vert_list):
            # If you are at the last vertex then use first vertex
            if index == len(vert_list) - 1:
                next_vert = vert_list[0]
            else:
                next_vert = vert_list[index + 1]
                
            slope = Fraction(current_vert[1] - next_vert[1], current_vert[0] - next_vert[0])
            rise = slope.numerator
            run = slope.denominator
            
            if run > 0 and rise == 0 and current_vert[0] - next_vert[0] > 0:
                canvas.create_line(current_vert[0] - 50, current_vert[1] + 50,
                                   next_vert[0] - 50, next_vert[1] + 50, fill="blue")
                
                canvas.create_line(current_vert[0], current_vert[1],
                                   current_vert[0] - 50, current_vert[1] + 50, fill="red")
                
                canvas.create_line(next_vert[0] - 50, next_vert[1] + 50, next_vert[0] - 100, next_vert[1], fill="red")

            elif (run < 0 and rise < 0) or (run > 0 and rise < 0):
                canvas.create_line(current_vert[0] - 100, current_vert[1],
                                   next_vert[0] - 100, next_vert[1], fill="blue")
                
                canvas.create_line(current_vert[0], current_vert[1], current_vert[0] - 100, current_vert[1], fill="red")
                canvas.create_line(next_vert[0], next_vert[1], next_vert[0] - 100, next_vert[1], fill="red")
            else:
                canvas.create_line(current_vert[0], current_vert[1], next_vert[0], next_vert[1], fill="blue")
            

# Create a Canvas in a 750x750 window
master = Tk()
master.geometry("750x750")
canvas = Canvas(master, width=750, height=750)

# Draw robot triangle
robot_topX = 75
robot_topY = 0
canvas.pack()
draw_robot(robot_topX, robot_topY)

# Store all obstacle's vertices in a list
obstacle_list = []

# Draw obstacle
obstacle_list.append(draw_4_sided(200, 200))

draw_virtual_obstacles(obstacle_list)

# Create a 750x750 array to store virtual objects
#maze = [[0 for _ in range(750)] for _ in range(750)]

master.mainloop()
