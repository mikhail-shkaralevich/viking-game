# How does a game work?
# 1 checking player input (the even loop)
# 2 use that information to place elements on the screen
# repeat

import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score:{current_time}', False, (255,255,255))
    score_rectangle = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface, score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []
    
def collisions(player, obstacles):
    if obstacles:   
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom < 300: #display the jump if the player is not on ground
        player_surface = player_jump
    else:
        #play walking animation if player is on ground
        player_index += 0.1



# starts pygame and all the subparts of it.
pygame.init()
# create a display surface
screen = pygame.display.set_mode((800, 400))
# add caption
pygame.display.set_caption("mario")

clock = pygame.time.Clock()

# Creating text:
# 1. create a font (text size and style)
# 2. write text on a surface
# 3. blit the text surface (in the game loop)
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# create a surface with plain color:
#test_surface = pygame.Surface((100, 200))
#test_surface.fill('Red')

# create surfaces with imported image
sky_surface = pygame.image.load('graphics/Sky.png').convert() #conver() converts image into a better format for pygame than .png.
ground_surface = pygame.image.load('graphics/ground.png').convert()

""" text_surface = test_font.render('My game', False, (64,64,64)).convert()
# draw a rectangle around text_surface for an easiser allignment of text.
text_rectangle = text_surface.get_rect(center=(400, 50))
 """
#Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
#snail_rectangle = snail_surface.get_rect(midbottom=(600, 300))

fly_surface = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()

obstacle_rect_list =[]

# Create vars for surface's position to make it changeable, dynamic.
#snail_x_pos = 600

# why to use rectangles?
# 1. Precise positioning of surfaces.
# 2. Helps to detect collisions.
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80, 300)) # get_rect() takes a surface and draws a rectangle around it.
# used to imitate gravity when a player falls
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render("Viking", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400,330))

# Timer
osbstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(osbstacle_timer, 1500)

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # closes the program.
        
        # only check for the 'active' game stage
        if game_active == True:
            # check for keyboard input
            # implement jump on the 'space' button.
            if event.type == pygame.KEYDOWN: # 1. check if any button was pressed
                if event.key == pygame.K_SPACE: # 2. check for a specific key
                    if player_rectangle.bottom == 300: # let the player to jump only if it's touching the floor
                        # make a player to jump
                        player_gravity = -20
            # make the player jump if a mouse is pressed on him.
            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.collidepoint(event.pos):
                player_gravity = -20
        else: # space key resumes the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # reset the game
                game_active = True
                #snail_rectangle.left = 600
                player_rectangle.bottom = 300
                start_time = int(pygame.time.get_ticks() / 1000)
        if event.type == osbstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100),300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100),210)))

    # break the game into 2 stages 'active' and 'not active'
    if game_active:
        # attach surfaces to our display surface.
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        #screen.blit(text_surface, (300, 50))
        # draw a rectangle behind the text_surface as a background
        #pygame.draw.rect(screen, '#c0e8ec', text_rectangle)
        #pygame.draw.rect(screen, '#c0e8ec', text_rectangle, 10) # adds some margin to the background rectangle.
        score = display_score()

        # draw a line on the screen that follows the mouse coursor.
        #pygame.draw.line(screen, 'Blue', (0,0), pygame.mouse.get_pos(), 10)
        # draw a circle
        #pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100)) # we create a rectangle 'on the fly'.

        #screen.blit(text_surface, text_rectangle)
        # update position of the 'snail_surface'
        #snail_x_pos -= 4
        #if snail_x_pos < -72: snail_x_pos = 800
        #screen.blit(snail_surface, (snail_x_pos, 260))
        """ snail_rectangle.x -= 4
        if snail_rectangle.right <= 0: snail_rectangle.left = 800
        screen.blit(snail_surface, snail_rectangle) """

        """ # read keyboard input from a player
        keys = pygame.key.get_pressed()
        # check if player pressed space then jump= player_rectangle.move(0, player_gravity)
        if keys[pygame.K_SPACE]:
            print('jump') """

        # change surface position throught changing rectangles position.
        #player_rectangle.left += 1

        # Player
        player_gravity += 1 # longer you fall - faster you fall
        player_rectangle.y += player_gravity
        # make sure the player doesn't fall below the ground
        if player_rectangle.bottom > 300: player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rectangle) # we take the player surface and we place it in the position of the rectangle.

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collision
        #if snail_rectangle.colliderect(player_rectangle):
        #    game_active = False
        game_active = collisions(player_rectangle, obstacle_rect_list)

        # check for player and snail collision. Returns 1 when collision occurs, otherwise 0.
        """ if player_rectangle.colliderect(snail_rectangle): # in python 0 is False
            print('collision') """

        # 1. check if a mouse colides with a player
        # 2. check if a mouse is pressed on the player.
        """ mouse_position = pygame.mouse.get_pos()
        if player_rectangle.collidepoint(mouse_position): 
            print(pygame.mouse.get_pressed()) """

    else: # 'not active' game stage
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    # draw all out elements
    # update everything
    pygame.display.update()
    # the loop shouldn't run faster than 60 times per second
    # set ceiling for game's frame rate
    clock.tick(60)
