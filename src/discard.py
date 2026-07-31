#discard.py: Contains the Discard class that dictates how the discard pile logic works for the game
#Discard class
class Discard:
    #Creates an empty discard pile
    def __init__(self):
        self._cards = []



    #Returns how many cards are in the discard pile
    def size(self):
        return len(self._cards)
    


    #Returns the Card object on the top of the discard pile
    def top(self):
        if len(self._cards) == 0:
            return None
        else:
            return self._cards[-1]
    

    
    #Returns the discard pile
    @property
    def cards(self):
        return self._cards