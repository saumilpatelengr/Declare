import random
from src.card import Card

class Deck:
    #Creates a standard deck of 52 playing cards using Card objects
    def __init__(self):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        self._cards = []
        for suit in suits:
            for rank in ranks:
                self._cards.append(Card(suit, rank))
        self.shuffle()

    #Shuffles the deck
    def shuffle(self):
        random.shuffle(self._cards)

    #Returns the numbers of cards in the deck
    def size(self):
        return len(self._cards)
    
    #Returns the deck
    @property
    def cards(self):
        return self._cards