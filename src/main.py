#main.py: Combines all the code from the other files and creates the game loops for the game
#Imports
import pygame
import os
import random
from button_sprite import ButtonSprite
from game import Game
from save import write_value, read_value, reset_stats
from paths import resource_path
import constants as c
import graphics as g
import logic as l
import audio as a
from mode_sprite import ModeSprite



#Initializes Pygame modules, a fullscreen window, a virtual window where everything will be loaded onto, the window's caption, & game icon
pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
GAME_SCREEN = pygame.Surface((c.VIRTUAL_WIDTH, c.VIRTUAL_HEIGHT))
pygame.display.set_caption("Declare")
pygame.display.set_icon(pygame.image.load(resource_path(os.path.join('assets', 'images', 'other', 'icon.png'))))



#Controls the different screens in the game and allows the user to switch between them
def main():
    #Initial state to show the menu screen first
    state = "menu"

    #Creates the dictionary of fonts
    fonts = l.create_fonts()

    #Reads the values for SOUND and MUSIC to see if they are muted or not (both are not muted if no values exist)
    SOUND = read_value('sound', True)
    MUSIC = read_value('music', True)

    #Starts playing the music for the game
    a.play_audio('music', SOUND, MUSIC)

    #Initializes mode variable that determines what game mode the player is playing
    mode = None

    #Loop controls the different screens the user can access using return values
    #The loop breaks once the user presses the 'QUIT' button
    run = True
    while run:
        if state == "menu":
            state = menu(SOUND, MUSIC)
        elif state == 'rules':
            state = rules(fonts, SOUND, MUSIC)
        elif state == "game":
            state = game(fonts, SOUND, MUSIC, mode)
        elif state == 'options':
            state, SOUND, MUSIC = options(SOUND, MUSIC, fonts)
        elif state == "credits":
            state = credits(fonts, SOUND, MUSIC)
        elif state == "stats":
            state = stats(fonts, SOUND, MUSIC)
        elif state == "selection":
            state, mode = selection(fonts, SOUND, MUSIC)
        elif state == "quit":
            run = False

    #Writes the values for SOUND and MUSIC in case the user muted either of them
    write_value('sound', SOUND)
    write_value('music', MUSIC)

    #Quits the Pygame
    pygame.quit()



#Runs the menu screen for the game
def menu(SOUND, MUSIC):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a sprite group for all the buttons on the menu screen
    #Adds buttons to the sprite group
    button_sprite = pygame.sprite.Group()
    l.create_menu_buttons(button_sprite)

    #Loop controls mouse click events on buttons
    #Plays a sound effect when a button is clicked
    #Depending on the button that is clicked, a different value is returned to change between screens
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = l.virtual_mouse(SCREEN)
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'play':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'selection'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'rules':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'rules'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'credits':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'credits'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'options':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'options'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'quit':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'quit'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'stats':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'stats'
                    
        #Creates and draws the background and title
        g.create_background(GAME_SCREEN)
        g.create_title(GAME_SCREEN)

        #Draws the buttons onto the screen
        button_sprite.draw(GAME_SCREEN)

        #Scales everything on screen to the computer's screen size
        g.render_to_screen(GAME_SCREEN, SCREEN)

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(c.FPS)
            


#Runs the actual game for the user to play
def game(fonts, SOUND, MUSIC, mode):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a Game object that represents a single round being played
    #Depending on what the mode parameter is, values are passed into the Game object
    #Creation mode: +1 card for player
    #Destruction mode: -1 card for computer
    match mode:
        case 'normal' | 'preservation':
            game = Game()
        case 'creation':
            game = Game(6, 5)
        case 'destruction':
            game = Game(5, 4)

    #Holds the cards that the user wants to drop during their turn
    selected_cards = []

    #Initializes the start time used to measure a duration of time
    start_time = 0

    #Sets both the player's and computer's overall score to 0
    overall_player_score = 0
    overall_computer_score = 0

    #Reads the highscore for the player for the chosen mode (0 if no value exists)
    highscore = read_value(f'{mode}_highscore', 0)

    #Creates sprite groups for buttons, the deck, the player, the computer, and the discard pile
    button_sprite = pygame.sprite.Group()
    deck_sprite = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    computer_sprite = pygame.sprite.Group()
    discard_sprite = pygame.sprite.Group()

    #Creates a sprite group for the mode card and adds a sprite to it
    mode_sprite = pygame.sprite.GroupSingle()
    mode_sprite.add(ModeSprite(mode, 275, c.VIRTUAL_HEIGHT / 2))

    #Adds buttons to the button sprite group
    l.create_game_buttons(button_sprite)

    #Boolean to control stats are saved only once to the save state
    once = True

    #Boolean to control when the confirmation screen is shown when the player wants to quit from the game
    quit = False

    #Loop controls the flow of an entire game
    run = True
    while run:
        #Stores how many milliseconds passed since Pygame was initialized
        current_time = pygame.time.get_ticks()

        #Checks for any events
        for event in pygame.event.get():
            #Mouse for GAME_SCREEN is created
            mouse_x, mouse_y = l.virtual_mouse(SCREEN)

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
                            a.play_audio('button', SOUND, MUSIC)
                            game.player_declare()
                            game.phase = 'Phase_Declare'
                            write_value('declares', (read_value('declares', 0) + 1))
                            break

                        #If the back button is clicked on, changes phase to 'Phase_Quit' and sets previous phase to 'Phase_Player'
                        #button_sprite is emptied so that the confirmation screen buttons can be added to it
                        #quit is set to True to stop other objects from being displayed on the screen
                        #Plays a sound effect when the button is clicked
                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                            a.play_audio('button', SOUND, MUSIC)
                            game.phase = 'Phase_Quit'
                            game.previous_phase = 'Phase_Player'
                            button_sprite.empty()
                            l.create_confirmation_buttons(button_sprite)
                            quit = True

                    #If the player clicks on any cards in their hand, they will be 'selected' and will move up slightly
                    #Plays a sound effect when a card is clicked
                    for sprite in player_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            a.play_audio('card', SOUND, MUSIC)
                            sprite.update_on_click(selected_cards)

                    #If the player clicks on the deck, the cards selected by the player will be checked to see if they are valid to drop
                    #Valid to drop means that at least 1 card is selected and all selected cards are of the same rank
                    #If not valid, all cards in the player's hand will be reset to their original positions and selected_cards is emptied
                    #If valid, the player draws a card, drops all selected cards, selected_cards is emptied, and its now the computer's turn.
                    #   start_time is set to current_time and will be used to ensure that the computer takes only 1 second to take its turn
                    #Exception: if the game mode is preservation and the player selects more than 1 card when clicking the deck, all cards
                    #   in the player's hand will be reset to their original positions and selected_cards is emptied
                    #Plays a sound effect when cards are reset or when a card is drawn
                    for sprite in deck_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            chosen_cards = game.player_select_cards(selected_cards)
                            if chosen_cards == None:
                                for sprite in player_sprite:
                                    sprite.revert(c.PLAYER_Y)
                                a.play_audio('card', SOUND, MUSIC, 0.2)
                                selected_cards.clear()
                            elif mode == 'preservation' and len(selected_cards) > 1:
                                for sprite in player_sprite:
                                    sprite.revert(c.PLAYER_Y)
                                a.play_audio('card', SOUND, MUSIC, 0.2)
                                selected_cards.clear()
                            else:
                                game.player_draw()
                                game.player_drop(selected_cards)
                                selected_cards.clear()
                                a.play_audio('card', SOUND, MUSIC)
                                game.phase = 'Phase_Computer'
                                start_time = current_time
                                break
                    
                    #If the player clicks on the discard pile, the cards selected by the player will be checked to see if they are valid to drop
                    #Valid to drop means that at least 1 card is selected and all selected cards are of the same rank
                    #If not valid, all cards in the player's hand will be reset to their original positions and selected_cards is emptied
                    #If valid, the player will pickup the top card of the discard pile, drop all selected cards, selected_cards is emptied, and
                    #   its now the computer's turn. start_time is set to current_time and will be used to ensure that the computer takes only 
                    #   1 second to take its turn
                    #Exception: if the game mode is preservation and the player selects more than 1 card when clicking the discard pile, all
                    #   cards in the player's hand will be reset to their original positions and selected_cards is emptied
                    #Plays a sound effect when cards are reset or when a card is picked up from the discard pile
                    for sprite in discard_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            chosen_cards = game.player_select_cards(selected_cards)
                            if chosen_cards == None:
                                for sprite in player_sprite:
                                    sprite.revert(c.PLAYER_Y)
                                a.play_audio('card', SOUND, MUSIC, 0.2)
                                selected_cards.clear()
                            elif mode == 'preservation' and len(selected_cards) > 1:
                                for sprite in player_sprite:
                                    sprite.revert(c.PLAYER_Y)
                                a.play_audio('card', SOUND, MUSIC, 0.2)
                                selected_cards.clear()
                            else:   
                                game.player_pickup()
                                game.player_drop(selected_cards)
                                selected_cards.clear()
                                a.play_audio('card', SOUND, MUSIC)
                                game.phase = 'Phase_Computer'
                                start_time = current_time
                                break

                #If either the player or computer declare during their turn
                elif game.phase == 'Phase_Declare':
                    #If the player clicks on any buttons in the score box
                    for sprite in button_sprite:
                        #If the player clicks the 'MENU' button, changes phase to 'Phase_Quit' and sets previous phase to 'Phase_Declare'
                        #button_sprite is emptied so that the confirmation screen buttons can be added to it
                        #quit is set to True to stop other objects from being displayed on the screen
                        #Plays a sound effect when the button is clicked
                        if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'menu':
                            a.play_audio('button', SOUND, MUSIC)
                            game.phase = 'Phase_Quit'
                            game.previous_phase = 'Phase_Declare'
                            button_sprite.empty()
                            l.create_confirmation_buttons(button_sprite)
                            quit = True

                        #If the player clicks the 'PLAY' button, button_sprite is emptied to remove the 'MENU' and 'PLAY' buttons
                        #   from the screen. The overall scores for both the computer and player are updated & selected_cards is emptied.
                        #Creates the game buttons again once button_sprite is emptied
                        #'once' is set to True to ensure the next round's stats are saved correctly to the save state
                        #Plays a sound effect when the button is clicked
                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'play':
                            a.play_audio('button', SOUND, MUSIC, 0.2)
                            button_sprite.empty()
                            l.create_game_buttons(button_sprite)
                            overall_computer_score, overall_player_score = l.update_scores(game, overall_computer_score, overall_player_score)
                            selected_cards.clear()
                            once = True

                            #A new Game object is created to start another round of the game
                            #Depending on what the mode parameter is, values are passed into the Game object
                            #Creation mode: +1 card for player
                            #Destruction mode: -1 card for computer
                            match mode:
                                    case 'normal' | 'preservation':
                                        game = Game()
                                    case 'creation':
                                        game = Game(6, 5)
                                    case 'destruction':
                                        game = Game(5, 4)

                        #If the back button is clicked on, changes phase to 'Phase_Quit' and sets previous phase to 'Phase_Declare'
                        #button_sprite is emptied so that the confirmation screen buttons can be added to it
                        #quit is set to True to stop other objects from being displayed on the screen
                        #Plays a sound effect when the button is clicked
                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                            a.play_audio('button', SOUND, MUSIC)
                            game.phase = 'Phase_Quit'
                            game.previous_phase = 'Phase_Declare'
                            button_sprite.empty()
                            l.create_confirmation_buttons(button_sprite)
                            quit = True

                #If the player wants to quit from the game
                elif game.phase == 'Phase_Quit':
                    #If the player clicks on any buttons in the confirmation box
                    for sprite in button_sprite:
                        #If the yes button is clicked on, returns 'selection' and goes back to the selection screen
                        #Plays a sound effect when the button is clicked
                        if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'yes':
                            a.play_audio('button', SOUND, MUSIC)
                            return 'selection'

                        #If the no button is clicked on, changes phase back to the previous phase
                        #button_sprite is emptied so that the game buttons can be added to it
                        #quit is set to False to allow objects to be displayed on the screen again
                        #Plays a sound effect when the button is clicked
                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'no':
                            a.play_audio('button', SOUND, MUSIC)
                            game.phase = game.previous_phase
                            button_sprite.empty()
                            l.create_game_buttons(button_sprite)
                            quit = False
        
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
                a.play_audio('card', SOUND, MUSIC)
                game.phase = 'Phase_Player'

        #Creates and draws the background
        g.create_background(GAME_SCREEN)

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
            if overall_player_score + game.player_score() >= 100:
                g.display_score(GAME_SCREEN, game, button_sprite, overall_computer_score, overall_player_score, fonts['medium'], True)
            #Otherwise, the scores are printed
            else:
                g.display_score(GAME_SCREEN, game, button_sprite, overall_computer_score, overall_player_score, fonts['medium'])

            #If the computer's overall score is greater than the current game mode's highscore, the game mode's highscore is updated
            if overall_computer_score + game.computer_score() > highscore:
                    write_value(f'{mode}_highscore', overall_computer_score + game.computer_score())
                    highscore = overall_computer_score + game.computer_score()

            #Flips all the cards in the computer's hand to the front side
            for sprite in computer_sprite:
                sprite.flip('Front')

            #All cards in the player's hand are reset to their original positions
            for sprite in player_sprite:
                sprite.revert(c.PLAYER_Y)

        #If the player wants to quit from the game
        if game.phase == 'Phase_Quit':
            #Creates a box to house the buttons and message
            g.create_box(GAME_SCREEN, c.VIRTUAL_WIDTH / 2, c.VIRTUAL_HEIGHT / 2, 1.0)

            #Confirmation message split up in a list
            lines = ['Quit To Selection Menu?', 'Game progress will be lost', 'Stats will be saved']
            
            #Renders each line of text, centers and draws it in the middle of the screen, and gets the new y-position for the next line of text
            y = 350
            for line in lines:
                text = fonts['medium'].render(line, True, (0, 0, 0))
                text_rect = text.get_rect(center=(c.VIRTUAL_WIDTH / 2, y))
                GAME_SCREEN.blit(text, text_rect)
                y += text.get_height() + 1
        
        #Creates the deck, player's hand, computer's hand, and discard pile
        l.create_deck(deck_sprite, game)
        l.create_player(player_sprite, game)
        l.create_computer(computer_sprite, game)
        l.create_discard(discard_sprite, game)

        #If quit is True, then everything besides button_sprite is not drawn on screen
        button_sprite.draw(GAME_SCREEN)
        if not quit:
            #Draws the buttons, deck, player's hand, computer's hand, discard pile, and mode card onto the screen
            deck_sprite.draw(GAME_SCREEN)
            player_sprite.draw(GAME_SCREEN)
            computer_sprite.draw(GAME_SCREEN)
            discard_sprite.draw(GAME_SCREEN)
            mode_sprite.draw(GAME_SCREEN)

            #Prints the current deck size out of 52 onto the screen
            g.print_deck_size(GAME_SCREEN, game, fonts['small'])

            #Prints a guide for the player to aid them during their turns
            g.guide(GAME_SCREEN, fonts['medium'], game.phase, selected_cards, mode)

            #Prints the description for the mode card onto the screen
            mode_sprite.sprite.print_description(GAME_SCREEN, fonts)

        #Scales everything on screen to the computer's screen size
        g.render_to_screen(GAME_SCREEN, SCREEN)

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(c.FPS)



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
                mouse_x, mouse_y = l.virtual_mouse(SCREEN)
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'menu'

        #Creates and draws the background, back button, and rules box onto the screen
        g.create_background(GAME_SCREEN)
        button_sprite.draw(GAME_SCREEN)
        g.create_rules(GAME_SCREEN, fonts['small'])

        #Scales everything on screen to the computer's screen size
        g.render_to_screen(GAME_SCREEN, SCREEN)

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(c.FPS)



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
                mouse_x, mouse_y = l.virtual_mouse(SCREEN)
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'menu'

        #Creates and draws the background, back button, and credits box onto the screen
        g.create_background(GAME_SCREEN)
        button_sprite.draw(GAME_SCREEN)
        g.create_credits(GAME_SCREEN, fonts['small'])

        #Scales everything on screen to the computer's screen size
        g.render_to_screen(GAME_SCREEN, SCREEN)

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(c.FPS)



#Runs the options screen for the game
def options(SOUND, MUSIC, fonts):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a sprite group; creates all the option screen buttons and adds them to button_sprite
    button_sprite = pygame.sprite.Group()
    l.create_options_buttons(button_sprite, SOUND, MUSIC)

    #Boolean flag used to see if reset button is pressed
    reset = False

    #Loop controls mouse click events on buttons
    #Plays a sound effect when a button is clicked
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = l.virtual_mouse(SCREEN)
                for sprite in button_sprite:
                    #If the back button is clicked, it will return 'menu' to change to the menu screen and will return
                    #   both SOUND and MUSIC to ensure user preferences are saved (if either are muted or not)
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'menu', SOUND, MUSIC
                    
                    #If the music button is clicked, it will change if the button was clicked or not (button not being
                    #   clicked means that music is 'ON' and it being clicked means that music is 'OFF')
                    #If the click attribute changes to True, then it will change MUSIC to False and pause all music in
                    #   the game
                    #Otherwise, it will change MUSIC to True and unpause all music in the game
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'music':
                        a.play_audio('button', SOUND, MUSIC)
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
                        a.play_audio('button', SOUND, MUSIC)
                        sprite.mute()
                        if sprite.click == True:
                            SOUND = False
                        else:
                            SOUND = True

                    #If the reset button is clicked, it will delete all the sprites in button_sprite, create the confirmation 
                    #   message buttons, and set reset to True
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'reset':
                        a.play_audio('button', SOUND, MUSIC)
                        button_sprite.empty()
                        l.create_confirmation_buttons(button_sprite, True)
                        reset = True

                    #If the yes button is clicked, it will reset all the player's stats and go back to the original options screen
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'yes':
                        a.play_audio('button', SOUND, MUSIC)
                        reset_stats()
                        return 'options', SOUND, MUSIC

                    #If the no button is clicked, it will go back to the original options screen
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'no':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'options', SOUND, MUSIC
                        
        #Creates and draws the background, box, and buttons onto the screen
        g.create_background(GAME_SCREEN)
        g.create_box(GAME_SCREEN, c.VIRTUAL_WIDTH / 2, c.VIRTUAL_HEIGHT / 2, 1.0)
        button_sprite.draw(GAME_SCREEN)

        #If reset is True (after the reset button is clicked), then a confirmation message will be displayed on screen alongside
        #   the confirmation buttons
        if reset:
            #Confirmation message split up in a list
            lines = ['Delete Player Stats?', 'Are you sure?']
            
            #Renders each line of text, centers and draws it in the middle of the screen, and gets the new y-position for the next line of text
            y = 350
            for line in lines:
                text = fonts['medium'].render(line, True, (0, 0, 0))
                text_rect = text.get_rect(center=(c.VIRTUAL_WIDTH / 2, y))
                GAME_SCREEN.blit(text, text_rect)
                y += text.get_height() + 1

        #Scales everything on screen to the computer's screen size
        g.render_to_screen(GAME_SCREEN, SCREEN)

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(c.FPS)



#Runs the stats screen for the game
def stats(fonts, SOUND, MUSIC):
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
                mouse_x, mouse_y = l.virtual_mouse(SCREEN)
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'menu'

        #Creates and draws the background, back button, and stats box onto the screen
        g.create_background(GAME_SCREEN)
        button_sprite.draw(GAME_SCREEN)
        g.create_stats(GAME_SCREEN, fonts['medium'])

        #Scales everything on screen to the computer's screen size
        g.render_to_screen(GAME_SCREEN, SCREEN)

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(c.FPS)



#Runs the selection screen for the game
def selection(fonts, SOUND, MUSIC):
    #Used to control the FPS of the game
    clock = pygame.time.Clock()

    #Creates a sprite group; creates all the mode screen buttons and adds them to button_sprite
    button_sprite = pygame.sprite.Group()
    l.create_mode_buttons(button_sprite)

    #Loop controls mouse click events on buttons
    #If the back button is clicked on, 'menu' is returned and the screen changes to the menu screen
    #If any of the other buttons are clicked on, 'game' is returned with the mode's name as a second return value that
    #   will allow the user to play a specific game mode
    #Plays a sound effect when the button is clicked
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = l.virtual_mouse(SCREEN)
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'menu', None
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'normal':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'game', 'normal'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'creation':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'game', 'creation'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'preservation':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'game', 'preservation'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'destruction':
                        a.play_audio('button', SOUND, MUSIC)
                        return 'game', 'destruction'

        #Creates and draws the background and buttons onto the screen
        g.create_background(GAME_SCREEN)
        button_sprite.draw(GAME_SCREEN)

        #Besides the back button, the mode button's description and highscores are printed onto the screen below the buttons
        for sprite in button_sprite:
            if sprite.name != 'back':
                sprite.print_description(GAME_SCREEN, fonts)
                sprite.print_highscore(GAME_SCREEN, fonts['medium'])

        #Prints 'SELECT GAME MODE' onto the selection screen
        g.print_single_line(GAME_SCREEN, fonts['large'], 'SELECT GAME MODE', (255, 255, 255), c.VIRTUAL_WIDTH / 2, 200)

        #Scales everything on screen to the computer's screen size
        g.render_to_screen(GAME_SCREEN, SCREEN)

        #Refreshes the display window
        pygame.display.update()

        #Caps the game's FPS to whatever the 'FPS' variable is equal to
        clock.tick(c.FPS)



#Main function is run
if __name__ == "__main__":
    main()