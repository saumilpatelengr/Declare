import pygame
import os
import random
from src.button_sprite import ButtonSprite
from src.card_sprite import CardSprite
from src.game import Game
from src.save import write_value, read_value

pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Declare")
FPS = 60
DECK_X, DECK_Y = 660, 550
CARD_X = 660
PLAYER_Y = 850
COMPUTER_Y = 250
DISCARD_X, DISCARD_Y = 960, 550
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1920, 1080
GAME_SCREEN = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, 'assets', 'images', 'icons', 'icon.png')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

def render_to_screen():
    scaled = pygame.transform.smoothscale(GAME_SCREEN, SCREEN.get_size())
    SCREEN.blit(scaled, (0,0))

def create_game_buttons(button_sprite):
    declare_button = ButtonSprite(VIRTUAL_WIDTH / 2, 1010, 'declare')
    button_sprite.add(declare_button)

def create_player(player_sprite, game):
    existing_cards = [sprite.card for sprite in player_sprite]
    for card in game.player.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, 0, PLAYER_Y)
            player_sprite.add(new_sprite)

    for sprite in player_sprite:
        if sprite.card not in game.player.cards:
            player_sprite.remove(sprite)
        sprite.flip('Front')
    
    card_positions(player_sprite)

def create_deck(deck_sprite, game):
    existing_cards = [sprite.card for sprite in deck_sprite]
    x = DECK_X
    for card in game.deck.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, x, DECK_Y)
            deck_sprite.add(new_sprite)
    
    for sprite in deck_sprite:
        if sprite.card not in game.deck.cards:
            deck_sprite.remove(sprite)
        sprite.flip('Back')

def create_computer(computer_sprite, game):
    existing_cards = [sprite.card for sprite in computer_sprite]
    for card in game.computer.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, 0, COMPUTER_Y)
            computer_sprite.add(new_sprite)

    for sprite in computer_sprite:
        if sprite.card not in game.computer.cards:
            computer_sprite.remove(sprite)
        if game.phase != 'Phase_Declare':
            sprite.flip('Back')

    card_positions(computer_sprite)

def create_discard(discard_sprite, game):
    existing_cards = [sprite.card for sprite in discard_sprite]
    x = DISCARD_X
    for card in game.discard.cards:
        if card not in existing_cards:
            new_sprite = CardSprite(card, x, DISCARD_Y)
            discard_sprite.add(new_sprite)
        
    for sprite in discard_sprite:
        if sprite.card not in game.discard.cards:
            discard_sprite.remove(sprite)
        sprite.flip('Front')

def display_score(game, button_sprite, overall_computer_score, overall_player_score, font, lost = False):
    create_box(1575, 550, 0.8)

    overall_computer_score += game.computer_score()
    overall_player_score += game.player_score()

    if not lost:
        text = font.render(f'Computer Score: {overall_computer_score}\nYour Score: {overall_player_score}', True, (0, 0, 0))
    else:
        text = font.render(f'Computer Score: {overall_computer_score}\nYour Score: {overall_player_score}\nGame Over', True, (0, 0, 0))
    GAME_SCREEN.blit(text, (1400, 375))

    play_button = ButtonSprite(1575, 600, 'play')
    button_sprite.add(play_button)
    menu_button = ButtonSprite(1575, 700, 'menu')
    button_sprite.add(menu_button)

    button_sprite.draw(GAME_SCREEN)

def card_positions(current_sprite):
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
    
    for sprite in current_sprite:
        sprite.rect.centerx = X
        X += 150

def update_scores(game, overall_computer_score, overall_player_score):
    overall_computer_score += game.computer_score()
    overall_player_score += game.player_score()

    if overall_player_score >= 100:
        overall_player_score = 0
        overall_computer_score = 0

    return overall_computer_score, overall_player_score

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

def create_background():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(script_dir, 'assets', 'images', 'ui', 'background.png')
    background_image = pygame.image.load(background_path).convert_alpha()
    background_image = pygame.transform.scale(background_image, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    
    return background_image

def create_title():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    title_path = os.path.join(script_dir, 'assets', 'images', 'ui', 'title.png')
    title_image = pygame.image.load(title_path).convert_alpha()

    title_rect = title_image.get_rect()
    title_rect.center = (VIRTUAL_WIDTH / 2, 300)

    return title_image, title_rect

def create_box(X, Y, scale):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    box_path = os.path.join(script_dir, 'assets', 'images', 'ui', 'box.png')
    box_image = pygame.image.load(box_path).convert_alpha()
    box_image = pygame.transform.scale_by(box_image, scale)

    box_rect = box_image.get_rect()
    box_rect.center = (X, Y)

    GAME_SCREEN.blit(box_image, box_rect)

def create_fonts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, 'assets', 'fonts', 'Handjet', 'static', 'Handjet-Regular.ttf')
    small_font = pygame.font.Font(font_path, 25)
    large_font = pygame.font.Font(font_path, 50)

    return large_font, small_font

def print_deck_size(game, font):
    size = game.deck.size()
    text = font.render(f'{size}/52', True, (255, 255, 255))
    GAME_SCREEN.blit(text, (535, VIRTUAL_HEIGHT / 2))

def print_highscore(font):
    highscore = read_value('highscore', 0)
    text = font.render(f'Highscore: {highscore}', True, (255, 255, 255))
    GAME_SCREEN.blit(text, (1635, 0))

def create_rules(font):
    create_box(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2, 1.75)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'src', 'rules.txt')
    with open(file_path, "r", encoding = "utf-8") as file:
        rules = file.read()
    text = font.render(rules, True, (0, 0, 0))
    text_rect = text.get_rect(center=(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2))
    GAME_SCREEN.blit(text, text_rect)

def virtual_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = mouse_x * VIRTUAL_WIDTH / SCREEN.get_width()
    mouse_y = mouse_y * VIRTUAL_HEIGHT / SCREEN.get_height()
    return mouse_x, mouse_y

def play_sound(name, SOUND, MUSIC, volume = 1.0):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, 'assets', 'audio', f'{name}.mp3')
    if name == 'music':
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        if not MUSIC:
            pygame.mixer.music.pause()
    elif name != 'music' and SOUND:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play()

def create_credits(font):
    create_box(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2, 1.6)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'src', 'credits.txt')
    with open(file_path, "r", encoding = "utf-8") as file:
        credits = file.read()
    text = font.render(credits, True, (0, 0, 0))
    text_rect = text.get_rect(center=(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2))
    GAME_SCREEN.blit(text, text_rect)



def main():
    state = "menu"
    running = True
    background = create_background()
    highscore = read_value('highscore', 0)
    large_font, small_font = create_fonts()
    SOUND = read_value('sound', True)
    MUSIC = read_value('music', True)
    play_sound('music', SOUND, MUSIC)

    while running:
        if state == "menu":
            state = menu(background, large_font, SOUND, MUSIC)
        elif state == 'rules':
            state = rules(background, small_font, SOUND, MUSIC)
        elif state == "game":
            state = game(background, highscore, large_font, small_font, SOUND, MUSIC)
        elif state == 'options':
            state, SOUND, MUSIC = options(background, SOUND, MUSIC)
        elif state == "credits":
            state = credits(background, small_font, SOUND, MUSIC)
        elif state == "quit":
            running = False

    write_value('sound', SOUND)
    write_value('music', MUSIC)
    pygame.quit()

def menu(background, large_font, SOUND, MUSIC):
    clock = pygame.time.Clock()
    run = True

    button_sprite = pygame.sprite.Group()
    title_sprite, title_position = create_title()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'play':
                        play_sound('button', SOUND, MUSIC)
                        return 'game'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'rules':
                        play_sound('button', SOUND, MUSIC)
                        return 'rules'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'credits':
                        play_sound('button', SOUND, MUSIC)
                        return 'credits'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'options':
                        play_sound('button', SOUND, MUSIC)
                        return 'options'
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'quit':
                        play_sound('button', SOUND, MUSIC)
                        return 'quit'



        GAME_SCREEN.blit(background, (0, 0))
        GAME_SCREEN.blit(title_sprite, title_position)
        create_menu_buttons(button_sprite)
        button_sprite.draw(GAME_SCREEN)
        print_highscore(large_font)

        render_to_screen()
        pygame.display.update()
        clock.tick(FPS)
            
def game(background, highscore, large_font, small_font, SOUND, MUSIC):
    clock = pygame.time.Clock()
    run = True
    game = Game()
    selected_cards = []
    start_time = 0
    overall_player_score = 0
    overall_computer_score = 0



    button_sprite = pygame.sprite.Group()
    deck_sprite = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    computer_sprite = pygame.sprite.Group()
    discard_sprite = pygame.sprite.Group()



    while run:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            mouse_x, mouse_y = virtual_mouse()
            for sprite in player_sprite:
                if sprite.rect.collidepoint(mouse_x, mouse_y):
                    sprite.hovering(True)
                else:
                    sprite.hovering(False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.phase == 'Phase_Player':
                    for sprite in button_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'declare':
                            play_sound('button', SOUND, MUSIC)
                            game.player_declare()
                            game.phase = 'Phase_Declare'
                            break
                        
                    for sprite in player_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            play_sound('card', SOUND, MUSIC)
                            sprite.update_on_click(selected_cards)

                    for sprite in deck_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            chosen_cards = game.player_select_cards(selected_cards)
                            if chosen_cards == None:
                                for sprite in player_sprite:
                                    sprite.revert(PLAYER_Y)
                                play_sound('card', SOUND, MUSIC, 0.2)
                                selected_cards.clear()
                            else:
                                game.player_draw()
                                game.player_drop(selected_cards)
                                selected_cards.clear()
                                play_sound('card', SOUND, MUSIC)
                                game.phase = 'Phase_Computer'
                                start_time = current_time
                                break
                    
                    for sprite in discard_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            chosen_cards = game.player_select_cards(selected_cards)
                            if chosen_cards == None:
                                for sprite in player_sprite:
                                    sprite.revert(PLAYER_Y)
                                selected_cards.clear()
                            else:   
                                game.player_pickup()
                                game.player_drop(selected_cards)
                                selected_cards.clear()
                                play_sound('card', SOUND, MUSIC)
                                game.phase = 'Phase_Computer'
                                start_time = current_time
                                break



                elif game.phase == 'Phase_Declare':
                    for sprite in button_sprite:
                        if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'menu':
                            play_sound('button', SOUND, MUSIC)
                            return 'menu'

                        elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'play':
                            play_sound('button', SOUND, MUSIC, 0.2)
                            button_sprite.empty()

                            overall_computer_score, overall_player_score = update_scores(game, overall_computer_score, overall_player_score)

                            selected_cards.clear()
                            game = Game()



        if game.phase == 'Phase_Computer' and current_time - start_time >= 1000:
            number = random.randint(10, 15)
            if game.computer.points() <= number:
                game.computer.declare(game.player)
                game.phase = 'Phase_Declare'
            else:
                game.computer_turn()
                play_sound('card', SOUND, MUSIC)
                game.phase = 'Phase_Player'



        GAME_SCREEN.blit(background, (0, 0))
        create_game_buttons(button_sprite)
        create_deck(deck_sprite, game)
        create_player(player_sprite, game)
        create_computer(computer_sprite, game)
        create_discard(discard_sprite, game)

        button_sprite.draw(GAME_SCREEN)
        deck_sprite.draw(GAME_SCREEN)
        player_sprite.draw(GAME_SCREEN)
        computer_sprite.draw(GAME_SCREEN)
        discard_sprite.draw(GAME_SCREEN)
        print_deck_size(game, small_font)
        print_highscore(large_font)

        if game.phase == 'Phase_Declare':
            if overall_player_score + game.player_score() >= 100:
                display_score(game, button_sprite, overall_computer_score, overall_player_score, large_font, True)
                if overall_computer_score + game.computer_score() > highscore:
                    write_value('highscore', overall_computer_score + game.computer_score())
            else:
                display_score(game, button_sprite, overall_computer_score, overall_player_score, large_font)

            for sprite in computer_sprite:
                sprite.flip('Front')

            for sprite in player_sprite:
                sprite.revert(PLAYER_Y)


        render_to_screen()
        pygame.display.update()
        clock.tick(FPS)

def rules(background, small_font, SOUND, MUSIC):
    clock = pygame.time.Clock()
    run = True

    button_sprite = pygame.sprite.GroupSingle()
    back_button = ButtonSprite(100, 970, 'back')
    button_sprite.add(back_button)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        play_sound('button', SOUND, MUSIC)
                        return 'menu'

        GAME_SCREEN.blit(background, (0, 0))
        button_sprite.draw(GAME_SCREEN)
        create_rules(small_font)

        render_to_screen()
        pygame.display.update()
        clock.tick(FPS)

def credits(background, small_font, SOUND, MUSIC):
    clock = pygame.time.Clock()
    run = True

    button_sprite = pygame.sprite.GroupSingle()
    back_button = ButtonSprite(100, 970, 'back')
    button_sprite.add(back_button)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        play_sound('button', SOUND, MUSIC)
                        return 'menu'

        GAME_SCREEN.blit(background, (0, 0))
        button_sprite.draw(GAME_SCREEN)
        create_credits(small_font)

        render_to_screen()
        pygame.display.update()
        clock.tick(FPS)

def options(background, SOUND, MUSIC):
    clock = pygame.time.Clock()
    run = True

    button_sprite = pygame.sprite.Group()
    back_button = ButtonSprite(100, 970, 'back')
    button_sprite.add(back_button)
    if SOUND:
        sound_button = ButtonSprite((VIRTUAL_WIDTH / 2) - 150, VIRTUAL_HEIGHT / 2, 'sound', 0.75, False)
    else:
        sound_button = ButtonSprite((VIRTUAL_WIDTH / 2) - 150, VIRTUAL_HEIGHT / 2, 'sound', 0.75, True)
    button_sprite.add(sound_button)
    if MUSIC:
        music_button = ButtonSprite((VIRTUAL_WIDTH / 2) + 150, VIRTUAL_HEIGHT / 2, 'music', 0.75, False)
    else:
        music_button = ButtonSprite((VIRTUAL_WIDTH / 2) + 150, VIRTUAL_HEIGHT / 2, 'music', 0.75, True)
    button_sprite.add(music_button)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = virtual_mouse()
                for sprite in button_sprite:
                    if sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'back':
                        play_sound('button', SOUND, MUSIC)
                        return 'menu', SOUND, MUSIC
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'music':
                        play_sound('button', SOUND, MUSIC)
                        sprite.mute()
                        if sprite.click == True:
                            MUSIC = False
                            pygame.mixer.music.pause()
                        else:
                            MUSIC = True
                            pygame.mixer.music.unpause()
                    elif sprite.rect.collidepoint(mouse_x, mouse_y) and sprite.name == 'sound':
                        play_sound('button', SOUND, MUSIC)
                        sprite.mute()
                        if sprite.click == True:
                            SOUND = False
                        else:
                            SOUND = True
                        
        GAME_SCREEN.blit(background, (0, 0))
        create_box(VIRTUAL_WIDTH / 2, VIRTUAL_HEIGHT / 2, 1.0)
        button_sprite.draw(GAME_SCREEN)

        render_to_screen()
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()