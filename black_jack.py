import random
suits = ('Hearts','Diamonds','Clubs','Spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

#CONTROL WHILE LOOP LATER IN GAME LOGIC
playing = True

#DEFINE THE CARDS
class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit
    
#DEFINE THE DECK
class Deck():
    def __init__(self):
        self.deck = [] #START WITH AN EMPTY LIST
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+card.__str__()
        return 'The deck has: '+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
class Hand():

    def __init__(self):
        self.cards = [] #START WITH AN EMPTY LIST
        self.value = 0  #START WITH A VALUE OF 0
        self.aces = 0   #ADD AN ATTRIBUTE TO KEEP TRACK OF ACES

    def add_card(self,card):
        ##CARD PASSED IN FROM Deck.deal() --> SINGLE Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        #TRACK ACES
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):

        #CHECK IF VALUE OVER 21
        #IF TRUE AND STILL HAVE AN ACE CHANGE ACE TO BE 1 INSTEAD OF 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
class Chips():

    def __init__(self):
        self.total = 100 ##SET TO A DEFAULT VALUE
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet
        
def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry please provide an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry you do not have enough chips! You have: {}'.format(chips.total))
            else:
                break
            
def hit(deck,hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing ##TO CONTROL COMING WHILE LOOP

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck,hand)
        
        elif x[0].lower() == 's':
            print("Player stands, dealer's turn")
            playing = False

        else:
            print('Sorry, I did not understand that, please enter h or s')
            continue
        break
    
def show_some(player,dealer):
    #SHOW ONLY ONE OF THE DEALER'S CARDS
    print("\n Dealer's Hand: ")
    print('First card hidden!')
    print(dealer.cards[1])
    
    #SHOW ALL(2 CARDS) OF THE PLAYER'S HAND/CARDS
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)
        
def show_all(player,dealer):
    #SHOW ALL OF THE DEALER'S CARDS AND CALCULATE AND DISPLAY VALUE OF DEALER'S HAND
    print("\n Dealer's Hand: ")
    for card in dealer.cards:
        print(card)
    print(f"The value of of Dealer's hand is: {dealer.value}")
    
    #SHOW ALL OF THE PLAYER'S CARDS AND CALCULATE AND DISPLAY VALUE OF PLAYER'S HAND
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)
    print(f"The value of of Player's hand is: {player.value}")
    
def player_busts(player,dealer,chips):
    print('Player Busts!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player Wins!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('Dealer Busts!')
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print('Dealer Wins!')
    chips.lose_bet()

def push(player,dealer):
    print('Player and Dealer tie! PUSH')
    
#GAME LOGIC
while True:
    #PRINT AN OPENING STATEMENT
    print('Welcome to Blackjack!')

    #CREATE & SHUFFLE THE DECK, DEAL TWO CARDS TO EACH PLAYER
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #SET UP THE PLAYER'S CHIPS
    player_chips = Chips()

    #PROMPT THE PLAYER FOR THEIR BET
    take_bet(player_chips)

    #SHOW CARDS(BUT KEEP ONE DEALER CARD HIDDEN)
    show_some(player_hand,dealer_hand)

    while playing:
        #PROMPT THE PLAYER TO HIT OR STAND
        hit_or_stand(deck,player_hand)

        #SHOW CARDS(BUT KEEP ONE DEALER CARD HIDDEN)
        show_some(player_hand,dealer_hand)

        #IF THE PLAYER'S HAND EXCEEDS 21, RUN PLAYER_BUSTS() AND BREAK OUT OF THE LOOP
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

        break

    #IF PLAYER HASN'T BUSTED, PLAY DEALER'S HAND UNTIL DEALER REACHES 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        #SHOW ALL THE CARDS
        show_all(player_hand,dealer_hand)

        #RUN DIFFERENT WINNING SCENARIOS
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)

    #INFORM THE PLAYER OF THEIR CHIP TOTAL
    print('\n Player total chips are at {}'.format(player_chips.total))

    #ASK TO PLAY AGAIN
    new_game = input('Would you like to play another hand? y/n ')

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thanks for playing!')
        break