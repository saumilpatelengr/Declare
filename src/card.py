#Card class
class Card:
    #Creates a standard playing card with its rank and suit
    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank



    #Compares if 2 cards are the exact same
    def __eq__(self, other):
        return self._suit == other.suit and self._rank == other.rank
    


    #Checks the rank of a card and returns the point value of that card
    def value(self):
        if self._rank == 'K' or self._rank == 'Q' or self._rank == 'J':
            return 10
        elif self._rank == 'A':
            return 1
        else:
            return int(self._rank)



    #Allows rank attribute to be accessed outside of this class
    @property
    def rank(self):
        return self._rank
    

    
    #Allows suit attribute to be accessed outside of this class
    @property
    def suit(self):
        return self._suit