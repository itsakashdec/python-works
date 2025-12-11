# simple_breakout.py
# Very simple Breakout clone (slower ball, faster paddle)

import turtle
import random

# Screen
wn = turtle.Screen()
wn.title("Simple Breakout")
wn.bgcolor("black")
wn.setup(600, 600)
wn.tracer(0)

# Score / lives
score = 0
lives = 3

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(-280, 260)
pen.write(f"Score: {score}  Lives: {lives}", font=("Arial", 14, "normal"))

# Paddle (wider and moves faster)
paddle = turtle.Turtle()
paddle.shape("square")
paddle.shapesize(stretch_wid=1, stretch_len=8)   # wide paddle
paddle.color("white")
paddle.penup()
paddle.goto(0, -230)
PADDLE_MOVE = 60

def left():
    x = paddle.xcor() - PADDLE_MOVE
    if x < -260: x = -260
    paddle.setx(x)

def right():
    x = paddle.xcor() + PADDLE_MOVE
    if x > 260: x = 260
    paddle.setx(x)

wn.listen()
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")

# Ball (slower)
ball = turtle.Turtle()
ball.shape("circle")
ball.color("yellow")
ball.penup()
ball.goto(0, -150)
ball.dx = 2 * random.choice([1, -1])   # slower x
ball.dy = 2                             # slower y

# Simple bricks: 3 rows x 5 cols
bricks = []
colors = ["red", "orange", "green"]
start_x = -200
start_y = 180
for r in range(3):
    for c in range(5):
        b = turtle.Turtle()
        b.shape("square")
        b.shapesize(stretch_wid=1, stretch_len=4)
        b.color(colors[r])
        b.penup()
        b.goto(start_x + c*100, start_y - r*30)
        bricks.append(b)

def update_score():
    pen.clear()
    pen.goto(-280, 260)
    pen.write(f"Score: {score}  Lives: {lives}", font=("Arial", 14, "normal"))

game_over = False

while True:
    wn.update()

    if game_over:
        continue

    # move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # wall bounce
    if ball.xcor() > 290:
        ball.setx(290)
        ball.dx *= -1
    if ball.xcor() < -290:
        ball.setx(-290)
        ball.dx *= -1
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    # paddle collision (very simple rectangle check)
    if (ball.ycor() < paddle.ycor() + 10 and ball.ycor() > paddle.ycor() - 10 and
        abs(ball.xcor() - paddle.xcor()) < 80 and ball.dy < 0):
        ball.dy *= -1

    # bricks collision simple loop
    for b in bricks:
        if b.isvisible() and abs(ball.xcor() - b.xcor()) < 40 and abs(ball.ycor() - b.ycor()) < 15:
            b.hideturtle()
            ball.dy *= -1
            score += 10
            update_score()
            break

    # bottom - lose life
    if ball.ycor() < -300:
        lives -= 1
        update_score()
        if lives == 0:
            pen.goto(0, 0)
            pen.write("GAME OVER", align="center", font=("Arial", 30, "bold"))
            game_over = True
            ball.hideturtle()
        else:
            # reset ball and paddle
            ball.goto(0, -150)
            ball.dx = 2 * random.choice([1, -1])
            ball.dy = 2
            paddle.goto(0, -230)

    # win?
    if all(not b.isvisible() for b in bricks):
        pen.goto(0, 0)
        pen.write("YOU WIN!", align="center", font=("Arial", 30, "bold"))
        game_over = True
        ball.hideturtle()
