#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
from collections import Counter

class Card( object ):
  def __init__(self, name, value, suit, symbol): # this is a represent function which will help assign the cards with name,value, suits and symbol
    self.value = value
    self.suit = suit
    self.name = name
    self.symbol = symbol
    self.showing = False

  def __repr__(self): # __repr__() function which helps in representing in the Cards
    if self.showing:
      return self.symbol
    else:
      return "Card"

class Deck(object):
  def shuffle(self, times=1 ): # this function uses random.shuffle to help shuffle the deck
    random.shuffle(self.cards)
    print("Deck Shuffled")

  def deal(self): # removes a card from top of the deck
    return self.cards.pop(0)

class StandardDeck(Deck):
  def __init__(self):
    self.cards = []
    suits = {"Hearts":"♡", "Spades":"♠", "Diamonds":"♢", "Clubs":"♣"} # using set to assign the symbols to suit
    values = {"Two":2,   # assigning values using set
              "Three":3,
              "Four":4,
              "Five":5,
              "Six":6,
              "Seven":7,
              "Eight":8,
              "Nine":9,
              "Ten":10,
              "Jack":11,
              "Queen":12,
              "King":13,
              "Ace":14 }

    for name in values: # this for loop is to assign the symbols so it is better read and understand (ie. [3♢, A♢, Q♣, 5♡, K♢])
      for suit in suits:
        symbolIcon = suits[suit]
        if values[name] < 11:
          symbol = str(values[name])+symbolIcon
        else:
          symbol = name[0]+symbolIcon
        self.cards.append( Card(name, values[name], suit, symbol) )

  def __repr__(self):
    return "Standard deck of cards:{0} remaining".format(len(self.cards))

class Player(object):
  def __init__(self):
    self.cards = []

  def cardCount(self):    # this funxtion counts the number of cards a player has 
    return len(self.cards)

  def addCard(self, card): # function to add cards to the player
    self.cards.append(card)

class PokerScorer(object):
  def __init__(self, cards):
    # Number of cards
    if not len(cards) == 5:
      return "Error: Wrong number of cards"

    self.cards = cards

  def flush(self): # flush function which checks all of the cards of the same suit
    suits = [card.suit for card in self.cards] # using list comprehension we take only the suits of the cards a player has 
    if len( set(suits) ) == 1: # since set() does not allow duplicate values we check if the lenght of the suit is 1, if it is 1 it means all of the cards belong to a single suit, hence a flush
      return True
    return False

  def straight(self): # straight in poker is when all the cards a sequential (ie. 1,2,3,4,5 or 10,J,Q,K,A)
    values = [card.value for card in self.cards] # using list comprehension we take all the values of the cards, here the suit does not matter.
    values.sort() # once we have all the values we sort it using sort() function

    if not len( set(values)) == 5: # basic error checking
      return False 

    if values[4] == 14 and values[0] == 2 and values[1] == 3 and values[2] == 4 and values[3] == 5: # this is condition is an exception since Ace can also be treated as 1 in poker
      return 5 # returning the highest value card

    else: # this else condition checks for the next cards in the values[] list
      if not values[0] + 1 == values[1]: return False 
      if not values[1] + 1 == values[2]: return False
      if not values[2] + 1 == values[3]: return False
      if not values[3] + 1 == values[4]: return False

    return values[4]

  def highCard(self): # self explanatory checks which card is the highest 
    values = [card.value for card in self.cards]
    highCard = None
    for card in self.cards:
      if highCard is None:
        highCard = card
      elif highCard.value < card.value: 
        highCard=card

    return highCard

  def highestCount(self):# self explanatory checks which value has the highest count
    count = 0
    values = [card.value for card in self.cards]
    for value in values:
      if values.count(value) > count:
        count = values.count(value)

    return count

  def pairs(self): # checks to see if there are 2 pairs (ie. 9♣, 9♢, 6♣, 6♢)
    pairs = []
    values = [card.value for card in self.cards]
    for value in values:
      if values.count(value) == 2 and value not in pairs:
        pairs.append(value)

    return pairs
        
  def fourKind(self):# checks to see if there are 4 of a kind (9♣, 9♢, 9♡, 9♠️)
    values = [card.value for card in self.cards]
    for value in values:
      if values.count(value) == 4:
        return True

  def fullHouse(self): # full house means (ie. 9♣, 9♢, 10♡, 10♠️ , 10♣)
    two = False 
    three = False
    
    values = [card.value for card in self.cards]
    result=Counter(values)
    check = list(result.values())
    if check.count(2) == 1: # checks if there are any 2 values which are same
      two = True
    if check.count(3) == 1: # checks if there are any 3 values which are same
      three = True

    if two and three: # if both are true its a Full House
      return True

    return False

def main():
  player = Player()

  # Intial Amount
  points = 100

  # Cost per hand
  handCost = 5

  end = False
  while not end:
    print("********* NEW ROUND ***********")
    print( "You have {0} points".format(points) ) #how many points a player has 
    print("--------------------")
    points-=5 #each round costs 5 points

    ## Hand Loop
    deck = StandardDeck()
    deck.shuffle()

    # Deal Out
    for i in range(5): #dealing out 5 cards
      player.addCard(deck.deal())

    # fullHouse=[Card("Ace",14,"Diamonds","A♢"),Card("Ace",14,"Spades","A♠"),Card("Ace",14,"Clubs","A♣"),Card("Seven",7,"Diamonds","7♢") ,Card("Seven",7,"Clubs","7♣")]
    # player.cards=fullHouse

    # Make them visible
    for card in player.cards:
      card.showing = True
    print("Your Cards")
    print(player.cards)
    print("--------------------")
    validInput = False
    while not validInput:
      print("Which cards do you want to discard? ( eg. 1, 2, 3 )")
      print("Just hit return to hold all, type exit to quit")
      print("--------------------")
      inputStr = input()

      if points == 0 or points >= 2500 or inputStr == "exit" :
        if(points == 0 ):
          print("Sorry, you do not have any more points to continue the game. Please start a new game!")
        if(points>=2500):
          print("Congratulations you won 2500 points !!!")
        if inputStr == "exit":
          print("Huh! You are a quitter...")
        end=True
        break

      try:
        inputList = [int(inp.strip()) for inp in inputStr.split(",") if inp]
        for inp in inputList:
          if inp > 6:
            continue 
          if inp < 1:
            continue 

        for inp in inputList:
          player.cards[inp-1] = deck.deal()
          player.cards[inp-1].showing = True

        validInput = True

        print("These were you new cards...")
        print(player.cards)
        print("--------------------")
      except:
        print("Input Error: use commas to separated the cards you want to hold")
    
    #Score
    score = PokerScorer(player.cards)
    straight = score.straight()
    flush = score.flush()
    highestCount = score.highestCount()
    pairs = score.pairs()

    # Royal flush
    if straight and flush and straight == 14:
      print("Royal Flush!!!")
      print("+2000")
      points += 2000

    # Straight flush
    elif straight and flush:
      print("Straight Flush!")
      print("+250")
      points += 250

    # 4 of a kind
    elif score.fourKind():
      print("Four of a kind!")
      print("+125")
      points += 125

    # Full House
    elif score.fullHouse():
      print("Full House!")
      print("+40")
      points += 40

    # Flush
    elif flush:
      print("Flush!")
      print("+25")
      points += 25

    # Straight
    elif straight:
      print("Straight!")
      print("+20")
      points += 20

    # 3 of a kind
    elif highestCount == 3:
      print("Three of a Kind!")
      print("+15")
      points += 15

    # 2 pair
    elif len(pairs) == 2:
      print("Two Pairs!")
      print("+10")
      points += 10

    # Jacks or better
    elif pairs and pairs[0] > 10:
      print ("Jacks or Better!")
      print("+5")
      points += 5
    
    else:
      print("You had bad cards, no points for these cards.")

    player.cards=[]
    print()
    print()
    print()

def test():
  royalFlush=[Card('Ten',2,'Hearts','10♡'),Card('Jack',11,'Hearts','J♡'),Card('Queen',12,'Hearts','Q♡'),Card('King',13,'Hearts','K♡'),Card('Ace',14,'Hearts','A♡')]
  straightFlush=[Card("Four",4,"Clubs","4♣"),Card("Five",5,"Clubs","5♣"),Card("Six",6,"Clubs","6♣"),Card("Seven",7,"Clubs","7♣"),Card("Eight",8,"Clubs","8♣")]
  fourOfAKind=[Card("Ten",10,"Hearts","10♡"),Card("Seven",7,"Hearts","7♡"),Card("Seven",7,"Clubs","7♣"),Card("Seven",7,"Spades","7♠"),Card("Seven",7,"Diamonds","7♢")]
  fullHouse=[Card("Ace",14,"Diamonds","A♢"),Card("Ace",14,"Spades","A♠"),Card("Ace",14,"Clubs","A♣"),Card("Seven",7,"Diamonds","7♢") ,Card("Seven",7,"Clubs","7♣")]
  flushTest=[Card("Four",4,"Diamonds","4♢"),Card("Nine",9,"Diamonds","9♢"),Card("King",13,"Diamonds","K♢"),Card("Eight",8,"Diamonds","8♢"),Card("Three",3,"Diamonds","3♢")]
  straightTest=[Card("Six",6,"Spades","6♠"),Card("Seven",7,"Diamonds","7♢"),Card("Eight",8,"Hearts","8♡"),Card("Nine",9,"Clubs","9♣"),Card("Ten",10,"Diamonds","10♢")]
  threeOfAKind=[Card("Two",2,"Clubs","2♣"),Card("Seven",7,"Diamonds","7♢"),Card("King",13,"Spades","K♠"),Card("King",13,"Diamonds","K♢"),Card("King",13,"Clubs","K♣")]
  twoPairs=[Card("Eight",8,"Spades","8♠"),Card("Nine",9,"Clubs","9♣"),Card("Nine",9,"Diamonds","9♢"),Card("Six",6,"Clubs","6♣"),Card("Six",6,"Diamonds","6♢")]
  jacksOrBetter = [Card("King",13,"Diamonds","K♢"),Card("Six",6,"Diamonds","6♢"),Card("Queen",12,"Diamonds","Q♢"),Card("King",13,"Hearts","K♣"),Card("Seven",7,"Hearts","7♡")]

  print("test")
  for (a,b,c,d,e,f,g,h,i) in zip(royalFlush,straightFlush,fourOfAKind,fullHouse,flushTest,straightTest,threeOfAKind,twoPairs,jacksOrBetter):
    a.showing=True
    b.showing=True 
    c.showing=True 
    d.showing=True 
    e.showing=True 
    f.showing=True 
    g.showing=True 
    h.showing=True 
    i.showing=True 
  print(royalFlush)
  print(straightFlush)
  print(fourOfAKind)
  print(fullHouse)
  print(flushTest)
  print(straightTest)
  print(threeOfAKind)
  print(twoPairs)
  print(jacksOrBetter)

  print("test")

main()


# In[ ]:




