#mode_sprite: Contains the ModeSprite class that dictates how the mode cards work for the game
#Imports
import pygame
import os
from paths import resource_path
from save import read_value



#ModeSprite class
class ModeSprite(pygame.sprite.Sprite):
    #Creates a mode card that can be visually seen with (x,y) coordinates
    def __init__(self, name, x, y):
        #Sets up code so objects can work with Pygame
        super().__init__()

        #Name attribute
        self._name = name

        #Depending on the name of the object, a different description attribute is assigned to it
        match self._name:
            case 'normal':
                self._description = ['Normal', 'No modifiers']
            case 'creation':
                self._description = ['Creation', '+1 card for player']
            case 'preservation':
                self._description = ['Preservation', "Player's hand size remains at 5"]
            case 'destruction':
                self._description = ['Destruction', '-1 card for computer']

        #(x,y) attributes
        self._x, self._y = x, y

        #Sets the filename for the ModeSprite object
        name = f'{self._name}_mode.png'

        #Loads and scales the image for the ModeSprite object
        image_path = resource_path(os.path.join('assets', 'images', 'modes', name))
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 2/3)

        #Creates a rectangle the same size as the mode card and centers it at (x,y)
        self.rect = self.image.get_rect(center=(x, y))



    #Prints the description for the mode card onto the screen
    def print_description(self, GAME_SCREEN, fonts):
        #Boolean used to have the first line print in a larger font and all subsequent lines in a smaller font
        first = True

        #Initial y-coordinate for first line of text
        y = self._y + 130

        #Loop prints each line of text from self._description list
        for line in self._description:
            #First line of text is rendered in larger font
            if first:
                text = fonts['large'].render(line, True, (0, 0, 0))
                first = False
            #Subsequent lines of text are rendered in a smaller font
            else:
                text = fonts['small'].render(line, True, (0, 0, 0))

            #Draws it onto the screen
            text_rect = text.get_rect(center=(self._x, y))
            GAME_SCREEN.blit(text, text_rect)

            #Gets the new y-position for the next line of text
            y += text.get_height() + 1



    #Loads the current highscore for the mode card and prints it onto the screen
    def print_highscore(self, GAME_SCREEN, font):
        highscore = read_value(f'{self._name}_highscore', 0)
        text = font.render(f'Highscore: {highscore}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self._x, self._y + 300))
        GAME_SCREEN.blit(text, text_rect)

    

    #Allows name attribute to be accessed outside of this class
    @property
    def name(self):
        return self._name