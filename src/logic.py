#Imports
import pygame
import os
from button_sprite import ButtonSprite
import constants as c
from card_sprite import CardSprite
from paths import resource_path



#Creates all buttons needed for the game screen and adds them to button_sprite
def create_game_buttons(button_sprite):
    declare_button = ButtonSprite(c.VIRTUAL_WIDTH / 2, 1010, 'declare')
    button_sprite.add(declare_button)
    back_button = ButtonSprite(100, 970, 'back')
    button_sprite.add(back_button)



#Creates all the cards that are in the player's hand and adds them to player_sprite
def create_player(player_sprite, game):
    #Creates a list of all the current Card objects in the player's hand
    existing_cards = [sprite.card for sprite in player_sprite]

    #Connects the backend code to update the cards in the player's hand
    #If a Card object exists in the backend code for the player but isn't visually shown, it will add the sprite to player_sprite
    for card in game.player.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, 0, c.PLAYER_Y)
            player_sprite.add(new_sprite)
    #If a Card object doesn't exist in the backend code for the player but does visually, it will remove the sprite from player_sprite
    for sprite in player_sprite:
        if sprite.card not in game.player.cards:
            player_sprite.remove(sprite)
        #Flips all the sprites so the front side of the card is showing
        sprite.flip('Front')
    
    #Loads in all the sprites in player_sprite to their correct coordinates depending on how many cards are in the player's hand
    card_positions(player_sprite)



#Creates all the cards that are in the deck and adds them to deck_sprite
def create_deck(deck_sprite, game):
    #Creates a list of all the current Card objects in the deck
    existing_cards = [sprite.card for sprite in deck_sprite]

    #Connects the backend code to update the cards in the deck
    #If a Card object exists in the backend code for the deck but isn't visually shown, it will add the sprite to deck_sprite
    for card in game.deck.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, c.DECK_X, c.DECK_Y)
            deck_sprite.add(new_sprite)
    #If a Card object doesn't exist in the backend code for the deck but does visually, it will remove the sprite from deck_sprite
    for sprite in deck_sprite:
        if sprite.card not in game.deck.cards:
            deck_sprite.remove(sprite)
        #Flips all the sprites so the back side of the card is showing
        sprite.flip('Back')



#Creates all the cards that are in the computer's hand and adds them to computer_sprite
def create_computer(computer_sprite, game):
    #Creates a list of all the current Card objects in the computer's hand
    existing_cards = [sprite.card for sprite in computer_sprite]

    #Connects the backend code to update the cards in the computer's hand
    #If a Card object exists in the backend code for the computer but isn't visually shown, it will add the sprite to computer_sprite
    for card in game.computer.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, 0, c.COMPUTER_Y)
            computer_sprite.add(new_sprite)
    #If a Card object doesn't exist in the backend code for the deck but does visually, it will remove the sprite from computer_sprite
    for sprite in computer_sprite:
        if sprite.card not in game.computer.cards:
            computer_sprite.remove(sprite)
        #Flips all the sprites so the back side of the card is showing
        #Only happens when the current phase of the round is not 'Phase_Declare'
        if game.phase != 'Phase_Declare':
            sprite.flip('Back')

    #Loads in all the sprites in computer_sprite to their correct coordinates depending on how many cards are in the computer's hand
    card_positions(computer_sprite)



#Creates all the cards that are in the discard pile and adds them to discard_sprite
def create_discard(discard_sprite, game):
    #Creates a list of all the current Card objects in the discard pile
    existing_cards = [sprite.card for sprite in discard_sprite]

    #Connects the backend code to update the cards in the discard pile
    #If a Card object exists in the backend code for the discard pile but isn't visually shown, it will remove the sprite from discard_sprite
    for card in game.discard.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, c.DISCARD_X, c.DISCARD_Y)
            discard_sprite.add(new_sprite)
    #If a Card object doesn't exist in the backend code for the discard pile but does visually, it will remove the sprite from discard_sprite
    for sprite in discard_sprite:
        if sprite.card not in game.discard.cards:
            discard_sprite.remove(sprite)
        #Flips all the sprites so the front side of the card is showing
        sprite.flip('Front')



#Updates the card positions for both the player's and computer's hands
def card_positions(current_sprite):
    #Checks how many cards are in the hand and updates the initial X coordinate based on that
    match len(current_sprite):
        case 1:
            X = c.CARD_X + 300
        case 2:
            X = c.CARD_X + 225
        case 3:
            X = c.CARD_X + 150
        case 4:
            X = c.CARD_X + 75
        case 5:
            X = c.CARD_X
        case 6:
            X = c.CARD_X - 75
    
    #Updates the X coordinate for all the cards in the hand, centering them on the screen
    for sprite in current_sprite:
        sprite.rect.centerx = X
        X += 150



#Updates the total scores for the player and computer once a new round begins
def update_scores(game, overall_computer_score, overall_player_score):
    #Updates the scores for the player and computer
    overall_computer_score += game.computer_score()
    overall_player_score += game.player_score()

    #If the player score is >= 100 (the player loses), the scores are reset
    if overall_player_score >= 100:
        overall_player_score = 0
        overall_computer_score = 0

    #Overall scores are returned
    return overall_computer_score, overall_player_score



#Creates all the menu buttons and adds them to button_sprite
def create_menu_buttons(button_sprite):
    play_button = ButtonSprite((c.VIRTUAL_WIDTH / 2) - 250, 550, 'play')
    button_sprite.add(play_button)
    rules_button = ButtonSprite((c.VIRTUAL_WIDTH / 2) + 250, 550, 'rules')
    button_sprite.add(rules_button)
    options_button = ButtonSprite((c.VIRTUAL_WIDTH / 2) - 250, 700, 'options')
    button_sprite.add(options_button)
    credits_button = ButtonSprite((c.VIRTUAL_WIDTH / 2) + 250, 700, 'credits')
    button_sprite.add(credits_button)
    quit_button = ButtonSprite(c.VIRTUAL_WIDTH / 2, 850, 'quit')
    button_sprite.add(quit_button)
    avatar_button = ButtonSprite(75, 75, 'avatar')
    button_sprite.add(avatar_button)



#Gets filepath for the font, loads it, creates a dictionary of fonts, and returns them
def create_fonts():
    font_path = resource_path(os.path.join('assets', 'fonts', 'Handjet', 'static', 'Handjet-Regular.ttf'))
    fonts = {}
    fonts['small'] = pygame.font.Font(font_path, 25)
    fonts['large'] = pygame.font.Font(font_path, 50)
    return fonts



#Creates a virtual mouse that is scaled to the computer's display size and returns its (x,y) coordinates
#Allows computers with different display sizes to click on objects on the screen correctly
def virtual_mouse(SCREEN):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = mouse_x * c.VIRTUAL_WIDTH / SCREEN.get_width()
    mouse_y = mouse_y * c.VIRTUAL_HEIGHT / SCREEN.get_height()
    return mouse_x, mouse_y