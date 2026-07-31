#hand.py: Contains the Hand class that dictates the card hand's logic for the game
#Imports
from collections import Counter
from card import Card



#Hand class
class Hand:
    #Creates a hand of cards drawn from the deck
    #Hand size is determined by the size parameter
    def __init__(self, deck, size):
        self._score = 0
        self._cards = []
        for i in range(size):
            self._cards.append(deck.cards.pop())



    #Draws a card from the deck
    def draw(self, deck):
        self._cards.append(deck.cards.pop())



    #Picks up a card from the discard pile
    def pickup(self, discard):
        self._cards.append(discard.cards.pop())



    #Returns the total numbers of points in the hand
    def points(self):
        total = 0
        for card in self._cards:
            total += card.value()
        return total



    #Asks the player to select cards from their hand to drop
    #Returns a list of Card objects (selected cards)
    def select(self, selected_cards):
        if len(selected_cards) == 0:
            return None

        #If multiple existing cards are chosen
        #Checks to see if all the cards have the same rank
        if len(selected_cards) > 1:
            check = selected_cards[0].rank
            for i in range(len(selected_cards)):
                if selected_cards[i].rank != check:
                    return None

        #Returns a list of Card objects (selected cards)
        return selected_cards
    


    #Drops all the cards from the selected_cards list
    #Adds all dropped cards to discard pile
    def drop(self, discard, selected_cards):
        for i in range(len(selected_cards)):
            self._cards.remove(selected_cards[i])
            discard.cards.append(selected_cards[i])
    


    #If player/computer thinks they have the lowest number of points, they can declare their hand
    #If successful, the player/computer that declared gets 0 points while the other player/computer 
    #   gets the combined total of their hand
    #If unsuccessful (same number of points or greater than other player/computer), the player/computer 
    #   that declared gets the total of their hand and the other player/computer's hand. The other 
    #   player/computer gets -10 points
    def declare(self, other):
        if self.points() < other.points():
            other.score += other.points()
        else:
            other.score -= 10
            self._score += self.points()
            self._score += other.points()



    #Allows cards attribute to be accessed outside of this class
    @property
    def cards(self):
        return self._cards
    


    #Allows score attribute to be accessed outside of this class
    @property
    def score(self):
        return self._score
    


    #Allows score attribute to be set outside of this class
    @score.setter
    def score(self, score):
        self._score = score



    #----------Computer-Specific Methods----------
    #Returns how many pairs of duplicates exist in a hand
    def number_of_duplicates(self):
        ranks = []
        for card in self._cards:
            ranks.append(card.rank)
        counts = Counter(ranks)
        duplicates = []
        for rank, count in counts.items():
            if count > 1:
                duplicates.append(rank)
        return len(duplicates)
    


    #Returns the highest value Card object in the hand
    def high_card(self, discard):
        #Placeholder so Card objects are compared
        max = Card('Spades', '0')

        for card in self._cards:
            #Edge Case: If the high card has the same rank as the top of the discard pile, it is better
            #       to pickup that card to create a pair that can be dropped on the next turn. Skips this card
            if card.rank == discard.top().rank:
                continue

            if card.value() > max.value():
                max = card

        return max
    


    #Finds the highest value duplicate if multiple of them exist in the hand
    #Returns a list of Card objects (best_duplicate)
    def highest_value_duplicate(self, discard):
        #Creates a dictionary (counts) that holds how many times a rank shows up in the hand
        ranks = []
        for card in self._cards:
            ranks.append(card.rank)
        counts = Counter(ranks)

        #For each pair in the dictionary (counts), finds the total number of points if dropped
        #Example: '10' : 2 -> value of 20 if two 10's are dropped the next turn
        #Adds the total number of points for each pair into the values list
        values = []
        for rank, count in counts.items():
            #Edge Case: If the duplicate being looked at has the same rank as the top of the discard pile,
            #       it is better to pickup that card to add to the duplicate so that it can be dropped on 
            #       the next turn. Skips the duplicate that holds this condition
            if count > 1 and rank != discard.top().rank:
                if rank == 'K' or rank == 'Q' or rank == 'J':
                    values.append(10 * count)
                elif rank == 'A':
                    values.append(count)
                else:
                    values.append(int(rank) * count)
    
        #Finds the maximum total value from the values list
        high = max(values, default = 0)
        #Because of the edge case above, if that was the only duplicate in the hand, then values would be empty
        #Returns an empty list if that holds true
        if high == 0:
            return []

        #Checks each pair in the dictionary (counts) to see which one gave the highest total value 
        #Once the rank that gave the highest total value is found (best_rank), the loop breaks
        for rank, count in counts.items():
            #Edge Case: If the duplicate being looked at has the same rank as the top of the discard pile,
            #       it is better to pickup that card to add to the duplicate so that it can be dropped on 
            #       the next turn. Skips the duplicate that holds this condition
            if count > 1 and rank != discard.top().rank:
                if rank == 'K' or rank == 'Q' or rank == 'J':
                    if 10 * count == high:
                        best_rank = rank
                        break
                elif rank == 'A':
                    if count == high:
                        best_rank = rank
                        break
                else:
                    if int(rank) * count == high:
                        best_rank = rank
                        break

        #Using the best_rank, any card whose rank matches the best_rank from the hand is added to best_duplicate
        best_duplicate = []
        for card in self._cards:
            if card.rank == best_rank:
                best_duplicate.append(card)

        #Returns a list of Card objects (best_duplicate)
        return best_duplicate
    


    #Compares the best duplicate in the hand with the high card to see which one has a greater total value
    #Returns a list of Card objects (the best option to drop on the next turn)
    def compare(self, duplicates, high_card):
        cards_to_drop = []

        #Edge Case: If the highest_value_duplicate method returned an empty list that is passed into this 
        #       method, then there is nothing to compare the high card to. Therefore, the high card is the 
        #       best option and is returned
        if len(duplicates) == 0:
            cards_to_drop.append(high_card)
            return cards_to_drop

        #Gets the total value for all the duplicates added up
        duplicate_value = len(duplicates) * duplicates[0].value()

        #Compares between the 2 to see which one has a higher value and return those cards
        if duplicate_value < high_card.value():
            cards_to_drop.append(high_card)
            return cards_to_drop
        else:
            return duplicates



    #Checks to see if picking up the top card of the discard pile creates or adds to a duplicate in the hand
    #If it does, returns true; otherwise, returns false
    def pickup_creates_duplicate(self, discard):
        #Gets the high card in the hand and the value of the top card of the discard pile
        high_card = self.high_card(discard)
        total = discard.top().value()

        #Checks all cards to see if they match the top card of the discard pile
        #If so, card's value is added to total and matching is incremented
        matching = 0
        for card in self._cards:
            if card.rank == discard.top().rank:
                total += card.value()
                matching += 1
        
        #Checks if there are any matching cards and if the total value of the matching cards is greater than the high card's value or not
        if matching > 0:
            if total >= high_card.value():
                return True
            else:
                return False
        else:
            return False