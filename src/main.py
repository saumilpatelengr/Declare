#Imports
import pygame
import os
import random
from button_sprite import ButtonSprite
from card_sprite import CardSprite
from game import Game
from save import write_value, read_value
from paths import resource_path



#Constants for FPS and different coordinates for objects
FPS = 60
DECK_X, DECK_Y = 660, 550
CARD_X = 660
PLAYER_Y = 850
COMPUTER_Y = 250
DISCARD_X, DISCARD_Y = 960, 550
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1920, 1080



#Initializes Pygame modules, a fullscreen window, a virtual window where everything will be loaded onto, and the window's caption
pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
GAME_SCREEN = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
pygame.display.set_caption("Declare")



#Gets filepath for game icon, loads it, and sets it
icon_path = resource_path(os.path.join('assets', 'images', 'icons', 'icon.png'))
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)



#Scales everything on GAME_SCREEN to fit on the computer's display when in fullscreen
#Allows computers with different display sizes to run the game
def render_to_screen():
    scaled = pygame.transform.smoothscale(GAME_SCREEN, SCREEN.get_size())
    SCREEN.blit(scaled, (0,0))



#Creates all buttons needed for the game screen and adds them to button_sprite
def create_game_buttons(button_sprite):
    declare_button = ButtonSprite(VIRTUAL_WIDTH / 2, 1010, 'declare')
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
            new_sprite = CardSprite(card, 0, PLAYER_Y)
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
            new_sprite = CardSprite(card, DECK_X, DECK_Y)
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
            new_sprite = CardSprite(card, 0, COMPUTER_Y)
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
            new_sprite = CardSprite(card, DISCARD_X, DISCARD_Y)
            discard_sprite.add(new_sprite)
    #If a Card object doesn't exist in the backend code for the discard pile but does visually, it will remove the sprite from discard_sprite
    for sprite in discard_sprite:
        if sprite.card not in game.discard.cards:
            discard_sprite.remove(sprite)
        #Flips all the sprites so the front side of the card is showing
        sprite.flip('Front')



#Displays the scores for both players after a round ends
def display_score(game, button_sprite, overall_computer_score, overall_player_score, font, lost = False):
    #Creates a box where the scores and buttons will be placed
    create_box(1575, 550, 0.8, 'square')

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



#Updates the card positions for both the player's and computer's hands
def card_positions(current_sprite):
    #Checks how many cards are in the hand and updates the initial X coordinate based on that
    match len(current_sprite):
        case 1:
            X = CARD_X + 300
        case 2:
            X = CARD_X + 225
        case 3:
            X = CARD_X + 150
        case 4:
            X = CARD_X + 75
        case 5:
            X = CARD_X
        case 6:
            X = CARD_X - 75
    
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
    play_button = ButtonSprite((VIRTUAL_WIDTH / 2) - 250, 550, 'play')
    button_sprite.add(play_button)
    rules_button = ButtonSprite((VIRTUAL_WIDTH / 2) + 250, 550, 'rules')
    button_sprite.add(rules_button)
    options_button = ButtonSprite((VIRTUAL_WIDTH / 2) - 250, 700, 'options')
    button_sprite.add(options_button)
    credits_button = ButtonSprite((VIRTUAL_WIDTH / 2) + 250, 700, 'credits')
    button_sprite.add(credits_button)
    quit_button = ButtonSprite(VIRTUAL_WIDTH / 2, 850, 'quit')
    button_sprite.add(quit_button)
    avatar_button = ButtonSprite(75, 75, 'avatar')
    button_sprite.add(avatar_button)



#Gets filepath for the background, loads it, scales it to GAME_SCREEN's size, and draws it to screen
def create_background():
    background_path = resource_path(os.path.join('assets', 'images', 'ui', 'background.png'))
    background_image = pygame.image.load(background_path).convert_alpha()
    background_image = pygame.transform.scale(background_image, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    GAME_SCREEN.blit(background_image, (0, 0))



#Gets filepath for the title, loads it, and draws it to screen
def create_title():
    title_path = resource_path(os.path.join('assets', 'images', 'ui', 'title.png'))
    title_image = pygame.image.load(title_path).convert_alpha()
    title_rect = title_image.get_rect()
    title_rect.center = (VIRTUAL_WIDTH / 2, 300)
    GAME_SCREEN.blit(title_image, title_rect)



#Gets filepath for the box using the name parameter (square, rectangle), loads it, sets its (x,y) coordinates, scales it, and draws it to screen
def create_box(X, Y, scale, name):
    box_path = resource_path(os.path.join('assets', 'images', 'ui', f'{name}.png'))
    box_image = pygame.image.load(box_path).convert_alpha()
    box_image = pygame.transform.scale_by(box_image, scale)
    box_rect = box_image.get_rect()
    box_rect.center = (X, Y)
    GAME_SCREEN.blit(box_image, box_rect)



#Gets filepath for the font, loads it, creates a dictionary of fonts, and returns them
def create_fonts():
    font_path = resource_path(os.path.join('assets', 'fonts', 'Handjet', 'static', 'Handjet-Regular.ttf'))
    fonts = {}
    fonts['small'] = pygame.font.Font(font_path, 25)
    fonts['large'] = pygame.font.Font(font_path, 50)
    return fonts



#Gets the current number of cards in the deck and prints it onto the screen
def print_deck_size(game, font):
    size = game.deck.size()
    text = font.render(f'{size}/52', True, (255, 255, 255))
    GAME_SCREEN.blit(text, (535, VIRTUAL_HEIGHT / 2))



#Loads the current highscore for the user and prints it onto the screen
def print_highscore(font):
    highscore = read_value('highscore', 0)
    text = font.render(f'Highscore: {highscore}', True, (255, 255, 255))
    GAME_SCREEN.blit(text, (1635, 0))



#Creates and prints all the rules of the game
def create_rules(font):
    #Creates a box for the rules to be printed in
    create_box(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2, 1.75, 'square')

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
        text_rect = text.get_rect(center=(VIRTUAL_WIDTH / 2, y))
        GAME_SCREEN.blit(text, text_rect)
        y += text.get_height() + 1



#Creates a virtual mouse that is scaled to the computer's display size and returns its (x,y) coordinates
#Allows computers with different display sizes to click on objects on the screen correctly
def virtual_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = mouse_x * VIRTUAL_WIDTH / SCREEN.get_width()
    mouse_y = mouse_y * VIRTUAL_HEIGHT / SCREEN.get_height()
    return mouse_x, mouse_y



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



#Creates and prints the credits for the game
def create_credits(font):
    #Creates a box for the credits to be printed in
    create_box(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2, 1.6, 'square')

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
        text_rect = text.get_rect(center=(VIRTUAL_WIDTH / 2, y))
        GAME_SCREEN.blit(text, text_rect)
        y += text.get_height() + 1



#Creates and prints the player's overall stats
def create_stats(font):
    #Creates a box for the stats to be printed in
    create_box(250, 225, 0.75, 'rectangle')

    #All the stats that will be printed (values are read from save state)
    lines = [f"Highscore: {read_value('highscore', 0)}", 
             f"Games: {read_value('games', 0)}", 
             f"Rounds: {read_value('rounds', 0)}",
             f"Points: {read_value('points', 0)}", 
             f"Declares: {read_value('declares', 0)}"]
    
    #Renders each line of text, draws it to the (x,y) coordinates, and gets the new y-position for the next line of text
    x, y = 80, 150
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        GAME_SCREEN.blit(text, (x, y))
        y += text.get_height()



#Controls the different screens in the game and allows the user to switch between them
def main():
    #Initial state to show the menu screen first
    state = "menu"

    #Reads the highscore for the user (0 if no value exists)
    highscore = read_value('highscore', 0)

    #Creates the dictionary of fonts
    fonts = create_fonts()

    #Reads the values for SOUND and MUSIC to see if they are muted or not (both are not muted if no values exist)
    SOUND = read_value('sound', True)
    MUSIC = read_value('music', True)

    #Starts playing the music for the game
    play_audio('music', SOUND, MUSIC)

    #Loop controls the different screens the user can access using return values
    #The loop breaks once the user presses the 'QUIT' button
    run = True
    while run:
        if state == "menu":
            state = menu(fonts, SOUND, MUSIC)
        elif state == 'rules':
            state = rules(fonts, SOUND, MUSIC)
        elif state == "game":
            state = game(highscore, fonts, SOUND, MUSIC)
        elif state == 'options':
            state, SOUND, MUSIC = options(SOUND, MUSIC)
        elif state == "credits":
            state = credits(fonts, SOUND, MUSIC)
        elif state == "quit":
            run = False

    #Writes the values for SOUND and MUSIC in case the user muted either of them
    write_value('sound', SOUND)
    write_value('music', MUSIC)

    #Quits the Pygame
    pygame.quit()



#Runs the menu screen for the game
def menu(fonts, SOUND, MUSIC):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a sprite group for all the buttons on the menu screen
    #Adds buttons to the sprite group
    button_sprite = pygame.sprite.Group()
    create_menu_buttons(button_sprite)

    #Loop controls mouse click events on buttons
    #Plays a sound effect when a button is clicked
    #Depending on the button that is clicked, a different value is returned to change between screens
    #If the 'avatar' button is clicked on, the player's stats will be drawn onto the screen
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'play':
                        play_audio('button', SOUND, MUSIC)
                        return 'game'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'rules':
                        play_audio('button', SOUND, MUSIC)
                        return 'rules'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'credits':
                        play_audio('button', SOUND, MUSIC)
                        return 'credits'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'options':
                        play_audio('button', SOUND, MUSIC)
                        return 'options'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'quit':
                        play_audio('button', SOUND, MUSIC)
                        return 'quit'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'avatar':
                        play_audio('button', SOUND, MUSIC)
                        sprite.update_click()

        #Creates and draws the background and title
        create_background()
        create_title()

        #If the 'avatar' button is clicked on, the player's stats will be drawn onto the screen
        for sprite in button_sprite:
            if sprite.name == 'avatar' and sprite.click:
                create_stats(fonts['small'])

        #Draws the buttons onto the screen
        button_sprite.draw(GAME_SCREEN)

        #The current highscore for the user is also displayed
        print_highscore(fonts['large'])

        #Scales everything on screen to the computer's screen size
        render_to_screen()

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(FPS)
            


#Runs the actual game for the user to play
def game(highscore, fonts, SOUND, MUSIC):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a Game object that represents a single round being played
    game = Game()

    #Holds the cards that the user wants to drop during their turn
    selected_cards = []

    #Initializes the start time used to measure a duration of time
    start_time = 0

    #Sets both the player's and computer's overall score to 0
    overall_player_score = 0
    overall_computer_score = 0

    #Creates sprite groups for buttons, the deck, the player, the computer, and the discard pile
    button_sprite = pygame.sprite.Group()
    deck_sprite = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    computer_sprite = pygame.sprite.Group()
    discard_sprite = pygame.sprite.Group()

    #Adds buttons to the button sprite group
    create_game_buttons(button_sprite)

    #Boolean to control stats are saved only once to the save state
    once = True

    #Loop controls the flow of an entire game
    run = True
    while run:
        #Stores how many milliseconds passed since Pygame was initialized
        current_time = pygame.time.get_ticks()

        #Checks for any events
        for event in pygame.event.get():
            #Mouse for GAME_SCREEN is created
            mouse_x, mouse_y = virtual_mouse()

            #If the mouse is over a card in the player's hand, it will enlarge the card the mouse is over
            for sprite in player_sprite:
                if sprite.rect.collidepoint(mouse_x, mouse_y):
                    sprite.hovering(True)
                else:
                    sprite.hovering(False)

            #Looking for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Player's turn
                if game.phase == 'Phase_Player':
                    for sprite in button_sprite:
                        #If the player clicks on the 'DECLARE' button during their turn, then points are counted up for the round
                        #Plays a sound effect when the button is clicked
                        #Changes phase to 'Phase_Declare' to handle the round's results
                        #Increments the 'declares' stat in the save start by 1
                        if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'declare':
                            play_audio('button', SOUND, MUSIC)
                            game.player_declare()
                            game.phase = 'Phase_Declare'
                            write_value('declares', (read_value('declares', 0) + 1))
                            break

                        #If the back button is clicked on, 'menu' is returned and the screen changes to the menu screen
                        #Plays a sound effect when the button is clicked
                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                            play_audio('button', SOUND, MUSIC)
                            return 'menu'

                    #If the player clicks on any cards in their hand, they will be 'selected' and will move up slightly
                    #Plays a sound effect when a card is clicked
                    for sprite in player_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            play_audio('card', SOUND, MUSIC)
                            sprite.update_on_click(selected_cards)

                    #If the player clicks on the deck, the cards selected by the player will be checked to see if they are valid to drop
                    #Valid to drop means that at least 1 card is selected and all selected cards are of the same rank
                    #If not valid, all cards in the player's hand will be reset to their original positions and selected_cards is emptied
                    #If valid, the player draws a card, drops all selected cards, selected_cards is emptied, and its now the computer's turn.
                    #   start_time is set to current_time and will be used to ensure that the computer takes only 1 second to take its turn
                    #Plays a sound effect when cards are reset or when a card is drawn
                    for sprite in deck_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            chosen_cards = game.player_select_cards(selected_cards)
                            if chosen_cards == None:
                                for sprite in player_sprite:
                                    sprite.revert(PLAYER_Y)
                                play_audio('card', SOUND, MUSIC, 0.2)
                                selected_cards.clear()
                            else:
                                game.player_draw()
                                game.player_drop(selected_cards)
                                selected_cards.clear()
                                play_audio('card', SOUND, MUSIC)
                                game.phase = 'Phase_Computer'
                                start_time = current_time
                                break
                    
                    #If the player clicks on the discard pile, the cards selected by the player will be checked to see if they are valid to drop
                    #Valid to drop means that at least 1 card is selected and all selected cards are of the same rank
                    #If not valid, all cards in the player's hand will be reset to their original positions and selected_cards is emptied
                    #If valid, the player will pickup the top card of the discard pile, drop all selected cards, selected_cards is emptied, and
                    #   its now the computer's turn. start_time is set to current_time and will be used to ensure that the computer takes only 
                    #   1 second to take its turn
                    #Plays a sound effect when cards are reset or when a card is picked up from the discard pile
                    for sprite in discard_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            chosen_cards = game.player_select_cards(selected_cards)
                            if chosen_cards == None:
                                for sprite in player_sprite:
                                    sprite.revert(PLAYER_Y)
                                play_audio('card', SOUND, MUSIC, 0.2)
                                selected_cards.clear()
                            else:   
                                game.player_pickup()
                                game.player_drop(selected_cards)
                                selected_cards.clear()
                                play_audio('card', SOUND, MUSIC)
                                game.phase = 'Phase_Computer'
                                start_time = current_time
                                break

                #If either the player or computer declare during their turn
                elif game.phase == 'Phase_Declare':
                    #If the player clicks on any buttons in the score box
                    for sprite in button_sprite:
                        #If the player clicks the 'MENU' button, then the user will be redirected to the menu screen
                        #Plays a sound effect when the button is clicked
                        if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'menu':
                            play_audio('button', SOUND, MUSIC)
                            return 'menu'

                        #If the player clicks the 'PLAY' button, button_sprite is emptied to remove the 'MENU' and 'PLAY' buttons
                        #   from the screen. The overall scores for both the computer and player are updated, selected_cards is emptied,
                        #   and a new Game object is created to start another round of the game
                        #Creates the game buttons again once button_sprite is emptied
                        #'once' is set to True to ensure the next round's stats are saved correctly to the save state
                        #Plays a sound effect when the button is clicked
                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'play':
                            play_audio('button', SOUND, MUSIC, 0.2)
                            button_sprite.empty()
                            create_game_buttons(button_sprite)
                            overall_computer_score, overall_player_score = update_scores(game, overall_computer_score, overall_player_score)
                            selected_cards.clear()
                            game = Game()
                            once = True

                        #If the back button is clicked on, 'menu' is returned and the screen changes to the menu screen
                        #Plays a sound effect when the button is clicked
                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                            play_audio('button', SOUND, MUSIC)
                            return 'menu'

        #Computer's turn
        #'current_time - start_time >= 1000' ensures that the computer's turn takes 1 second to complete
        if game.phase == 'Phase_Computer' and current_time - start_time >= 1000:
            #Picks a random number between 10-15 inclusive to create a sense of randomness in the computer's decision
            number = random.randint(10, 15)

            #If the total number of points in the computer's hand is less than or equal to the random number, it will declare
            #   and change the phase to 'Phase_Declare'
            #Otherwise, the computer will take its turn and change the phase to 'Phase_Player' once it is done
            #Plays a sound effect after the computer draws/picks up a card
            if game.computer.points() <= number:
                game.computer.declare(game.player)
                game.phase = 'Phase_Declare'
            else:
                game.computer_turn()
                play_audio('card', SOUND, MUSIC)
                game.phase = 'Phase_Player'

        #Creates and draws the background
        create_background()

        #If either the player or computer declare during their turn
        if game.phase == 'Phase_Declare':
            #Once a round ends, stats are saved into the save state
            if once:
                #If the player lost, the 'games' stat is incremented by 1
                #The 'rounds' stat is incremented by 1 and the 'points' stat is incremented by the computer's total points for the round
                if overall_player_score + game.player_score() >= 100:
                    write_value('games', (read_value('games', 0) + 1))
                write_value('rounds', (read_value('rounds', 0) + 1))
                write_value('points', (read_value('points', 0) + game.computer_score()))
                
                #'once' is set to False to ensure that the stats are only saved once per round
                once = False

            #If the player's overall score is greater than or equal to 100 (meaning they lose), 'Game Over' is printed alongside
            #   the scores
            #If the computer's overall score is greater than the current highscore, the highscore is updated
            if overall_player_score + game.player_score() >= 100:
                display_score(game, button_sprite, overall_computer_score, overall_player_score, fonts['large'], True)
                if overall_computer_score + game.computer_score() > highscore:
                    write_value('highscore', overall_computer_score + game.computer_score())
            #Otherwise, the scores are printed
            else:
                display_score(game, button_sprite, overall_computer_score, overall_player_score, fonts['large'])

            #Flips all the cards in the computer's hand to the front side
            for sprite in computer_sprite:
                sprite.flip('Front')

            #All cards in the player's hand are reset to their original positions
            for sprite in player_sprite:
                sprite.revert(PLAYER_Y)
        
        #Creates the deck, player's hand, computer's hand, and discard pile
        create_deck(deck_sprite, game)
        create_player(player_sprite, game)
        create_computer(computer_sprite, game)
        create_discard(discard_sprite, game)

        #Draws the buttons, deck, player's hand, computer's hand, and discard pile onto the screen
        button_sprite.draw(GAME_SCREEN)
        deck_sprite.draw(GAME_SCREEN)
        player_sprite.draw(GAME_SCREEN)
        computer_sprite.draw(GAME_SCREEN)
        discard_sprite.draw(GAME_SCREEN)

        #Prints the current deck size out of 52 alongside the current highscore onto the screen
        print_deck_size(game, fonts['small'])
        print_highscore(fonts['large'])

        #Scales everything on screen to the computer's screen size
        render_to_screen()

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(FPS)



#Runs the rules screen for the game
def rules(fonts, SOUND, MUSIC):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a sprite group that can hold a single sprite; creates the back button and adds it to the sprite group
    button_sprite = pygame.sprite.GroupSingle()
    back_button = ButtonSprite(100, 970, 'back')
    button_sprite.add(back_button)

    #Loop controls mouse click events on the back button
    #If the back button is clicked on, 'menu' is returned and the screen changes to the menu screen
    #Plays a sound effect when the button is clicked
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        play_audio('button', SOUND, MUSIC)
                        return 'menu'

        #Creates and draws the background, back button, and rules box onto the screen
        create_background()
        button_sprite.draw(GAME_SCREEN)
        create_rules(fonts['small'])

        #Scales everything on screen to the computer's screen size
        render_to_screen()

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(FPS)



#Runs the credits screen for the game
def credits(fonts, SOUND, MUSIC):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a sprite group that can hold a single sprite; creates the back button and adds it to the sprite group
    button_sprite = pygame.sprite.GroupSingle()
    back_button = ButtonSprite(100, 970, 'back')
    button_sprite.add(back_button)

    #Loop controls mouse click events on the back button
    #If the back button is clicked on, 'menu' is returned and the screen changes to the menu screen
    #Plays a sound effect when the button is clicked
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        play_audio('button', SOUND, MUSIC)
                        return 'menu'

        #Creates and draws the background, back button, and credits box onto the screen
        create_background()
        button_sprite.draw(GAME_SCREEN)
        create_credits(fonts['small'])

        #Scales everything on screen to the computer's screen size
        render_to_screen()

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(FPS)



#Runs the options screen for the game
def options(SOUND, MUSIC):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a sprite group that can hold a single sprite; creates the back button and adds it to the sprite group
    button_sprite = pygame.sprite.Group()
    back_button = ButtonSprite(100, 970, 'back')
    button_sprite.add(back_button)

    #If SOUND is True, then draws the 'ON' version of the sound button onto the screen (all sound effects will play in the game)
    #Otherwise, it will draw the 'OFF' version of the sound button onto the screen (all sound effects are muted in the game)
    if SOUND:
        sound_button = ButtonSprite((VIRTUAL_WIDTH / 2) - 150, VIRTUAL_HEIGHT / 2, 'sound', 0.75, False)
    else:
        sound_button = ButtonSprite((VIRTUAL_WIDTH / 2) - 150, VIRTUAL_HEIGHT / 2, 'sound', 0.75, True)
    button_sprite.add(sound_button)

    #If MUSIC is True, then draws the 'ON' version of the music button onto the screen (music will play in the game)
    #Otherwise, it will draw the 'OFF' version of the music button onto the screen (music will be muted in the game)
    if MUSIC:
        music_button = ButtonSprite((VIRTUAL_WIDTH / 2) + 150, VIRTUAL_HEIGHT / 2, 'music', 0.75, False)
    else:
        music_button = ButtonSprite((VIRTUAL_WIDTH / 2) + 150, VIRTUAL_HEIGHT / 2, 'music', 0.75, True)
    button_sprite.add(music_button)

    #Loop controls mouse click events on buttons
    #Plays a sound effect when a button is clicked
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    #If the back button is clicked, it will return 'menu' to change to the menu screen and will return
                    #   both SOUND and MUSIC to ensure user preferences are saved (if either are muted or not)
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        play_audio('button', SOUND, MUSIC)
                        return 'menu', SOUND, MUSIC
                    #If the music button is clicked, it will change if the button was clicked or not (button not being
                    #   clicked means that music is 'ON' and it being clicked means that music is 'OFF')
                    #If the click attribute changes to True, then it will change MUSIC to False and pause all music in
                    #   the game
                    #Otherwise, it will change MUSIC to True and unpause all music in the game
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'music':
                        play_audio('button', SOUND, MUSIC)
                        sprite.mute()
                        if sprite.click == True:
                            MUSIC = False
                            pygame.mixer.music.pause()
                        else:
                            MUSIC = True
                            pygame.mixer.music.unpause()
                    #If the sound button is clicked, it will change if the button was clicked or not (button not being 
                    #   clicked means that sound is 'ON' and it being clicked means that sound is 'OFF')
                    #If the click attribute changes to True, then it will change SOUND to False and any sound effects in
                    #   the game will not play when objects are interacted with
                    #Otherwise, it will change SOUND to True and any sound effects in the game will play when objects are
                    #   interacted with
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'sound':
                        play_audio('button', SOUND, MUSIC)
                        sprite.mute()
                        if sprite.click == True:
                            SOUND = False
                        else:
                            SOUND = True
                        
        #Creates and draws the background, box, and buttons onto the screen
        create_background()
        create_box(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2, 1.0, 'square')
        button_sprite.draw(GAME_SCREEN)

        #Scales everything on screen to the computer's screen size
        render_to_screen()

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(FPS)



#Main function is run
if __name__ == "__main__":
    main()