import turtle
import math
import random

# cardinal variables
speed = 20
enemy_speed = 1
number_of_enemies = 2
missile_speed = 20
speed_increase_threshold = 5
earth_health = 5
ship_health = 3
total_missiles = 3

# the screen:
wn = turtle.Screen()
wn.screensize(800, 650)
wn.bgcolor("black")
wn.title("Space Impact")
wn.bgpic("images\\background.gif")

# Register the shapes
turtle.register_shape("images\\player.gif")
turtle.register_shape("images\\enemy1.gif")

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.setposition(-300, -300)
pen.pensize(3)
pen.pendown()
for side in range(4):
    pen.fd(600)
    pen.lt(90)
pen.hideturtle()

player = turtle.Turtle()
player.color("blue")
player.shape("images\\player.gif")
player.penup()
player.speed(0)
player.setposition(-250, -0)

# score variable
score = 0

# score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(400, 200)
score_final = "Score: %s" % score
score_pen.write(score_final, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# locomotion
# speed = 20

# enemy_speed = 1;

# number of enemies
# number_of_enemies = 2
# list for enemies
enemies = []

# Add enemies to list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

# the Enemy!
for enemy in enemies:
    enemy.color("red")
    enemy.shape("images\\enemy1.gif")
    enemy.penup()
    enemy.speed(0)
    y = random.randint(-280, 281)
    enemy.setposition(250, y)


def random_enemy_position():
    return random.randint(-280, 281)


def move_down():
    y = player.ycor()
    y -= speed
    if y <= -280:
        y = 280
    player.sety(y)


def move_up():
    y = player.ycor()
    y += speed
    if y >= 280:
        y = -280
    player.sety(y)


# player's missiles
missiles = []
states = []
for i in range(total_missiles):
    missiles.append(turtle.Turtle())
    states.append("ready")

for missile in missiles:
    missile = turtle.Turtle()
    missile.color("yellow")
    missile.penup()
    missile.speed(0)
    missile.shapesize(0.6, 0.6)
    missile.hideturtle()
    missile.setposition(-400, -400)

# missile_speed = 20

# missile states
# ready state : ready to fire
# fire : missile is fired

cm = 3


# short for current_missiles

# functions for bullets
def fire_missile():
    # declared missile_state as global
    global cm
    if cm > 0:
        global states
        n = len(states) - 1 - states[::-1].index("ready")
        if states[n] == "ready" :
            cm -= 1
            states[n] = "fired"
            missile = missiles[n]
            x = player.xcor()
            y = player.ycor()
            missile.setposition(x + 20, y)
            missile.showturtle()


# collision detection
def isCollision(t1, t2, dist):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < dist:
        return True
    return False


# health display
# Health heading
head = turtle.Turtle()
head.speed(0)
head.color("white")
head.penup()
head.setposition(-490, 120)
head_string = "Your Health: "
head.write(head_string, False, align="left", font=("Arial", 14, "normal"))
head.hideturtle()
# player health
shield = []
for i in range(ship_health):
    shield.append(turtle.Turtle())

pos = -480
for shard in shield:
    shard.lt(90)
    shard.shape("triangle")
    shard.setposition(pos, 100)
    shard.penup()
    shard.speed(0)
    if pos == -480:
        shard.color("red")
    elif pos == -450:
        shard.color("yellow")
    elif pos == -420:
        shard.color("green")
    pos += 30

# planet health heading
foot = turtle.Turtle()
foot.speed(0)
foot.color("white")
foot.penup()
foot.setposition(-490, 30)
foot_string = "Earth's Health: "
foot.write(foot_string, False, align="left", font=("Arial", 14, "normal"))
foot.hideturtle()
# planet health
earth = []
for i in range(earth_health):
    earth.append(turtle.Turtle())

pos = -490
for e in earth:
    e.lt(90)
    e.shape("triangle")
    e.setposition(pos, 0)
    e.penup()
    e.speed(0)
    if pos == -490:
        e.color("red")
    elif pos == -460:
        e.color("orange")
    elif pos == -430:
        e.color("yellow")
    elif pos == -400:
        e.color("blue")
    elif pos == -370:
        e.color("green")
    pos += 30


# update health display
def remove_player_health(h):
    sh = shield[len(shield) - h - 1]
    sh.hideturtle()


def remove_earth_health(h):
    sh = earth[len(earth) - h - 1]
    sh.hideturtle()


# quit game
def quit_game():
    wn.bye()
    print("Done")
    print("Your score was ", score)


turtle.listen()
turtle.onkeypress(move_down, "Down")
turtle.onkeypress(move_up, "Up")
turtle.onkeypress(fire_missile, "space")
turtle.onkeypress(quit_game, "q")

takeout = 0
health = 0
# main loop
while True:
    for enemy in enemies:
        # Moving enemy
        x = enemy.xcor()
        x -= enemy_speed
        enemy.setx(x)

        if enemy.xcor() <= -280:
            enemy.setposition(250, 40)
            remove_earth_health(takeout)
            takeout += 1

        for missile in missiles:
            i = 0
            # collision between missile and enemy
            if isCollision(missile, enemy, 15):
                missile.hideturtle()
                states[i] = "ready"
                cm += 1
                missile.setposition(-400, -400)
                # reset the enemy
                enemy.setposition(250, random_enemy_position())
                score += 1
                score_final = "Score: %s" % score
                score_pen.clear()
                score_pen.write(score_final, False, align="left", font=("Arial", 14, "normal"))
                if score % speed_increase_threshold == 0:
                    enemy_speed += 1
            i += 1

        if isCollision(player, enemy, 25):
            enemy.setposition(250, random_enemy_position())
            remove_player_health(health)
            health += 1
            # print(health)

    if (health > ship_health) or (takeout > earth_health):
        print(health)
        break

    for missile in missiles:
        i = 0
        if states[i] == "fired":
            # move missile
            x = missile.xcor()
            x += missile_speed
            missile.setx(x)

        # resetting missile
        if missile.xcor() > 280:
            states[i] = "ready"
            cm += 1
            missile.hideturtle()
        i += 1

wn.bye()

print("Done!!")
print("Your score was ", score)
