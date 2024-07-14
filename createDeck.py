import os
import json
import collections.abc as col
import random
import copy
import sys

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, col.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source
cwd = os.getcwd()
name = 'Decks'
if len(sys.argv) > 1:
    name = sys.argv[1]
newpath = cwd + '\\decks\\'
if not os.path.exists(newpath):
    os.makedirs(newpath)
filepath = cwd + '\\decks\\' + name + '.txt'
c = open('cardDB.json')
p = open('playerStats.json')
cardDB = json.load(c)
playerStats = json.load(p)

totalCP = playerStats['SORA']['CP']
maxDeckSize = playerStats['SORA']['MAX']
cardbase = {}
deck = {}
totalCards = 0
totalValue = 0

#Create the cardbase
for card in playerStats:
    if card != 'SORA':
        for val in playerStats[card]:
            if playerStats[card][val]['QUANT'] > 0:
                numCards = playerStats[card][val]['QUANT']
                premCards = playerStats[card][val]['PREM']
                costCard = cardDB[card][val]
                premCost = cardDB[card].get('1') 
                update = {card : {val : {'NUMBER' : numCards, 'COST' : costCard, "PREM" : premCards, "PREMCOST" : premCost}}}
                totalCards = totalCards + numCards
                totalValue = totalValue + costCard
                deep_update(cardbase, update)

cont = True
cardsLeft = totalCards
cardsSelected = 0
deckValue = 0
while cont:
    randNum = random.randint(1, cardsLeft)
    cardSelected = 0
    cardFound = False
    dupCardBase = copy.deepcopy(cardbase)
    for card in cardbase :
        if (cardFound == True):
            break
        for val in cardbase[card]:
            if (cardFound == True):
                break
            cardSelected = cardSelected + 1
            if cardSelected == randNum:
                cardFound = True
                cardsLeft = cardsLeft - 1
                cardsSelected = cardsSelected + 1
                numCards = playerStats[card][val]
                if cardbase[card][val]['PREM'] > deck.get(card, {}).get(val, {}).get('NUMBER', 0):
                    costCard = cardbase[card][val]['PREMCOST']
                    cardbase[card][val]['PREM'] = cardbase[card][val]['PREM'] - 1
                else:
                    costCard = cardbase[card][val]['COST']
                deckValue = deckValue + costCard
                if deck.get(card, {}).get(val):
                    deck[card][val]['NUMBER'] = deck[card][val]['NUMBER'] + 1
                    deck[card][val]['COST'] = deck[card][val]['COST'] + costCard
                else:
                    update = {card : {val : {'NUMBER' : 1, 'COST' : costCard}}}
                    deep_update(deck, update)
                if (deck[card][val]['NUMBER'] == cardbase[card][val]['NUMBER']) :
                    dupCardBase[card].pop(val)
    lowestCost = 0
    cardbase = copy.deepcopy(dupCardBase)
    for card in cardbase:
        for val in cardbase[card]:
            cardVal = cardbase[card][val]['PREMCOST'] if cardbase[card][val]['PREM'] > 0 else cardbase[card][val]['COST']
            if lowestCost == 0 or lowestCost > cardVal:
                lowestCost = cardVal
            if (cardVal + deckValue) > totalCP:
                dupCardBase[card].pop(val)
        if len(dupCardBase[card]) == 0:
            dupCardBase.pop(card)
    cardbase = copy.deepcopy(dupCardBase)
    if cardsSelected >= maxDeckSize or cardsLeft <= 0 or deckValue + lowestCost > totalCP or len(cardbase) == 0:
        cont = False
sortedDeck = {}
for card in deck:
    for val in sorted(deck[card]):
        numCards = deck[card][val]['NUMBER']
        costCard = deck[card][val]['COST']
        update = {card : {val : numCards}}
        deep_update(sortedDeck, update)

f = open(filepath, 'a')
f.write(name + '\n')
f.write('Deck Value: ' + str(deckValue) + '\n')
f.write('Number of Cards: ' + str(cardsSelected) + '\n')
for card in sortedDeck:
    f.write(card + ':\n')
    for val in sortedDeck[card]:
        f.write(val + ': ' + str(sortedDeck[card][val]) + '\n')
f.close()
print('Grats on your shiny new deck!')