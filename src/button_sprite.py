#Imports
import pygame
import os



#ButtonSprite class
class ButtonSprite(pygame.sprite.Sprite):
    #Creates a button that can visually be seen with (x,y) coordinates, a name, scale, and seeing if the button has been clicked or not
    def __init__(self, x, y, name, scale = 0.75, click = False):
        #Sets up code so objects can work with Pygame
        super().__init__()

        #Attributes
        self._name = name
        self._click = click

        #Uses the name of the button to load its image
        name = f'{name}_button.png'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'ui', name)
        self._og_image = pygame.image.load(image_path).convert_alpha()
        self._og_image = pygame.transform.scale_by(self._og_image, scale)

        #For the music and sound buttons, they can be turned "on" and "off"
        #Depending if they have been clicked or not, either the "on" or "off" button version of these buttons are loaded and set
        if self._name == 'music' or self._name == 'sound':
            name = f'{self._name}_off_button.png'
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, '..', 'assets', 'images', 'ui', name)
            self._off_image = pygame.image.load(image_path).convert_alpha()
            self._off_image = pygame.transform.scale_by(self._off_image, scale)

            #Checks to see if the button has been clicked and which version of the button should be set
            if self._click == False:
                self.image = self._og_image
            else:
                self.image = self._off_image
        #If any other button, the "og" or default version of the button is set
        else:
            self.image = self._og_image

        #Creates a rectangle the same size as the button and centers it at (x,y)
        self.rect = self.image.get_rect(center=(x, y))



    #Allows name attribute to be accessed outside of this class
    @property
    def name(self):
        return self._name
    


    #Allows click attribute to be accessed outside of this class
    @property
    def click(self):
        return self._click
    


    #For the music and sound buttons (buttons with 2 states), changes their image to the other state
    def mute(self):
        old_center = self.rect.center
        if not self._click:
            self.image = self._off_image
            self._click = True
        else:
            self.image = self._og_image
            self._click = False
        self.rect = self.image.get_rect(center = old_center)