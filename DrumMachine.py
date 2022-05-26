import pygame
import dmVariables as var

def main():
    pygame.init() #Intializes all imported pygame modules

    screen = pygame.display.set_mode([var.WIDTH, var.HEIGHT]) #creates a display surface
    pygame.display.set_caption('Drum Machine') #changes the name of the window

    label_font = pygame.font.Font('CaviarDreams.ttf', 32) #initializes a font object

    timer = pygame.time.Clock() #Creates a Clock object to help track time

    run = True
    
    boxes = []
    clicked = [[-1 for _ in range(var.beats)] for _ in range(var.instruments)] #Creates a list of lists with the beats per instrument. If the beat is clicked its value will be 1. Otherwise -1
    
    sound_list = load_sounds()

    while run:
        timer.tick(var.fps) #updates the clock, called once per frame. Computes how many ms passed since last call
        screen.fill(var.black)

        draw_grid(screen, label_font)
        boxes = draw_beat_boxes(screen, clicked)
        draw_beat_tracker(screen)
        draw_play_pause_buttons(screen)

        if var.beat_changed:
            play_notes(clicked, sound_list)
        var.beat_changed = False

        for event in pygame.event.get(): #get events from the queue
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in boxes: #checks for any collition with the beat rectangles
                    if box[0].collidepoint(event.pos): 
                        coords = box[1]
                        clicked[coords[1]][coords[0]] *= -1

        if var.playing:
            if var.active_length < var.beat_length:
                var.active_length += 1
            else:
                var.active_length = 0
                var.beat_changed = True
                if var.active_beat == var.beats - 1:
                    var.active_beat = 0
                else:
                    var.active_beat +=1
                

        pygame.display.flip() #updates the contents of the entire display to the screen

        beat_length = 3600 // var.bpm

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
        pygame.draw.line(screen, var.purple,(0,positionY + 75), (200,positionY + 75), 4)
        positionY += 100

def draw_beat_boxes(screen, clicked):
    #Draw the beat boxes of the screen.
    boxes = []
    for i in range(var.beats):
        for j in range(var.instruments):
            pygame.draw.rect(screen, var.black, [200 + i * ((var.WIDTH -200) // var.beats),(j*100), ((var.WIDTH - 200) //var.beats), (var.HEIGHT -200) // var.instruments], 5, 5)
            pygame.draw.rect(screen, var.purple, [200 + i * ((var.WIDTH -200) // var.beats),(j*100), ((var.WIDTH - 200) //var.beats), (var.HEIGHT -200) // var.instruments], 2, 5)
            if clicked[j][i] == 1:
                color = var.cyan
            else:
                color = var.black
            rect = pygame.draw.rect(screen, color, [200 + i * ((var.WIDTH -200) // var.beats) +5,(j*100) +5, ((var.WIDTH - 200) //var.beats) -10, (var.HEIGHT -200) // var.instruments -10],0 ,3)
            boxes.append((rect,(i,j)))
    return boxes

def draw_beat_tracker(screen):
    #Draws the beat tracker rectangle
    pygame.draw.rect(screen, var.yellow, [200  + (var.active_beat) * ((var.WIDTH -200) // var.beats), 0 , ((var.WIDTH -200)//var.beats), var.instruments*100], 5, 3)

def draw_play_pause_buttons(screen):
    pause = pygame.draw.polygon(screen, var.purple,[(0,var.HEIGHT), (200, var.HEIGHT -200), (200, var.HEIGHT)], 3)


def load_sounds():
    sound_list = [
    pygame.mixer.Sound('sounds/hi hat.WAV'),
    pygame.mixer.Sound('sounds/snare.WAV'),
    pygame.mixer.Sound('sounds/kick.WAV'),
    pygame.mixer.Sound('sounds/crash.wav'),
    pygame.mixer.Sound('sounds/clap.wav'),
    pygame.mixer.Sound('sounds/tom.wav')
    ]
    return sound_list

def play_notes(clicked, sound_list):
    #Play every clicked box from the sound list
    for i in range (len(clicked)):
        if clicked[i][var.active_beat] == 1:
            sound_list[i].play()

main()