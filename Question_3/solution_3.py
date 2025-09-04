import turtle

def fractal_edge(length, level):
    """
    Recursive function to draw one edge of the fractal polygon.
    Each edge is split into 4 parts with an inward 'bump'.
    """
    if level == 0:
        turtle.forward(length)
    else:
        length /= 3.0

        # First part
        fractal_edge(length, level - 1)

        # Turn and draw bump inward
        turtle.right(60)
        fractal_edge(length, level - 1)

        turtle.left(120)
        fractal_edge(length, level - 1)

        # Return to original heading
        turtle.right(60)
        fractal_edge(length, level - 1)

def fractal_polygon(sides, length, level):
    """
    Draw the full polygon with fractal edges.
    """
    angle = 360 / sides
    for _ in range(sides):
        fractal_edge(length, level)
        turtle.right(angle)

def main():
    # User input (slightly different wording)
    sides = int(input("Number of sides for polygon: "))
    length = float(input("Side length (pixels): "))
    level = int(input("Recursion depth: "))

    # Setup
    turtle.speed(0)
    turtle.hideturtle()
    turtle.title("Fractal Polygon Pattern")

    # Start more centered
    turtle.penup()
    turtle.setheading(0)
    turtle.goto(-length/2, length/4)
    turtle.pendown()

    # Draw
    fractal_polygon(sides, length, level)

    turtle.done()

if __name__ == "__main__":
    main()
