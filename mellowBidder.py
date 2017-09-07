import mellowGUI
import mellowLogic
import math

def getMellowBid(hand):
	handNum = []
	for x in range(0, len(hand)):
		handNum.append(mellowGUI.convertCardStringToNum(hand[x]))
	
	bid = 0.0
	
	#Add number of aces:
	bid = bid + getNumberOfAces(hand)
	
	print 'Number of aces: ' + str(getNumberOfAces(hand))
	
	#if trumping means losing a king or queen of spades, then it doesn't mean much
	trumpingIsSacrifice = 0
	
	#Add kind of spades if 1 or 2 other spade
	if hasCard(hand, 'KS') and getNumSuit(hand, 'S') >= 2:
		bid = bid + 1
		if getNumSuit(hand, 'S') == 2:
			bid = bid - 0.2
			trumpingIsSacrifice = 1
		print 'ks'
	
	#Add queen of spacdes if 2 other spaces
	if hasCard(hand, 'QS') and getNumSuit(hand, 'S') >= 3:
		bid = bid + 1
		trumpingIsSacrifice = 1
		print 'qs'
	
	if hasCard(hand, 'JS') and getNumSuit(hand, 'S') >= 4 and (hasCard(hand, 'QS') or hasCard(hand, 'KS') or hasCard(hand, 'AS')):
		bid = bid + 0.15
		print 'js'
	
	trumpResevoir = 0.0
	
	#Add a bid for every extra spade over 3 you have:
	if getNumSuit(hand, 'S') > 3:
		bid = bid + (getNumSuit(hand, 'S')) - 3.5
		
		print 'over 3 spades: ' + str((getNumSuit(hand, 'S')) - 3.5)
		
		if hasCard(hand, 'JS'):
			bid = bid + 0.5
		elif hasCard(hand, 'TS'):
			bid = bid + 0.3
			trumpResevoir = 0.201
		#TODO: make cond this a func... because you repeated it...
		elif getNumSuit(hand, 'H') < 2 or  getNumSuit(hand, 'C') < 2 or  getNumSuit(hand, 'D') < 2:
			bid = bid + 0.2
			trumpResevoir = 0.301
		else:
			bid = bid
			trumpResevoir = 0.50
		
		#TODO: 5+ spades should give a special bonus depending on the offsuits.
		# The "take everything" bonus :P
	
	
	print 'off-suit kings:' + str(0.75 * (getNumberOfKings(hand) - hasCard(hand, 'KS')))
	bid = bid + 0.75 * (getNumberOfKings(hand) - hasCard(hand, 'KS'))
	
	#TODO: loop through suits:
	if hasCard(hand, 'KC') and getNumSuit(hand, 'C') == 1:
		bid = bid - 0.55
	elif hasCard(hand, 'KC') and getNumSuit(hand, 'C') > 5:
		bid = bid - 0.35
	elif hasCard(hand, 'KC') and (hasCard(hand, 'AC') or hasCard(hand, 'QC')):
		bid = bid + 0.26
		print 'qc or ac adjust kc'
	
	if hasCard(hand, 'KD') and getNumSuit(hand, 'D') == 1:
		bid = bid - 0.55
	elif hasCard(hand, 'KD') and getNumSuit(hand, 'D') > 5:
		bid = bid - 0.35
	elif hasCard(hand, 'KD') and (hasCard(hand, 'AD') or hasCard(hand, 'QD')):
		bid = bid + 0.26
		print 'qd or ad adjust kd'
		
	if hasCard(hand, 'KH') and getNumSuit(hand, 'H') == 1:
		bid = bid - 0.55
	elif hasCard(hand, 'KH') and getNumSuit(hand, 'H') > 5:
		bid = bid - 0.35
	elif hasCard(hand, 'KH') and (hasCard(hand, 'AH') or hasCard(hand, 'QH')):
		bid = bid + 0.26
		print 'qh or ah adjust kh'
	
	
	if getNumSuit(hand, 'H') < 3 or  getNumSuit(hand, 'C') < 3 or  getNumSuit(hand, 'D') < 3:
		
		if getNumSuit(hand, 'S') >= 2 and getNumSuit(hand, 'S') < 4 and trumpingIsSacrifice == 0:
			reservoir = 0.0
			if trumpingIsSacrifice == 0:
				bid = bid + 0.3
				reservoir = 0.5
				
			
			if (getNumSuit(hand, 'H') < 3 and  getNumSuit(hand, 'C') < 3) or (getNumSuit(hand, 'H') < 3 and  getNumSuit(hand, 'D') < 3) or (getNumSuit(hand, 'C') < 3 and  getNumSuit(hand, 'D') < 3):
				bid = bid + 0.25 + reservoir
			elif getNumSuit(hand, 'H') < 2 or  getNumSuit(hand, 'C') < 2 or  getNumSuit(hand, 'D') < 2:
				bid = bid + 0.25 + reservoir
	
		elif getNumSuit(hand, 'S') >= 4 and trumpResevoir > 0:
				if getNumSuit(hand, 'H') < 2 or  getNumSuit(hand, 'C') < 2 or  getNumSuit(hand, 'D') < 2:
					bid = bid + trumpResevoir
	
	
	
	if getNumSuit(hand, 'S') == 0:
		bid = bid  - 1
	
	bid = math.floor(bid)
	
	if bid < 0:
		bid = 0
	
	print 'Final bid: ' + str(bid)
#Utility functions:

def getNumberOfKings(hand):
	ret = 0
	for x in range(0, len(hand)):
		if hand[x][0:].find('K') != -1:
			ret = ret + 1
			
	return ret
	
def getNumberOfAces(hand):
	ret = 0
	for x in range(0, len(hand)):
		if hand[x].find('A') != -1:
			ret = ret + 1
			
	return ret
	
def hasCard(hand, str):
	for x in range(0, len(hand)):
		if hand[x] == str:
			return 1
	
	return 0
	
	
def getNumSuit(hand, suit):
	ret = 0
	for x in range(0, len(hand)):
		if hand[x][1:].find(suit) != -1:
			ret = ret + 1
	return ret