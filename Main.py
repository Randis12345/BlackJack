import os
from random import randint
from time import sleep

termsize = os.get_terminal_size()

CARDWIDTH = 8
CARDHEIGHT = 6
CARDSPACING = 1
WAITIME = 2

def printmid(text,heightwise = False):
    if heightwise:
        hpadding = (termsize.lines - text.count("\n") - 1)//2
        if hpadding <0: hpadding = 0
        print(hpadding*"\n",end="")

    if "\n" in text:
        for segment in text.split("\n"): printmid(segment)
        return

    padding = (termsize.columns - len(text))//2
    if padding < 0: padding = 0
    print(" "*padding+text)

def hit():
    ind = randint(0,len(cards)-1)
    cardval = cards[ind] 
    cards.pop(ind)
    return cardval

def cardstotal(selcards):
    total = 0
    aces = 0
    for card in selcards:
        if card in ["J","Q","K"]:
            total+=10
        elif card == "A":
            total+=1
            aces+=1
        else:
            total+=card
    while total <= 11 and aces > 0:
        aces-=1
        total+=10
    return total
    

def cardstext(selcards):
    text = ""
    for i in range(len(selcards)):
        if i: text+=" "*(CARDSPACING+2)
        text+= "_"*CARDWIDTH
    text+="\n"
    for j in range(CARDHEIGHT):
        for i in range(len(selcards)*2):
            if i: 
                if i%2 == 1:
                    if j == 0 or j == CARDHEIGHT-1:
                        if selcards[i//2] != 10: text+=" " 
                        text+=str(selcards[i//2])
                        text+=(CARDWIDTH- 4)*" "
                        text+=str(selcards[i//2])
                        if selcards[i//2] != 10: text+=" " 
                    else:
                        text+=" "*(CARDWIDTH)
                else:
                    text+=" "*(CARDSPACING)
            text+= "|"
        text+="\n"
    
    for i in range(len(selcards)):
        if i: text+=" "*(CARDSPACING+2)
        text+= "‾"*CARDWIDTH
    
    text+="\n"
    return text

def updatescreen(win=-2):
    os.system("cls" if os.name == "nt" else "clear")
    global termsize

    termsize = os.get_terminal_size()
    text = "Dealer\n"
    if win>=-1:
        text+=cardstext(dealercards)
    else:
        text+=cardstext(["@"]+dealercards[1:])
    text+= "Player\n"
    text+=cardstext(playercards)
    if win>-1:
        text+=["you lose","tie","you win"][win]
        text+= "\n"+str(playernum)+"-"+str(dealernum)

    printmid(text,True)

    

cardset = []
for t in [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]:
    cardset+=[t]*4
cards = cardset



while True:
    cards = cardset
    dealercards = [hit(),hit()]
    playercards = [hit(),hit()]
    
    playernum = cardstotal(playercards)
    while playernum<=21:
        updatescreen()
        if input() == "h":
            playercards.append(hit())
            playernum = cardstotal(playercards)
        else:   
            break
    
    updatescreen(-1)
    dealernum = cardstotal(dealercards)
    while playernum <= 21 and dealernum < playernum:
        sleep(WAITIME)
        dealercards.append(hit())
        dealernum = cardstotal(dealercards)
        updatescreen(-1)
        

    if (playernum > 21 and dealernum > 21) or playernum == dealernum:
        updatescreen(1)
    elif (playernum > 21 or playernum < dealernum) and dealernum <= 21:
        updatescreen(0)
    elif playernum > dealernum or dealernum > 21:
        updatescreen(2)
    input()



