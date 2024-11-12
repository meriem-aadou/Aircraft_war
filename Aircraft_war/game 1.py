#MERIEM OUELD AADOU

############################################################################################
import pgzrun
import random
import time

WIDTH = 480
HEIGHT = 700
TITLE = 'Aircraft war'

# Background actors
background1 = Actor('background')
background1.x = WIDTH / 2
background1.y = 852 / 2
background2 = Actor('background')
background2.x = WIDTH / 2
background2.y = -852 / 2

# Player and enemy actors
hero = Actor('hero')
hero.x = WIDTH / 2
hero.y = HEIGHT * 2 / 3
enemy = Actor('enemy')
enemy.x = WIDTH / 2
enemy.y = 0

# Button for starting the game
start_button = Actor('start_no')
start_button.x = WIDTH / 2
start_button.y = HEIGHT / 2

# Sound and gameplay variables
score = 0
isLoose = False
isPlaying = False
bullets = []  # List to track all bullets on screen
sounds.game_music.play(-1)

# Shooting controls
isShooting = False
last_shot_time = 0
shoot_interval = 0.2  # Interval in seconds between each shot



def draw():
    background1.draw()
    background2.draw()

    if not isPlaying:
        start_button.draw()  # Draw the start button
    else:
        hero.draw()
        enemy.draw()

        #draw bullets
        for bullet in bullets:
            bullet.draw()

        # Draw score
        screen.draw.text("Score: " + str(score), (200, HEIGHT - 50),
                         fontsize=30, color='black')

        # Draw game over message if lost
        if isLoose:
            screen.draw.text("Game Over!", (50, HEIGHT / 2),
                             fontsize=90, color='red')


# Update function
def update():
    global score, isLoose, last_shot_time

    if not isPlaying or isLoose:
        return

    # Background scrolling
    if background1.y > 852 / 2 + 852:
        background1.y = -852 / 2
    if background2.y > 852 / 2 + 852:
        background2.y = -852 / 2
    background1.y += 1
    background2.y += 1

    # Bullet movement and removal
    for bullet in bullets[:]:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)  # Remove bullet if it goes off-screen

    # Enemy movement and reset when off-screen
    enemy.y += 4
    if enemy.y > HEIGHT:
        enemy.y = 0
        enemy.x = random.randint(50, WIDTH - 50)

    # Keep the enemy within the screen boundaries horizontally
    if enemy.x < 0:
        enemy.x = 0
    elif enemy.x > WIDTH:
        enemy.x = WIDTH

    # Bullet-enemy collision
    for bullet in bullets:
        if bullet.colliderect(enemy):
            sounds.got_enemy.play()
            enemy.y = 0
            enemy.x = random.randint(0, WIDTH)
            score += 1
            bullets.remove(bullet)  # Remove bullet upon hitting the enemy
            break

    # Hero-enemy collision
    if hero.colliderect(enemy):
        sounds.explode.play()
        isLoose = True
        hero.image = 'hero_blowup'

    # Continuous shooting
    if isShooting and time.time() - last_shot_time > shoot_interval:
        fire_bullet()
        last_shot_time = time.time()


# Function to start the game
def on_mouse_down(pos):
    global isPlaying
    if start_button.collidepoint(pos) and not isPlaying:
        isPlaying = True
    else:
        global isShooting
        isShooting = True


def on_mouse_up():
    global isShooting
    isShooting = False


# Mouse control functions
def on_mouse_move(pos):
    global isLoose
    if isLoose:
        return
    if start_button.collidepoint(pos):
        start_button.image = 'start_yes'
    else:
        start_button.image = 'start_no'

    if isPlaying:
        hero.x = max(0, min(pos[0], WIDTH))
        hero.y = max(0, min(pos[1], HEIGHT))


# Fire bullet function
def fire_bullet():
    sounds.gun.play()
    new_bullet = Actor('bullet')
    new_bullet.x = hero.x
    new_bullet.y = hero.y - 70
    bullets.append(new_bullet)


pgzrun.go()
