from turtle import Screen, width
import pygame
import dmVariables as var

def main():
    pygame.init() #Intializes all imported pygame modules

    screen = pygame.display.set_mode([var.WIDTH, var.HEIGHT]) #creates a display surface
    pygame.display.set_caption('Drum Machine') #changes the name of the window

    label_font = pygame.font.Font('CaviarDreams.ttf', 32) #initializes a font object

    timer = pygame.time.Clock() #Creates a Clock object to help track time

    run = True

    while run:
        timer.tick(var.fps) #updates the clock, called once per frame. Computes how many ms passed since last call
        screen.fill(var.black)

        draw_grid(screen, label_font)
        

        for even in pygame.event.get(): #get events from the queue
            if even.type == pygame.QUIT:
                run = False

        pygame.display.flip() #updates the contents of the entire display to the scren

    pygame.QUIT
    return 0

def draw_grid(screen, label_font):
    #Draw the grid in form of rectangles and polygons
    left_menu_box = pygame.draw.polygon(screen, var.purple, [(0, 0), (0,var.HEIGHT), (200, var.HEIGHT -200),(200, 0)], 5)
    botton_menu_box = pygame.draw.polygon(screen, var.purple, [(0,var.HEIGHT), (200, var.HEIGHT -200),(var.WIDTH, var.HEIGHT-200),(var.WIDTH, var.HEIGHT)], 5)
    draw_left_menu(screen, label_font)

def draw_left_menu(screen, label_font):
    #draw the texts and lines of the left menu
    textlist = ['Hi hat', 'Snare', 'Bass Drum', 'Crash', 'Clap', 'Floor Tom']
    positionX = positionY = 25
    for text in textlist:
        screen.blit(label_font.render(text, True, var.cyan), (positionX, positionY))
        pygame.draw.line(screen, var.purple,(0,positionY + 75), (200,positionY + 75), 3)
        positionY += 100

main()