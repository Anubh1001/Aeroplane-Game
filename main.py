from email.mime import base
import random  #For random numbers
import sys  #For using sys.exit to quit the program
import pygame  #For graphics
from pygame.locals import *  #Basic pygame imports


# Game's Global Variables
fps = 34  #Frames per second
screen_width = 289  #Screen width
screen_height = 511  #Screen height
screen = pygame.display.set_mode((screen_width, screen_height))   #Display the Screen
groundy = screen_height * 0.8  #Ground position
game_sprites = {} #Game's spirit
game_sounds = {} #Game's sounds

player ='gallery/sprites/aeroplane.png'
background = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'



def welcomeScreen():
    """
    This function displays the welcome screen
    """
    player_x = int(screen_width/5)
    player_y = int((screen_height - game_sprites['player'].get_height())/2)
    message_x = int((screen_width - game_sprites['message'].get_width())/2)
    message_y = int(screen_height * 0.12)
    base_x = 0

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, then start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_sprites['background'], (0, 0))
                screen.blit(game_sprites['player'], (player_x, player_y))
                screen.blit(game_sprites['message'], (message_x, message_y))
                screen.blit(game_sprites['base'], (base_x, groundy))
                pygame.display.update()
                fps_clock.tick(fps)


def mainGame():
    score = 0
    player_x = int(screen_width/5)
    player_y = int((screen_width/2))
    base_x = 0

    # Create 2 pipes for blitting on the screen
    new_pipe1 = getRandomPipe()
    new_pipe2 = getRandomPipe()

    # My upperpipe list
    upperPipes = [
        {'x': screen_width + 200, 'y': new_pipe1[0]['y']},
        {'x': screen_width + 200 + (screen_width/2), 'y': new_pipe2[0]['y']}
    ]
    # My lowerpipe list
    lowerPipes =[
        {'x': screen_width + 200, 'y': new_pipe1[1]['y']},
        {'x': screen_width + 200 + (screen_width/2), 'y': new_pipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxY = 10
    playerMinY = -8
    playerAccY = 1

    playerFlapAcc = -8  #Flapping velocity (Jumping)
    playerFlapped = False  #It is true only when flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
               if player_y > 0:
                   playerVelY = playerFlapAcc
                   playerFlapped = True
                   game_sounds['wing'].play()

        crashTest = isCollide(player_x, player_y, upperPipes, lowerPipes)   #True when you're crashed
        if crashTest:
            return

        #Score Calculation
        playerMidPos = player_x + game_sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_sprites['player'].get_width()/2
            if pipeMidPos <= playerMidPos <pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                game_sounds['point'].play()

        if playerVelY < playerMaxY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = game_sprites['player'].get_height() 
        player_y += min(playerVelY, groundy - player_y + playerHeight) 

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX                 

        # Add a new pipe when the 1st pipe is about to cross the leftmost screen side
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])


        #Remove the pipe if it goes out of the screen
        if upperPipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        # Lets blit our sprites now
        screen.blit(game_sprites['background'], (0,0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_sprites['base'], (base_x, groundy))
        screen.blit(game_sprites['player'], (player_x, player_y))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_sprites['numbers'][digit].get_width()
        Xoffset = (screen_width - width)/2 

        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit], (Xoffset, screen_height * 0.12))   
            Xoffset += game_sprites['numbers'][digit].get_width()

        pygame.display.update()
        fps_clock.tick(fps)    



def getRandomPipe():
    """
    Return a randomly generated pipe ( 1 bottom straight and 1 top rotated)
    """
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = screen_height/3
    y2 = offset + random.randrange(0, int(screen_height - game_sprites['base'].get_height() - 1.2*offset))
    pipe_x = screen_width + 10
    y1 =  pipeHeight - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},   #Upper Pipe
        {'x': pipe_x, 'y': y2}     #Lower Pipe
    ]
    return pipe


def isCollide(player_x, player_y, upperPipes, lowerPipes):
    if player_y > groundy - 25 or player_y < 0:
        game_sounds['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if (player_y < pipeHeight + pipe['y']) and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True
    
    for pipe in lowerPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if (player_y + game_sprites['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True

    return False



if __name__ == '__main__':
    
    #This will be executed when the game is started
    pygame.init()  #Initialize all pygame modules
    fps_clock = pygame.time.Clock()  #Create a clock
    pygame.display.set_caption('Anubh\'s Aeroplane Game')  #Set the caption of the window
    game_sprites['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    game_sprites['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    game_sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha() , 180),
        pygame.image.load(pipe).convert_alpha()
    )

    # Game Sounds 
    game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    game_sprites['player'] = pygame.image.load(player).convert_alpha()
    game_sprites['background'] = pygame.image.load(background).convert()


    # Game's Functions
    while True:
        welcomeScreen() #Show the welcome screen until the player presses a key
        mainGame() #Start the main game

