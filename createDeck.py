import os
import json
import collections.abc as col
import random
import copy


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
            if playerStats[card][val] > 0:
                numCards = playerStats[card][val]
                costCard = cardDB[card][val]
                update = {card : {val : {'NUMBER' : numCards, 'COST' : costCard}}}
                totalCards = totalCards + numCards
                totalValue = totalValue + costCard
                deep_update(cardbase, update)

cont = True
cardsLeft = totalCards
cardsSelected = 0
deckValue = 0
while cont :
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
                costCard = cardDB[card][val]
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
            if lowestCost == 0 or lowestCost > cardbase[card][val]['COST']:
                lowestCost = cardbase[card][val]['COST']
            if (cardbase[card][val]['COST'] + deckValue) > totalCP:
                dupCardBase[card].pop(val)
    cardbase = copy.deepcopy(dupCardBase)
    if cardsSelected == maxDeckSize or cardsLeft == 0 or deckValue + lowestCost > totalCP:
        cont = False
sortedDeck = {}
for card in deck:
    for val in sorted(deck[card]):
        numCards = deck[card][val]['NUMBER']
        costCard = deck[card][val]['COST']
        update = {card : {val : {'NUMBER' : numCards, 'COST' : costCard}}}
        deep_update(sortedDeck, update)
print(sortedDeck)
print('Deck Value: ', deckValue)
print('Number of Cards: ', cardsSelected)