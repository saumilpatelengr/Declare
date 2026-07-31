#game.py: Contains the Game class that combines the logic of the Deck, Discard, and Hand classes for the game
#Imports
from deck import Deck
from discard import Discard
from hand import Hand



#Game class
class Game:
    #Creates all initial items to play
    def __init__(self, player_size = 5, computer_size = 5):
        #Creates all the objects needed to play the game
        #'player_size' and 'computer_size' determine what the hand sizes are for the player and computer
        self._deck = Deck()
        self._discard = Discard()
        self._player = Hand(self._deck, player_size)
        self._computer = Hand(self._deck, computer_size)

        #Phase attribute to see what phase of the game it is currently
        self._phase = 'Phase_Player'

        #Previous phase attribute to keep track of the previous phase of the game when needed
        self._previous_phase = None



    #Allows phase attribute to be accessed outside of this class
    @property
    def phase(self):
        return self._phase
    


    #Allows phase attribute to be set outside of this class
    @phase.setter
    def phase(self, phase):
        self._phase = phase



    #Allows previous phase attribute to be accessed outside of this class
    @property
    def previous_phase(self):
        return self._previous_phase



    #Allows previous phase attribute to be set outside of this class
    @previous_phase.setter
    def previous_phase(self, previous_phase):
        self._previous_phase = previous_phase



    #Allows deck attribute to be accessed outside of this class
    @property
    def deck(self):
        return self._deck
    


    #Allows discard attribute to be accessed outside of this class
    @property
    def discard(self):
        return self._discard
    


    #Allows player attribute to be accessed outside of this class
    @property
    def player(self):
        return self._player



    #Allows computer attribute to be accessed outside of this class
    @property
    def computer(self):
        return self._computer
    


    #If the player wants to declare during their turn
    def player_declare(self):
        self._player.declare(self._computer)



    #Checks to see if all cards selected by the player are valid to drop or not
    def player_select_cards(self, selected_cards):
        return self._player.select(selected_cards)



    #Lets the player draw a card from the deck
    def player_draw(self):
        self._player.draw(self._deck)



    #Lets the player pickup the top card of the discard pile
    def player_pickup(self):
        self._player.pickup(self._discard)



    #Lets the player drop all the cards they selected onto the discard pile
    def player_drop(self, selected_cards):
        self._player.drop(self._discard, selected_cards)



    #Returns the total score of all cards added up in the player's hand
    def player_score(self):
        return self._player.score



    #Returns the total score of all cards added up in the computer's hand
    def computer_score(self):
        return self._computer.score
    


    #Allows the computer to take their turn
    def computer_turn(self):
        #If there are multiple cards of the same rank in the computer's hand, it will determine which group of duplicate rank cards
        #   have the highest total value when added together. Afterwards, it will determine the highest value single card in its 
        #   hand and compare its total value to the best group of duplicates. Whichever one has the higher value will be placed into
        #   selected_cards.
        #If there are no cards of the same rank in the computer's hand, it will add the highest value single card to selected_cards
        selected_cards = []
        if self._computer.number_of_duplicates() > 0:
            best_duplicate = self._computer.highest_value_duplicate(self._discard)
            high_card = self._computer.high_card(self._discard)
            selected_cards = self._computer.compare(best_duplicate, high_card)
        else:
            selected_cards.append(self._computer.high_card(self._discard))

        #If the deck has no more cards in it, the computer will pickup the card on top of the discard pile
        if self._deck.size() == 0:
            self._computer.pickup(self._discard)
        #If the top card of the discard pile has a value less than or equal to 5 OR the top card of the discard pile can create a 
        #   duplicate whose total value is greater than the highest single value card in the computer's hand, the computer will 
        #   pickup the card on top of the discard pile
        elif self._discard.top().value() <= 5 or self._computer.pickup_creates_duplicate(self._discard):
            self._computer.pickup(self._discard)
        #Otherwise, the computer will draw a card from the deck
        else:
            self._computer.draw(self._deck)

        #The computer will drop all the cards it selected into the top of the discard pile
        self._computer.drop(self._discard, selected_cards)