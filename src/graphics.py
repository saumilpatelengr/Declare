#Imports
import pygame
import os
from button_sprite import ButtonSprite
from paths import resource_path
import constants as c
from save import read_value



#Scales everything on GAME_SCREEN to fit on the computer's display when in fullscreen
#Allows computers with different display sizes to run the game
def render_to_screen(GAME_SCREEN, SCREEN):
    scaled = pygame.transform.smoothscale(GAME_SCREEN, SCREEN.get_size())
    SCREEN.blit(scaled, (0,0))



#Displays the scores for both players after a round ends
def display_score(GAME_SCREEN, game, button_sprite, overall_computer_score, overall_player_score, font, lost = False):
    #Creates a box where the scores and buttons will be placed
    create_box(GAME_SCREEN, 1575, 550, 0.8, 'square')

    #Updates the scores for the player and computer
    overall_computer_score += game.computer_score()
    overall_player_score += game.player_score()

    #Determines which lines of text to print (depending on if the player lost or not)
    if not lost:
        lines = [f"Computer Score: {overall_computer_score}", f"Your Score: {overall_player_score}"]
    else:
        lines = [f"Computer Score: {overall_computer_score}", f"Your Score: {overall_player_score}","Game Over"]

    #(x, y) coordinates for where to display the text on screen
    x, y = 1400, 375

    #Renders each line of text, draws it onto the screen, and gets the new y-position for the next line of text
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        GAME_SCREEN.blit(text, (x, y))
        y += text.get_height()

    #Creates and loads the play and menu buttons
    #Checks the size of button_sprite to ensure that buttons are not continuously added to it
    if len(button_sprite) < 4:
        play_button = ButtonSprite(1575, 600, 'play')
        button_sprite.add(play_button)
        menu_button = ButtonSprite(1575, 700, 'menu')
        button_sprite.add(menu_button)
        button_sprite.draw(GAME_SCREEN)



#Gets filepath for the background, loads it, scales it to GAME_SCREEN's size, and draws it to screen
def create_background(GAME_SCREEN):
    background_path = resource_path(os.path.join('assets', 'images', 'ui', 'background.png'))
    background_image = pygame.image.load(background_path).convert_alpha()
    background_image = pygame.transform.scale(background_image, (c.VIRTUAL_WIDTH, c.VIRTUAL_HEIGHT))
    GAME_SCREEN.blit(background_image, (0, 0))



#Gets filepath for the title, loads it, scales it, and draws it to screen
def create_title(GAME_SCREEN):
    title_path = resource_path(os.path.join('assets', 'images', 'ui', 'title.png'))
    title_image = pygame.image.load(title_path).convert_alpha()
    title_image = pygame.transform.scale_by(title_image, 1.5)
    title_rect = title_image.get_rect()
    title_rect.center = (c.VIRTUAL_WIDTH / 2, 300)
    GAME_SCREEN.blit(title_image, title_rect)



#Gets filepath for the box using the name parameter (square, rectangle), loads it, sets its (x,y) coordinates, scales it, and draws it to screen
def create_box(GAME_SCREEN, X, Y, scale, name):
    box_path = resource_path(os.path.join('assets', 'images', 'ui', f'{name}.png'))
    box_image = pygame.image.load(box_path).convert_alpha()
    box_image = pygame.transform.scale_by(box_image, scale)
    box_rect = box_image.get_rect()
    box_rect.center = (X, Y)
    GAME_SCREEN.blit(box_image, box_rect)



#Gets the current number of cards in the deck and prints it onto the screen
def print_deck_size(GAME_SCREEN, game, font):
    size = game.deck.size()
    text = font.render(f'{size}/52', True, (255, 255, 255))
    GAME_SCREEN.blit(text, (535, c.VIRTUAL_HEIGHT / 2))



#Loads the current highscore for the user and prints it onto the screen
def print_highscore(GAME_SCREEN, font):
    highscore = read_value('highscore', 0)
    text = font.render(f'Highscore: {highscore}', True, (255, 255, 255))
    GAME_SCREEN.blit(text, (1635, 0))



#Creates and prints all the rules of the game
def create_rules(GAME_SCREEN, font):
    #Creates a box for the rules to be printed in
    create_box(GAME_SCREEN, c.VIRTUAL_WIDTH / 2,c.VIRTUAL_HEIGHT / 2, 1.75, 'square')

    #Gets filepath for rules.txt and loads it into the rules variable
    file_path = resource_path(os.path.join('src', 'rules.txt'))
    with open(file_path, "r", encoding = "utf-8") as file:
        rules = file.read()
    
    #Turns the rules into a list of strings
    lines = rules.splitlines()

    #Renders each line of text, centers and draws it in the middle of the screen, and gets the new y-position for the next line of text
    y = 140
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        text_rect = text.get_rect(center=(c.VIRTUAL_WIDTH / 2, y))
        GAME_SCREEN.blit(text, text_rect)
        y += text.get_height() + 1



#Creates and prints the credits for the game
def create_credits(GAME_SCREEN, font):
    #Creates a box for the credits to be printed in
    create_box(GAME_SCREEN, c.VIRTUAL_WIDTH / 2, c.VIRTUAL_HEIGHT / 2, 1.6, 'square')

    #Gets filepath for credits.txt and loads it into credits variable
    file_path = resource_path(os.path.join("src", "credits.txt"))
    with open(file_path, "r", encoding="utf-8") as file:
        credits = file.read()

    #Turns the credits into a list of strings
    lines = credits.splitlines()

    #Renders each line of text, centers and draws it in the middle of the screen, and gets the new y-position for the next line of text
    y = 175
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        text_rect = text.get_rect(center=(c.VIRTUAL_WIDTH / 2, y))
        GAME_SCREEN.blit(text, text_rect)
        y += text.get_height() + 1



#Creates and prints the player's overall stats for the game
def create_stats(GAME_SCREEN, font):
    #Creates a box for the stats to be printed in
    create_box(GAME_SCREEN, c.VIRTUAL_WIDTH / 2, c.VIRTUAL_HEIGHT / 2, 1.6, 'square')

    #Lists containing the stat types and values for each
    words = [f"Highscore:", 
            f"Number of Games:", 
            f"Number of Rounds:", 
            f"Total Points:", 
            f"Number of Declares:"]
    numbers = [f"{read_value('highscore', 0)}", 
            f"{read_value('games', 0)}", 
            f"{read_value('rounds', 0)}",
            f"{read_value('points', 0)}", 
            f"{read_value('declares', 0)}"]

    #Renders all the text, draws it onto the screen, and gets the new y-position for the next line of text
    y = 175
    for word in words:
        text = font.render(word, True, (0, 0, 0))
        text_rect = text.get_rect(topleft=(600, y))
        GAME_SCREEN.blit(text, text_rect)
        y += text.get_height() + 1
    y = 175
    for number in numbers:
        text = font.render(number, True, (0, 0, 0))
        text_rect = text.get_rect(topright=(1300, y))
        GAME_SCREEN.blit(text, text_rect)
        y += text.get_height() + 1