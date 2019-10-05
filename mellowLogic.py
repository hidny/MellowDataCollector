#!/usr/bin/env python
import sys
import time
import os

from threading import Thread
import threading

import mellowGUI
import random

import mellowBidder

#The variables are static because I only want one mellow client for the whole execution.

#Mellow specific constants:
START_MSG = 'From Game(public): Starting Mellow!'
YOUR_BID = 'From Game(private): What\'s your bid?'
YOUR_TURN = 'From Game(private): Play a card!'
PRIVATE_MSG = 'From Game(private):'
PUBLIC_MSG = 'From Game(public): '
#first dealer:
FIRST_DEALER = 'From Game(public): First dealer is '
DEALER_MSG = 'dealer is '
FIGHT_SUMMARY_MSG = 'From Game(public): Fight Winner:'
#From Game(private): 7C KS 9C AC AH 2S 4D KC KH 2D 7H 9S 7S 
STARTING_HAND_LENGTH = 13

TRICKS = 'trick(s).'

PLAYING_CARD = 'playing:'
PUBLIC_SERVER_MSG = 'From Game(public): '
WIN = 'win!'
END_OF_ROUND = 'END ROUND!'
#End Mellow specific constants

#Game specific variables:
gameStarted = 0
players = []
#http://stackoverflow.com/questions/419145/python-threads-critical-section
turn_lock = threading.Lock()
#End game specific variables:

currentBid = -1

def isNumber(s):
	try:
		float(s)
		return 1
	except ValueError:
		return 0
		
def isACard(card):
	if len(card) != 2:
		return 0
	else:
		if card[0] == '2' or card[0] == '3' or card[0] == '4' or card[0] == '5' or card[0] == '6' or card[0] == '7' or card[0] == '8' or card[0] == '9'  or card[0] == 'T'  or card[0] == 'J' or card[0] == 'Q'  or card[0] == 'K'   or card[0] == 'A':
			if card[1] == 'S' or card[1] == 'H' or card[1] == 'C' or card[1] == 'D':
				return 1


#Mellow gui: convertCardNumToString

#Assumes 52 card deck
def getShuffledDeck():
	deck = []
	for x in range(0, 52):
		deck.append(x)

	for i in range(0, 52):
		swap(deck, i, random.randint(i, 52 - 1))
	
	return deck

def swap(deck, i, j):
	temp = deck[i]
	deck[i] = deck[j]
	deck[j] = temp

#Pre: this should only get called from MellowGUI
def main(mellowGUIVars):
	gameLogic(mellowGUIVars)



#TODO: use this to make everything feel smoother
def slowDownIfInteract(amountOfTime):
	time.sleep(amountOfTime)


def gameLogic(mellowGUIVars):
	
	print 'Inside Mellow gameLogic function!'
	
	numBidsMade = 0
	
	#1st for 1st bidder:
	f=open("outputBidData1st.txt", "a+")
	
	f.write("Manual bid data collection started\n");
	
	#https://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/
	now = time.strftime("%c")
	f.write("Date(MM/DD/YY) and time: " + time.strftime("%c") + "\n")
	
	
	while numBidsMade < 1000 and mellowGUIVars.isStillRunning() == 1:
	
		#serve cards
		deck = getShuffledDeck()
		hand = []
		
		#TODO: less hard coding and make a helper function
		#Rig it so there's no AS or KS:
		foundHandWithoutASorKS=0
		handWithoutASorKS=0
		while foundHandWithoutASorKS == 0:
			foundHandWithoutASorKS = 1
			for i in range(0, 13):
				tempCard = mellowGUI.convertCardNumToString(deck[13 * handWithoutASorKS + i])
				if tempCard == "AS" or tempCard == "KS":
					handWithoutASorKS = handWithoutASorKS + 1
					foundHandWithoutASorKS = 0
					break
		
		
		handStringTest = ''
		for i in range(0, 13):
			hand.append(deck[13 * handWithoutASorKS + i])
			handStringTest = handStringTest + mellowGUI.convertCardNumToString(hand[i]) + ' '
		#END setting hand
		
		hand = mellowGUI.sortCards(hand)
		
		for i in range(0, 13):
			hand[i] = mellowGUI.convertCardNumToString(hand[i])
		
		handString = ''
		for i in range(0, 13):
			handString = handString + hand[i] + ' '
		
		mellowGUIVars.setupCardsForNewDeck(hand)
		
		bid = -1
		
		while (bid < 0 or mellowGUIVars.isRebidPressed() == 1) and mellowGUIVars.isStillRunning() == 1:
			
			#Reset the bid to -1 (no bid)
			mellowGUIVars.bidSouth(-1)
			
			#ask for bid
			mellowGUIVars.askUserForBid()
			
			if mellowGUIVars.isRebidPressed() == 1:
				mellowGUIVars.setMessage('Rebid!')
			else:
				mellowGUIVars.setMessage('Bids made: ' + str(numBidsMade))
			
			#Ask for alternative bids:
			mellowGUIVars.unpressRebid()
			mellowGUIVars.resetAlternativeBids()
			
			temp = -1
			
			while temp < 0 and mellowGUIVars.isStillRunning() == 1:
				temp = mellowGUIVars.consumeBid()
				time.sleep(0.2)
			
			bid = temp
			
			mellowGUIVars.bidSouth(bid)
			
			if bid > 0:
				mellowGUIVars.setMessage('You bid ' + str(bid) + '. Any Alternative bids?')
			else:
				mellowGUIVars.setMessage('You bid mellow. Any Alternative bids?')
			
			#ask mellowBidder
			mellowBidder.getMellowBid(hand)
			
			#Ask for alternative bids:
			mellowGUIVars.askUserForAlternativeBids()
			
			temp = []
			
			while mellowGUIVars.isWaitingForAlternativeBids() and mellowGUIVars.isRebidPressed() == 0 and mellowGUIVars.isStillRunning() == 1:
				time.sleep(0.2)
			
		alternativeBids = mellowGUIVars.consumeAlternativeBid()
		alternativeBids.sort()
		
		#write to file
		#format: card strings followed by newline
		#space seperated numbers followed by newline
		handString = ''
		for i in range(0, 13):
			handString = handString + hand[i] + ' '
		
		print handString
		print bid
		print alternativeBids
		
		if mellowGUIVars.isStillRunning() == 1:
			#WRITE TO FILE
			f.write(str(handString) + "\n")
			f.write(str(bid) + "\n")
			f.write(str(alternativeBids) + "\n")
			f.write("\n")
			
			#Write to file IMMEDIATELY:
			f.flush()
			os.fsync(f.fileno())
		
		#update counter
		numBidsMade = numBidsMade + 1
	
	#End of loop:
	f.close()
	
def testingRandom():

	matrix = [[0 for i in xrange(52)] for j in xrange(52)]
	
	smallCount = [0 for i in xrange(52)]
	
	for n in range(0, 100000):
		deck = getShuffledDeck()
		smallCount = [0 for i in xrange(52)]
		
		for i in range(0, 52):
			matrix[i][deck[i]] = matrix[i][deck[i]]+1
			smallCount[deck[i]] = smallCount[deck[i]] + 1
	
		for i in range(0, 52):
			if smallCount[i] != 1:
				print 'Error! Not all cards there'
				exit(1)
	
	for i in range(0, 52):
		for j in range(0, 52):
			print matrix[i][j],
		print ''

#You have to start it from mellowGUI because pygame has to be the main 
#thread.
if __name__ == "__main__":
	testingRandom()
	exit(1)