
#Colors used in the drum machine
black = (0, 0 ,0)
purple = (106,13,173)
cyan = (0, 255, 255)
yellow = (255,225,32)


#Screen size
WIDTH = 1400
HEIGHT = 800


#Framerate
fps = 60


#Program Variables
beats = 8
instruments = 6
bpm = 240
beat_length = fps * 60 // bpm
active_length = 0
active_beat = 0
playing = True
beat_changed = True



unclicked = -1
clicked = 1
