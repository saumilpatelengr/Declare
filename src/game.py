from src.deck import Deck
from src.discard import Discard
from src.hand import Hand

class Game:
    def __init__(self):
        self._deck = Deck()
        self._discard = Discard(self._deck)
        self._player = Hand(self._deck)
        self._computer = Hand(self._deck)
        self._phase = 'Phase_Player'

    @property
    def phase(self):
        return self._phase
    
    @phase.setter
    def phase(self, phase):
        self._phase = phase

    @property
    def deck(self):
        return self._deck
    
    @property
    def discard(self):
        return self._discard
    
    @property
    def player(self):
        return self._player

    @property
    def computer(self):
        return self._computer
    
    def player_declare(self):
        self._player.declare(self._computer)

    def player_select_cards(self, selected_cards):
        return self._player.select(selected_cards)

    def player_draw(self):
        self._player.draw(self._deck)

    def player_pickup(self):
        self._player.pickup(self._discard)

    def player_drop(self, selected_cards):
        self._player.drop(self._discard, selected_cards)

    def player_score(self):
        return self._player.score

    def computer_score(self):
        return self._computer.score
    
    def computer_turn(self):
        selected_cards = []
        if self._computer.number_of_duplicates() > 0:
            best_duplicate = self._computer.highest_value_duplicate(self._discard)
            high_card = self._computer.high_card(self._discard)
            selected_cards = self._computer.compare(best_duplicate, high_card)
        else:
            selected_cards.append(self._computer.high_card(self._discard))

        if self._deck.size() == 0:
            self._computer.pickup(self._discard)
        elif self._discard.top().value() < 5 or self._computer.pickup_creates_duplicate(self._discard):
            self._computer.pickup(self._discard)
        else:
            self._computer.draw(self._deck)

        self._computer.drop(self._discard, selected_cards)