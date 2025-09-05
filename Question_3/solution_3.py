import turtle
from PIL import Image

def fractal_edge(length, level):
    """
    Recursive function to draw one side of the fractal.
    If level = 0 → just draw a straight line.
    If level > 0 → split the line into 4 smaller parts with a inward bump in the middle.
    """
    if level == 0:
        turtle.forward(length)
    else:
        length /= 3.0  # divide edge into 3 equal parts

        # First part (straight)
        fractal_edge(length, level - 1)

        # Make the triangular "bump"
        turtle.right(60)
        fractal_edge(length, level - 1)

        turtle.left(120)
        fractal_edge(length, level - 1)

        # Back to original direction
        turtle.right(60)
        fractal_edge(length, level - 1)


def fractal_polygon(sides, length, level):
    """
    Draws a polygon where each side is replaced by a fractal edge.
    Example: sides=3 → triangle snowflake.
    """
    angle = 360 / sides
    for _ in range(sides):
        fractal_edge(length, level)
        turtle.right(angle)


def main():
    # Ask the user for details
    sides = int(input("Number of sides for polygon: "))
    length = float(input("Side length in pixels: "))
    level = int(input("Recursion depth (Number of times to apply the pattern rules): "))

    # Setup turtle speed and screen
    turtle.speed(0)        # fastest drawing
    turtle.hideturtle()    # hide the cursor
    turtle.title("Fractal Polygon Pattern")

    # Move turtle so drawing is more centered
    turtle.penup()
    turtle.setheading(0)
    turtle.goto(-length/2, length/4)
    turtle.pendown()
        
    # Draw the fractal polygon
    fractal_polygon(sides, length, level)
    
    #The window will stay open until the user closes it

    # --- SAVE RESULT TO PNG ---
    canvas = turtle.getcanvas()
    canvas.postscript(file="Question_3/result.eps")   # save EPS first
    img = Image.open("result.eps")        # open EPS
    img.save("Question_3/result.png")                # save as PNG
    print("Fractal saved as result.png")
    

    turtle.done()


if __name__ == "__main__":
    main()
