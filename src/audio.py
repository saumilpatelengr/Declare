#audio.py: Contains functions relating to the audio for the game
#Imports
import pygame
import os
from paths import resource_path



#Allows for sound effects and music to be played in the game
def play_audio(name, SOUND, MUSIC, volume = 1.0):
    #Gets the filepath for the music or sound effect
    path = resource_path(os.path.join('assets', 'audio', f'{name}.mp3'))

    #If the name parameter is 'music', then it will load the audio as music. Otherwise, it will load it as a sound effect
    #MUSIC and SOUND are booleans used to check if the user wants music or sound effects on while they play the game
    if name == 'music':
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        if not MUSIC:
            pygame.mixer.music.pause()
    elif name != 'music' and SOUND:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play()