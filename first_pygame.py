import pygame
import os  # 7 importing os, Operating System, will allow us to define the paths to the images we want to load and use
pygame.font.init()  # 21c pygame font library, we can i.e. use it for our health bar
pygame.mixer.init()  # 28 initializing sound library of pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # 3the window/main surface
pygame.display.set_caption("Space Kynis!")  # name caption for our game, will display at upper left window

WHITE = (255, 255, 255)  # 4RGB - Red, Green, Blue: this will create white
BLACK = (0, 0, 0)  # 12c color code for black
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)  # 12arguments passed to draw our border = x pos, y pos, width, height
# to find the middle for our x pos, we can divide width/2 and we can minus it by 5, since our width is hardcoded

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit_sound.wav'))  # 28c loading sounds
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)  # 21cc creating the font, and its size, that we want to use
WINNER_FONT = pygame.font.SysFont('comicsans', 150)  # 23 for our draw_winner function

FPS = 60  # helps you control how often the screen needs to refresh, so your machine doesn't overwork itself needlessly
VEL = 5  # 10 velocity, how fast anything set to this will be moving, i.e spaceship moves with -=5/+= 5 to sides/up/down
BULLETS_VEL = 10  # 13c creating bullet speed - the velocity the rectangles will be moving on screen
BULLET_AMOUNT = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  # 8c we pass in these variables, rather than raw numbers in proper places

YELLOW_COLLISION = pygame.USEREVENT + 1  # 17 we create an event for everytime a collision happens, i.e. hit by bullet
RED_COLLISION = pygame.USEREVENT + 2  # 17 each event needs a unique event id, so we can separate by i.e. 1 and 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))  # 7cwe path to the images
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  # 8 resizing spaceships and giving new dimensions
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))  # 7cc and load the images
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)  # 8c rotating the images

SPACE_BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))  # 19 loading the background and resizing->
# it, we pass in our WIDTH and HEIGHT, but could be other dimension also, if we desired so


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):  # 5functions for drawing/coloring
    WIN.blit(SPACE_BACKGROUND, (0, 0))  # 19cwe drawing the background, 0, 0 is pos we want to start the background from
#   WIN.fill(WHITE)  # 4c fills out the screen with colour of choice from the RGB range - fill screen before drawing
    pygame.draw.rect(WIN, BLACK, BORDER)  # 12cc .rect takes a rectangle, draws it on a WIN(surface), color, rectangle
    red_health_text = HEALTH_FONT.render('HP: ' + str(red_health), 1, WHITE)  # 21ccc health font, string, we convert
# red_health(10) into a string, 1=is aliasing and must always be 1, pass in the color of the red_health_text WHITE to
    yellow_health_text = HEALTH_FONT.render('HP: ' + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))  # 22 we draw it on the screen, what we->
# are blitting and where - at WIDTH minus the width of the red text(get_width) minus 10 pixels, at 10 on the y pos
    WIN.blit(yellow_health_text, (10, 10))  # 22 we blit it at pos 10 on x and 10 on y

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # 9ccc we replace the earlier predefined position, with x and y
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  # 7ccc we pass in the positions into "blit", we load spaceship, not the img

    for bullet in yellow_bullets:  # 18 we draw the bullets, and pass them into our draw_window function
        pygame.draw.rect(WIN, YELLOW, bullet)  # 18c draw rectangle, on the WINDOW in the color YELLOW and it's a BULLET

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)  # 18 must be passed in main function also, since we call this function there

    pygame.display.update()  # 4cc updates the display, and fills it with whatever we've input for it to show


def yellow_handle_movement(keys_pressed, yellow):  # 11 define new function, takes arguments "keys_pressed" and "yellow"
    if keys_pressed[pygame.K_a] and yellow.x - VEL + 5 > 0:  # left - "and" prevents us from moving less than 0 on x pos
        yellow.x -= VEL  # when pressing the "a" key, yellow rectangle will move VEL (5) on the x axis (left)
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15:  # right - VEL + yellow.width pos ->
        yellow.x += VEL  # should be less than the borders x position, we can +15 on border.x or -15 from yellow.width
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL  # 5, 15 and 15 on yellow.x and yellow.y are hardcoded to allow better/closer movement to border
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 15 < HEIGHT:  # down - makes sure the height of ->
        yellow.y += VEL  # our yellow.height is less than the screen height, and won't allow it to pass its height


def red_handle_movement(keys_pressed, red):  # 11 define new function, takes arguments "keys_pressed" and "red"
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left - when pressing left, reds x pos->
        red.x -= VEL  # subtracting VEL (speed), must be greater than the x pos of BORDER and x pos of borders width
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 20:  # right - red x pos must be less than ->
        red.x += VEL  # screen WIDTH, +20 added pixels to allow move reds rectangle closer
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # down - yellow down and red down are ->
        red.y += VEL  # both appropriate ways of allowing extra added pixels - makes same result


def handle_bullets(yellow_bullets, red_bullets, yellow, red):  # 16 handles collision, bullets on/off screen and chars
    for bullet in yellow_bullets:  # 16c making bullets move, from left to right by using += bullets vel
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):  # 16cc checks to see, if yellow char has collided with what we pass in, bullet
            pygame.event.post(pygame.event.Event(RED_COLLISION))  # 17c pass in the collision event here
            yellow_bullets.remove(bullet)  # 16ccc remove the bullet, so we can use it to fire again
        elif bullet.x > WIDTH:  # the yellow bullets goes to the right, so to the width of the screen on x pos
            yellow_bullets.remove(bullet)  # 16ccc remove the bullet, if it goes off the WIDTH (screen)

    for bullet in red_bullets:  # 16c making bullets move, from right to left by using -= bullets vel
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):  # 16cc checks to see, if red char has collided with what we pass in, bullet
            pygame.event.post(pygame.event.Event(YELLOW_COLLISION))  # 17c pass in the collision event here
            red_bullets.remove(bullet)  # 16ccc remove the bullet, so we can use it to fire again
        elif bullet.x < 0:  # the red bullets goes to the left, so if it's less than 0 on x pos, bullets gets removed
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)  # 23c we render text, antialiasing is always 1, and color white
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))  # 23cc we're making>
# the text appear at middle, by dividing height and width of text by 2, and appearing it at screens WIDTH/2 and HEIGHT/2
    pygame.display.update()  # 24 updating display FIRST before delay
    pygame.time.delay(5000)  # 24c delaying the screen by 5 seconds - let's winning text display for 5 seconds


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # 9create a rectangle, where our spaceship is inside
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # 9c arguments are = X pos, Y pos, Width, Height

    yellow_bullets = []
    red_bullets = []  # 13 creating an empty list for bullets

    yellow_health = 10  # 20 creating health and passing in events
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # 6this controls the speed of this while loop (FPS is hardcoded to) 60 times per second
        for event in pygame.event.get():  # 1this loop will check the various events that are occurring within our game
            if event.type == pygame.QUIT:  # 1c checking to see if the user has quit the game, or to continue our loop
                run = False
                pygame.quit()  # 27c we call pygame.quit here, rather than end of function, to actually quit it now

            if event.type == pygame.KEYDOWN:  # 14 if the key is pressed down
                if event.key == pygame.K_SPACE and len(yellow_bullets) < BULLET_AMOUNT:  # 15c if bullets are available>
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)  # 15 bullet >
# are rectangles, appears at: 1st argument x pos at the width, 2nd y pos at the height divided by 2 minus 2 pixels, ->
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < BULLET_AMOUNT:  # 15c then go ahead and create new
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)  # 15 3rd argument width and height->
                    red_bullets.append(bullet)  # of the bullets
                    BULLET_FIRE_SOUND.play()  # 29cc we play the bullet sounds here

            if event.type == RED_COLLISION:
                red_health -= 1  # 20 if red is hit, subtract 1 from  red_health
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_COLLISION:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""  # 20c empty string, gets replaced by appropriate text whenever a winner is found
        if red_health <= 0:
            winner_text = "Yellow won!"

        if yellow_health <= 0:
            winner_text = "Red won!"

        if winner_text != "":
            draw_winner(winner_text)  # 25 we call the function here, pass winners_text we created at step 20
            break  # 26 if we want to quit, we can call "pygame.quit()" at end of function, rather than "main()"

        keys_pressed = pygame.key.get_pressed()  # 10 tells the loop what keys are currently being pressed down
        yellow_handle_movement(keys_pressed, yellow)  # 11c we call it here inside "main" - it gives us us the list to->
        red_handle_movement(keys_pressed, red)  # 11c keys_pressed and our yellow and red character, that we pass in now

        handle_bullets(yellow_bullets, red_bullets, yellow, red)  # 16 we pass bullets and our chars here - rectangles

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        # 5c our draw function will simply be called here, drawing stuff on the screen
        # 9cc we pass in our "red" and "yellow" rectangles, where we have defined the draw_window function AND here
    main()  # 27 call main to keep playing
#    pygame.quit() 26c uncomment this, to quit game, rather than play next round


if __name__ == "__main__":  # 2this file will only run when we run it directly here, and not when it's being imported
    main()
