import turtle

def draw_edge(length, depth):
    """
    Recursively draw one edge of the fractal polygon.
    Each edge is divided into 4 smaller edges with an inward 'bump'.
    """
    if depth == 0:
        turtle.forward(length)  # Base case: draw straight line
    else:
        length /= 3.0  # Each new segment is 1/3 the original length

        # 1st segment
        draw_edge(length, depth - 1)

        # 2nd segment: turn right 60° to make the first side of the bump
        turtle.right(60)
        draw_edge(length, depth - 1)

        # 3rd segment: turn left 120° to draw the middle side of the bump
        turtle.left(120)
        draw_edge(length, depth - 1)

        # 4th segment: turn right 60° back to the original direction
        turtle.right(60)
        draw_edge(length, depth - 1)

def draw_polygon(sides, length, depth):
    """
    Draws the full fractal polygon shape.
    Goes around 'sides' times, applying recursion to each edge.
    """
    angle = 360 / sides  # Exterior angle of the polygon
    for _ in range(sides):
        draw_edge(length, depth)  # Draw fractal edge
        turtle.right(angle)       # Turn to the next side

def main():
    # Get user input for polygon properties
    sides = int(input("Enter the number of sides: "))
    length = float(input("Enter the side length (pixels): "))
    depth = int(input("Enter the recursion depth: "))

    # Setup turtle graphics
    turtle.speed(0)         # Fastest drawing speed
    turtle.hideturtle()     # Hide the arrow cursor
    turtle.title("Recursive Polygon Fractal (Inward Facing)")

    # Move turtle to a starting position
    turtle.penup()
    turtle.goto(-length/2, length/3)  # Roughly center the drawing
    turtle.pendown()

    # Draw the fractal polygon
    draw_polygon(sides, length, depth)

    # Keep the window open until closed by user
    turtle.done()

if __name__ == "__main__":
    main()
