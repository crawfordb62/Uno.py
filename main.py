import random

class Card():
    def __init__(self, value, color):
        self.value = value
        self.color = color

class Player():
    def __init__(self, tag):
        self.tag = tag
        self.hand = []

WINNER = False
VALUES = ["skip","reverse","+2","wild","+4"]
COLORS = ["red","blue","green","yellow"]
TURN = 0
DIRECTION = 1
HANDLIM = 7
DECK = []
for color in range(4):
    for value in range(15):
        card = Card(value, color)
        DECK.append(card)
PILE = []
PLAYERS = []
for i in range(4):
    player = Player(i)
    PLAYERS.append(player)

def shuffle():
    global TURN, DIRECTION, HANDLIM, DECK, PILE, PLAYERS
    temp = []
    while len(DECK) > 0:
        card = random.choice(DECK)
        DECK.remove(card)
        temp.append(card)
    DECK = temp

def newgame():
    global TURN, DIRECTION, HANDLIM, DECK, PILE, PLAYERS
    shuffle()
    for i in range(HANDLIM):
        for player in PLAYERS:
            player.hand.append(DECK[0])
            DECK = DECK[1:]
    PILE = [DECK[0]]
    DECK = DECK[1:]
    TURN = 0
    DIRECTION = 1

def check(played, ontop):
    if played.value >= 13:
        return True
    elif played.value == ontop.value or played.color == ontop.color:
        return True
    return False

def checkturn():
    global TURN, PLAYERS
    limit = len(PLAYERS) - 1
    if TURN > limit:
        TURN = 0
    elif TURN < 0:
        TURN = limit

def turn():
    global TURN, DIRECTION, HANDLIM, DECK, PILE, PLAYERS
    player = PLAYERS[TURN]
    print("--------------------")
    print("Player "+str(player.tag)+"'s turn")
    card = PILE[-1]
    color = card.color
    value = card.value
    values = ["skip","reverse","+2","wild","+4"]
    colors = ["red","blue","green","yellow"]
    if value > 9:
        value = values[value-10]
    else:
        value = str(value)
    color = colors[color]
    print("Current card: "+value+" "+color)
    i = 0
    print("Current hand:")
    for card in player.hand:
        color = card.color
        value = card.value
        values = ["skip","reverse","+2","wild","+4"]
        colors = ["red","blue","green","yellow"]
        if value > 9:
            value = values[value-10]
        else:
            value = str(value)
        color = colors[color]
        print(str(i)+": "+value+" "+color)
        i += 1
    print(str(i)+": Draw a card")
    choice = input("What card do you choose?")
    try:
        choice = int(choice)
    except:
        print("**************")
        print("Invalid choice")
        print("**************")
        turn()
    if choice < len(player.hand) and choice >= 0:
        if player.hand[choice].value < 13:
            if check(PILE[-1],player.hand[choice]):
                playcard(player.hand[choice])
            else:
                print("**************")
                print("Invalid choice")
                print("**************")
                turn()
        else:
            playcard(player.hand[choice])
    elif choice == len(player.hand):
        player.hand.append(DECK[0])
        DECK = DECK[1:]
    else:
        print("**************")
        print("Invalid choice")
        print("**************")
        turn()

    TURN += DIRECTION
    checkturn()

    if len(PILE) >= len(DECK):
        DECK = DECK + PILE[:-1]
        shuffle()
        PILE = [PILE[-1]]   

def playcard(card):
    global TURN, DIRECTION, HANDLIM, DECK, PILE, PLAYERS, WINNER
    player = PLAYERS[TURN]
    temp = player.hand
    temp.remove(card)
    if len(temp) == 1:
        print("UNO! - Player {}".format(player.tag))
    elif len(temp) == 0:
        print("Winner! Player {}".format(player.tag))
        WINNER = True
    if card.value >= 10:
        if card.value == 10:
            TURN += DIRECTION
            checkturn()
        elif card.value == 11:
            DIRECTION *= -1
            if len(PLAYERS) == 2:
                TURN += DIRECTION
                checkturn()
        elif card.value == 12:
            TURN += DIRECTION
            checkturn()
            player2 = PLAYERS[TURN]
            for i in range(2):
                player2.hand.append(DECK[0])
                DECK = DECK[1:]
        elif card.value == 13:
            newcolor = input("What color do you want?")
            i = 0
            for color in COLORS:
                if color == newcolor:
                    newcolor = i
                    break
                i += 1
            if i == len(COLORS):
                newcolor = 0
            card.color = newcolor
        elif card.value == 14:
            TURN += DIRECTION
            checkturn()
            player2 = PLAYERS[TURN]
            for i in range(4):
                player2.hand.append(DECK[0])
                DECK = DECK[1:]
            newcolor = input("What color do you want?")
            i = 0
            for color in COLORS:
                if color == newcolor:
                    newcolor = i
                    break
                i += 1
            card.color = newcolor
    PILE.append(card)

newgame()

while WINNER == False:
    turn()
