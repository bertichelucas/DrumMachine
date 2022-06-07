from asyncio.windows_events import NULL
import pygame
import dmVariables as var
import csv

def main():
    pygame.init() #Intializes all imported pygame modules

    screen = pygame.display.set_mode([var.WIDTH, var.HEIGHT]) #creates a display surface
    pygame.display.set_caption('Drum Machine') #changes the name of the window

    label_font = pygame.font.Font('CaviarDreams.ttf', 32) #initializes a font object
    medium_font = pygame.font.Font('CaviarDreams.ttf', 24) #medium font

    timer = pygame.time.Clock() #Creates a Clock object to help track time

    run = True
    
    boxes = []
    clicked = [[-1 for _ in range(var.beats)] for _ in range(var.instruments)] #Creates a list of lists with the beats per instrument. If the beat is clicked its value will be 1. Otherwise -1
    
    active_channels = [1 for _ in range(var.instruments)] #All our instruments channels
    sound_list = load_sounds()

    while run:
        
        timer.tick(var.fps) #updates the clock, called once per frame. Computes how many ms passed since last call
        screen.fill(var.background_color)

        beat_length = var.fps * 60 // var.bpm

        draw_grid(screen)
        draw_left_menu(screen, label_font, active_channels)
        boxes = draw_beat_boxes(screen, clicked, active_channels)
        draw_beat_tracker(screen)
        clear_button = draw_clear_button(screen, label_font)
        save_button, load_button = draw_save_load_buttons(screen, label_font)
        play_pause = draw_play_pause_button(screen, label_font)
        draw_game_status(screen, label_font, var.playing)
        bpm_rectangles = draw_bpm_rect(screen, medium_font)
        beat_rectangles = draw_beats_rect(screen, medium_font)
        instruments_rects = turn_instruments()

        if var.save_menu:
            exit_button, save_menu_button = draw_menu(screen, label_font, 'Save')
            input_box = draw_input_box(screen, label_font, var.beat_name, var.typing)
        if var.load_menu:
            exit_button, load_menu_button = draw_menu(screen, label_font, 'Load')
            delete_button = draw_delete_button(screen,label_font)
            loaded_rectangle, loaded_beats, var.load_index = draw_loaded_beats(screen, label_font, var.load_index)
            if 0 <= var.load_index < len(loaded_beats):
                beat_info = parse_beat(loaded_beats[var.load_index])
            else:
                beat_info = []
            

        if var.beat_changed:
            play_notes(clicked, sound_list, active_channels)
        var.beat_changed = False

        for event in pygame.event.get(): #get events from the queue
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not var.save_menu and not var.load_menu:
                for box in boxes: #checks for any collition with the beat rectangles
                    if box[0].collidepoint(event.pos): 
                        coords = box[1]
                        clicked[coords[1]][coords[0]] *= -1

            if event.type == pygame.MOUSEBUTTONUP and not var.save_menu and not var.load_menu: #all inputs when the player is not in menues
                if play_pause.collidepoint(event.pos): #play/pause
                    if var.playing:
                        var.playing = False
                    else:
                        var.playing = True
                elif bpm_rectangles[0].collidepoint(event.pos): #add bpm
                    var.bpm += 5
                elif bpm_rectangles[1].collidepoint(event.pos): #sub bpm
                    var.bpm -= 5
                elif beat_rectangles[0].collidepoint(event.pos): #add beats
                    var.beats += 1
                    for item in clicked:
                        item.append(-1)
                elif beat_rectangles[1].collidepoint(event.pos): #sub beats
                    if var.beats > 1: 
                        var.beats -= 1
                        for item in clicked:
                            item.pop(-1)
                elif clear_button.collidepoint(event.pos): #clear the table
                    clicked = [[-1 for _ in range(var.beats)] for _ in range(var.instruments)]
                elif save_button.collidepoint(event.pos): #open save menu
                    var.save_menu = True
                    var.playing = False
                elif load_button.collidepoint(event.pos): #open load menu
                    var.load_menu = True
                    var.playing = False

                for rect in instruments_rects: #makes a channel turned on or turned off
                    if rect.collidepoint(event.pos):
                        active_channels[instruments_rects.index(rect)] *= -1

            elif event.type == pygame.MOUSEBUTTONUP:  #inputs when player is in a menu
                if exit_button.collidepoint(event.pos): #exit menu
                    var.save_menu = var.load_menu = var.typing = False
                    var.playing = True
                    var.beat_name = ''
                if var.load_menu:
                    if loaded_rectangle.collidepoint(event.pos): #Clicked an space
                        var.load_index = (event.pos[1] - 100) // 50
                    if delete_button.collidepoint(event.pos):
                        if 0 <= var.load_index < len(loaded_beats):
                            pass
                    if load_menu_button.collidepoint(event.pos):
                        if beat_info:
                            var.beats = beat_info[0]
                            var.bpm = beat_info[1]
                            clicked = beat_info[2]
                            var.load_index = -1
                            var.load_menu = False
                            var.playing = True

                if var.save_menu:
                    if input_box.collidepoint(event.pos): #player clicks input option
                        if not var.typing:
                            var.typing = True
                        else:
                            var.typing = False
                    if save_menu_button.collidepoint(event.pos): #saves the current beat
                        route = open('saved_beats.csv', 'a')
                        route.write(f'{var.beat_name}; {var.beats}; {var.bpm};{clicked}\n')
                        route.close()
                        var.save_menu = var.typing = False
                        var.playing = True
                        var.beat_name = ''
            if event.type == pygame.TEXTINPUT and var.typing: #player is writing
                var.beat_name += event.text
            if event.type == pygame.KEYDOWN and var.typing:
                if event.key == pygame.K_BACKSPACE and var.beat_name != "":
                    var.beat_name = var.beat_name[:-1]

                    
        if var.playing:
            if var.active_length < beat_length:
                var.active_length += 1
            else:
                var.active_length = 0
                var.beat_changed = True
                if var.active_beat >= var.beats - 1:
                    var.active_beat = 0
                else:
                    var.active_beat +=1
                

        pygame.display.flip() #updates the contents of the entire display to the screen

    pygame.QUIT
    return 0

def draw_grid(screen):
    #Draw the grid in form of rectangles and polygons
    pygame.draw.polygon(screen, var.primary_color, [(0, 0), (0,var.HEIGHT), (200, var.HEIGHT -200),(200, 0)], 5) #left menu box
    pygame.draw.polygon(screen, var.primary_color, [(0,var.HEIGHT), (200, var.HEIGHT -200),(var.WIDTH, var.HEIGHT-200),(var.WIDTH, var.HEIGHT)], 5) #bottom menu box

def draw_left_menu(screen, label_font, actives):
    #draw the texts and lines of the left menu
    textlist = ['Hi hat', 'Snare', 'Bass Drum', 'Crash', 'Clap', 'Floor Tom']
    positionX = positionY = 25
    colors = (NULL, var.secondary_color, var.primary_color)
    for i in range(len(textlist)):
        screen.blit(label_font.render(textlist[i], True, colors[actives[i]]), (positionX, positionY))
        pygame.draw.line(screen, var.primary_color,(0,positionY + 75), (200,positionY + 75), 4)
        positionY += 100

def draw_beat_boxes(screen, clicked, active_channels):
    #Draw the beat boxes of the screen.
    boxes = []
    colors =(NULL, var.secondary_color, var.dark_yellow)
    for i in range(var.beats):
        for j in range(var.instruments):
            pygame.draw.rect(screen, var.background_color, [200 + i * ((var.WIDTH -200) // var.beats),(j*100), ((var.WIDTH - 200) //var.beats), (var.HEIGHT -200) // var.instruments], 5, 5)
            pygame.draw.rect(screen, var.primary_color, [200 + i * ((var.WIDTH -200) // var.beats),(j*100), ((var.WIDTH - 200) //var.beats), (var.HEIGHT -200) // var.instruments], 2, 5)
            if clicked[j][i] == 1:
                color = colors[active_channels[j]]
            else:
                color = var.background_color
            rect = pygame.draw.rect(screen, color, [200 + i * ((var.WIDTH -200) // var.beats) +5,(j*100) +5, ((var.WIDTH - 200) //var.beats) -10, (var.HEIGHT -200) // var.instruments -10],0 ,3)
            boxes.append((rect,(i,j)))
    return boxes

def draw_beat_tracker(screen):
    #Draws the beat tracker rectangle
    pygame.draw.rect(screen, var.cyan, [200  + (var.active_beat) * ((var.WIDTH -200) // var.beats), 0 , ((var.WIDTH -200)//var.beats), var.instruments*100], 5, 3)

def draw_play_pause_button(screen, label_font):
    #Draws the play and pause button
    play_pause = pygame.draw.polygon(screen, var.secondary_color,[(0,var.HEIGHT), (200, var.HEIGHT -200), (200, var.HEIGHT)], 0)
    play_text = label_font.render('Play/Pause', True, var.dark_purple)
    play_text = pygame.transform.rotozoom(play_text, 45, 1)
    screen.blit(play_text, (50, var.HEIGHT -150))
    return play_pause

def draw_game_status(screen, label_font, playing):
    #Draws the game status box
    pygame.draw.polygon(screen, var.dark_purple,[(0,var.HEIGHT), (200, var.HEIGHT -200), (0, var.HEIGHT -200)], 3)
    if playing:
        status_text = label_font.render('Playing', True, var.secondary_color)
    else:
        status_text = label_font.render('Paused', True, var.secondary_color)
    status_text = pygame.transform.rotozoom(status_text, 45, 1)
    screen.blit(status_text, (30, var.HEIGHT - 190))

def draw_bpm_rect(screen, medium_font):
    #Draws bpm rectangles
    pygame.draw.rect(screen, var.primary_color, [300, var.HEIGHT -150, 200 ,100], 5, 5)
    bpm_text = medium_font.render('Beats per Minute', True, var.secondary_color)
    bpm_text_quantity = medium_font.render(f'{var.bpm}', True, var.secondary_color)
    screen.blit(bpm_text, (308, var.HEIGHT -130))
    screen.blit(bpm_text_quantity, (370, var.HEIGHT -100))  

    #Drawing add and sub rectangles for bpm
    add_rect = pygame.draw.rect(screen, var.primary_color, (510, var.HEIGHT -150, 48, 48), 3, 5)
    sub_rect = pygame.draw.rect(screen, var.primary_color, (510, var.HEIGHT -100, 48, 48), 3, 5)
    add_text = medium_font.render('+5', True, var.secondary_color)
    sub_text = medium_font.render('-5', True, var.secondary_color)
    screen.blit(add_text, (520, var.HEIGHT -140))
    screen.blit(sub_text, (520, var.HEIGHT -90))
    return (add_rect, sub_rect)

def draw_beats_rect(screen, medium_font):
    #Draws beats rectangles
    pygame.draw.rect(screen, var.primary_color, [600, var.HEIGHT -150, 200 ,100], 5, 5)
    beats_text = medium_font.render('Beats per Loop', True, var.secondary_color)
    beats_text_quantity = medium_font.render(f'{var.beats}', True, var.secondary_color)
    screen.blit(beats_text, (608, var.HEIGHT -130))
    screen.blit(beats_text_quantity, (680, var.HEIGHT -100))  

    #Drawing add and sub rectangles for beats
    add_rect = pygame.draw.rect(screen, var.primary_color, (810, var.HEIGHT -150, 48, 48), 3, 5)
    sub_rect = pygame.draw.rect(screen, var.primary_color, (810, var.HEIGHT -100, 48, 48), 3, 5)
    add_text = medium_font.render('+1', True, var.secondary_color)
    sub_text = medium_font.render('-1', True, var.secondary_color)
    screen.blit(add_text, (820, var.HEIGHT -140))
    screen.blit(sub_text, (820, var.HEIGHT -90))
    return (add_rect, sub_rect)

def draw_save_load_buttons(screen, label_font):
    #Draws seave and load buttons
    save_button = pygame.draw.rect(screen, var.primary_color, [900, var.HEIGHT -150, 200, 48],3 ,5)
    load_button = pygame.draw.rect(screen, var.primary_color, [900, var.HEIGHT -100, 200 ,48], 3, 5)
    save_text = label_font.render('Save Beat', True, var.secondary_color)
    load_text = label_font.render('Load Beat', True, var.secondary_color)
    screen.blit(save_text, (920, var.HEIGHT - 145))
    screen.blit(load_text, (920, var.HEIGHT - 100))
    return (save_button, load_button)

def draw_menu(screen, label_font, type):
    #Draws the save menu
    pygame.draw.rect(screen, var.background_color, [0,0, var.WIDTH, var.HEIGHT])
    if type == 'Save':
        menu_text = label_font.render(f'{type} Menu: Enter a Name for Current Beat', True, var.secondary_color)
    else:
        menu_text = label_font.render(f'{type} Menu: Select a beat to {type}', True, var.secondary_color)
    screen.blit(menu_text, (400, 40))
    menu_button = pygame.draw.rect(screen, var.primary_color, [var.WIDTH //2 -200, var.HEIGHT -100, 400 ,90],3,5)
    menu_text = label_font.render(f'{type} Beat', True, var.secondary_color)
    screen.blit(menu_text, (var.WIDTH //2 - 70, var.HEIGHT -100 + 30))
    exit_button = pygame.draw.rect(screen, var.primary_color, [var.WIDTH -200, var.HEIGHT -100, 180, 90],3 ,5)
    exit_text = label_font.render('Close', True, var.secondary_color)
    screen.blit(exit_text, (var.WIDTH -160, var.HEIGHT - 70))
    return (exit_button, menu_button)


def draw_loaded_beats(screen, medium_font, load_index):
    #Draw Loaded Beats
    
    loaded_rectangle = pygame.draw.rect(screen,var.primary_color,[190, 90, 1000, 600], 3, 5)
    route = open('saved_beats.csv')
    csv_reader = csv.reader(route, delimiter=';')
    count = 0
    loaded_beats = []
    for line in csv_reader:
        loaded_beats.append(line)
        count += 1
        if load_index == count -1:
            pygame.draw.rect(screen, var.grey, [190, 100 + load_index * 50, 1000 ,50])
        row_text = medium_font.render(f'{count}  {line[0]}', True, var.secondary_color)
        screen.blit(row_text, (200, 50 + count * 50))

    route.close()
    
    return loaded_rectangle, loaded_beats, load_index

def parse_beat(line):
    #parses the loaded info to actual info in the game.
    _, beats, bpm, clicked = line
    beats = int(beats)
    bpm = int(bpm)
    clicked = clicked[2:-2]
    clicked_rows = list(clicked.split('], ['))
    parsed_clicked = []
    for row in clicked_rows:
        row = row.split(', ')
        for i in range(len(row)):
            row[i] = int(row[i])
        parsed_clicked.append(row)
    return [beats, bpm, parsed_clicked]

def draw_delete_button(screen, label_font):
    #Draws the delete button inside the load menu
    delete_button = pygame.draw.rect(screen, var.primary_color,[(var.WIDTH//2)- 500, var.HEIGHT -100, 200, 90], 3,5)
    delete_text = label_font.render('Delete Beat', True, var.secondary_color)
    screen.blit(delete_text, ((var.WIDTH//2)-485,var.HEIGHT -100 + 30))
    return delete_button

def draw_input_box(screen, label_font, beat_name, typing):
    #draws the input box  inside the save menu
    if typing:
        pygame.draw.rect(screen, var.grey, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, var.primary_color, [400, 200, 600, 200], 3, 5)
    entry_text = label_font.render(f'{beat_name}', True, var.secondary_color)
    screen.blit(entry_text, (420, 250))
    return entry_rect

def draw_clear_button(screen, label_font):
    #Clears all the beat board
    clear_button = pygame.draw.rect(screen, var.primary_color, [1150, var.HEIGHT -150, 200, 100],3 ,5)
    clear_text = label_font.render('Clear Beat', True, var.secondary_color)
    screen.blit(clear_text, (1160, var.HEIGHT - 120))
    return clear_button

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

def play_notes(clicked, sound_list, active_channels):
    #Play every clicked box from the sound list
    for i in range (len(clicked)):
        if var.active_beat >= var.beats:
            pass
        elif clicked[i][var.active_beat] == 1 and active_channels[i] == 1:
            sound_list[i].play()

def turn_instruments():
    instruments_rects = []
    for i in range(var.instruments):
        instruments_rects.append(pygame.rect.Rect((0, i *100), (200, 100)))
    return instruments_rects

main()