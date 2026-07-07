#Imports
import pygame
import os
from paths import resource_path



#CardSprite class
class CardSprite(pygame.sprite.Sprite):
    #Creates a card that can be visually seen with (x,y) coordinates & a card object with attributes like rank and suit
    def __init__(self, card, x, y):
        #Sets up code so objects can work with Pygame
        super().__init__()

        #Attributes
        self._card = card
        self._click = False
        self._hover = False

        #Gets the rank and suit from the card object to set the filename for the CardSprite object
        rank = self._card.rank
        if rank == 'A':
            rank = 'ace'
        elif rank == 'K':
            rank = 'king' 
        elif rank == 'Q':
            rank = 'queen'
        elif rank == 'J':
            rank = 'jack'
        name = f'{rank}_of_{(self._card.suit).lower()}.png'

        #Loads the front side image for the CardSprite object
        front_image_path = resource_path(os.path.join('assets', 'images', 'cards', name))
        self._front_image = pygame.image.load(front_image_path).convert_alpha()
        self._front_image = pygame.transform.scale(self._front_image, (138, 200))

        #Loads the back side image for the CardSprite object
        back_image_path = resource_path(os.path.join('assets', 'images', 'cards', 'back_card.png'))
        self._back_image = pygame.image.load(back_image_path).convert_alpha()
        self._back_image = pygame.transform.scale(self._back_image, (138, 200))

        #Sets the image of the object as the back
        #Creates a rectangle the same size as the card and centers it at (x,y)
        self.image = self._back_image
        self.rect = self.image.get_rect(center=(x, y))



    #Allows card attribute to be accessed outside of this class
    @property
    def card(self):
        return self._card
    


    #If a CardSprite object has not been clicked before and is clicked, it will move up slightly and be added to the selected_cards list
    #Otherwise, it will move down slightly and be removed from the selected_cards list
    def update_on_click(self, selected_cards):
        if not self._click:
            selected_cards.append(self._card)
            self.rect.y -= 50
            self._click = True
        else:
            selected_cards.remove(self._card)
            self.rect.y += 50
            self._click = False
    


    #Sets the object's click attribute to False and changes its y-coordinate to player_y
    def revert(self, player_y):
        self._click = False
        self.rect.centery = player_y
 


    #Changes the object's image depending on the state parameter
    def flip(self, state):
        old_center = self.rect.center
        if state == 'Front':
            self.image = self._front_image
        elif state == 'Back':
            self.image = self._back_image
        self.rect = self.image.get_rect(center = old_center)



    #If the mouse is over a CardSprite object while its hover attribute is False and the state parameter is True, then it will upscale the
    #   object slightly and set its hover attribute to True
    #If the mouse if over a CardSprite object while its hover attribute is True and the state parameter is False, then it will downscale the
    #   object slightly and set its hover attribute to False
    #With this, it allows the object to get bigger when the mouse is over it and smaller when it is not
    def hovering(self, state):
        old_center = self.rect.center
        if self._hover == False and state == True:
            self._front_image = pygame.transform.scale_by(self._front_image, 5/4)
            self.rect = self._front_image.get_rect(center = old_center)
            self._hover = True
        elif self._hover == True and state == False:
            self._front_image = pygame.transform.scale_by(self._front_image, 4/5)
            self.rect = self._front_image.get_rect(center = old_center)
            self._hover = False