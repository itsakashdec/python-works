# simple_breakout_fix.py
# Very simple Breakout clone — slower ball, timer-based loop (more playable)

import turtle
import random

# -------- Screen --------
wn = turtle.Screen()
wn.title("Simple Breakout (slower)")
wn.bgcolor("black")
wn.setup(600, 600)
wn.tracer(0)

# -------- Config (tweak these) --------
SPEED = 10     # multiply ball dx/dy by this (0.5 slower, 1.0 normal)
FRAME_MS = 20     # milliseconds per frame (20ms -> ~50 FPS). Increase to slow game.

# -------- Score / lives --------
score = 0
lives = 3

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(-280, 260)
pen.write(f"Score: {score}  Lives: {lives}", font=("Arial", 14, "normal"))

# -------- Paddle --------
paddle = turtle.Turtle()
paddle.shape("square")
paddle.shapesize(stretch_wid=1, stretch_len=8)
paddle.color("white")
paddle.penup()
paddle.goto(0, -230)
PADDLE_MOVE = 80   # bigger value -> faster per key press

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

# -------- Ball (slower floats) --------
ball = turtle.Turtle()
ball.shape("circle")
ball.color("yellow")
ball.penup()
ball.goto(0, -150)
# base velocities are small floats for smooth, slow motion
ball.dx = 0.9 * random.choice([1, -1])   # base x
ball.dy = 0.9                             # base y
# apply SPEED multiplier
ball.dx *= SPEED
ball.dy *= SPEED

# -------- Bricks: 3x5 --------
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

# -------- Game loop using ontimer (no busy while loop) --------
def game_loop():
    global score, lives, game_over

    if not game_over:
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

        # paddle collision
        if (ball.ycor() < paddle.ycor() + 12 and ball.ycor() > paddle.ycor() - 12 and
            abs(ball.xcor() - paddle.xcor()) < 80 and ball.dy < 0):
            # add slight horizontal change based on hit position for control
            hit_pos = (ball.xcor() - paddle.xcor()) / 80  # -1..1
            ball.dx = (0.9 + abs(hit_pos))*hit_pos  # adjust dx mildly
            ball.dy *= -1

        # brick collisions
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
                ball.goto(0, -150)
                ball.dx = 0.9 * random.choice([1, -1]) * SPEED
                ball.dy = 0.9 * SPEED
                paddle.goto(0, -230)

        # win?
        if all(not b.isvisible() for b in bricks):
            pen.goto(0, 0)
            pen.write("YOU WIN!", align="center", font=("Arial", 30, "bold"))
            game_over = True
            ball.hideturtle()

    wn.update()
    # schedule next frame
    wn.ontimer(game_loop, FRAME_MS)

# start loop
wn.ontimer(game_loop, FRAME_MS)
wn.mainloop()
