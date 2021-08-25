import pygame
import os  # 7 importing os, Operating System, will allow us to define the paths to the images we want to load and use

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # 3the window/main surface
pygame.display.set_caption("Space Kynis!")  # name caption for our game, will display at upper left window

WHITE = (255, 255, 255)  # 4RGB - Red, Green, Blue: this will create white
BLACK = (0, 0, 0)  # 12c color code for black

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)  # 12arguments passed to draw our border = x pos, y pos, width, height
# to find the middle for our x pos, we can divide width/2 and we can minus it by 5, since our width is hardcoded

FPS = 60  # helps you control how often the screen needs to refresh, so your machine doesn't overwork itself needlessly
VEL = 5  # 10 velocity, how fast anything set to this will be moving, i.e spaceship moves with -=5/+= 5 to sides/up/down
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  # 8c we pass in these variables, rather than raw numbers in proper places

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))  # 7cwe path to the images
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  # 8 resizing spaceships and giving new dimensions
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))  # 7cc and load the images
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)  # 8c rotating the images


def draw_window(red, yellow):  # 5all our functions for drawing and colouring will go in here, for simplicity
    WIN.fill(WHITE)  # 4c fills out the screen with colour of choice from the RGB range - fill screen before drawing
    pygame.draw.rect(WIN, BLACK, BORDER)  # 12cc .rect takes a rectangle, draws it on a WIN(surface), color, rectangle
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # 9ccc we replace the earlier predefined position, with x and y
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  # 7ccc we pass in the positions into "blit", we load spaceship, not the img
    pygame.display.update()  # 4cc updates the display, and fills it with whatever we've input for it to show


def yellow_handle_movement(keys_pressed, yellow):  # 11 define new function, takes arguments "keys_pressed" and "yellow"
    if keys_pressed[pygame.K_a]:  # left
        yellow.x -= VEL  # when pressing the "a" key, yellow rectangle will move VEL (5) on the x axis (left)
    if keys_pressed[pygame.K_d]:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w]:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s]:  # down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):  # 11 define new function, takes arguments "keys_pressed" and "red"
    if keys_pressed[pygame.K_LEFT]:  # left
        red.x -= VEL  # when pressing the "left" key, the red rectangle will move VEL (5) on the x axis (left)
    if keys_pressed[pygame.K_RIGHT]:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP]:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN]:  # down
        red.y += VEL


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # 9create a rectangle, where our spaceship is inside
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # 9c arguments are = X pos, Y pos, Width, Height

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # 6this controls the speed of this while loop (FPS is hardcoded to) 60 times per second
        for event in pygame.event.get():  # 1this loop will check the various events that are occurring within our game
            if event.type == pygame.QUIT:  # 1c checking to see if the user has quit the game, or to continue our loop
                run = False

        keys_pressed = pygame.key.get_pressed()  # 10 tells the loop what keys are currently being pressed down
        yellow_handle_movement(keys_pressed, yellow)  # 11c we call it here inside "main" - it gives us us the list to->
        red_handle_movement(keys_pressed, red)  # 11c keys_pressed and our yellow and red character, that we pass in now
        draw_window(red, yellow)  # 5c our draw function will simply be called here, drawing stuff on the screen
        # 9cc we pass in our "red" and "yellow" rectangles, where we have defined the draw_window function AND here
    pygame.quit()


if __name__ == "__main__":  # 2this file will only run when we run it directly here, and not when it's being imported
    main()
