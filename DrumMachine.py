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

        draw_grid(screen)

        for even in pygame.event.get(): #get events from the queue
            if even.type == pygame.QUIT:
                run = False

        pygame.display.flip() #updates the contents of the entire display to the scren

    pygame.QUIT
    return 0

def draw_grid(screen):
    left_menu_box = pygame.draw.polygon(screen, var.purple, [(0, 0), (0,var.HEIGHT), (200, var.HEIGHT -200),(200, 0)], 5)
    botton_menu_box = pygame.draw.polygon(screen, var.purple, [(0,var.HEIGHT), (200, var.HEIGHT -200),(var.WIDTH, var.HEIGHT-200),(var.WIDTH, var.HEIGHT)], 5)

main()