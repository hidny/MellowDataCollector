import sys, pygame
import time

import random, os
import pygame
from threading import Thread
import threading

#from pygame import _view
from pygame.locals import *
from sys import exit

import box
import mellowLogic

#This is designed to be a singleton object

	
FIRST_ROUND = -999
	
class MellowGUI:
	
	pygame.init()
	
	gameOver = 0
	
	screen_width = 1300
	screen_height = 900
	
	size = width, height = screen_width, screen_height
	
	screen = pygame.display.set_mode(size)
	
	off_the_edgeX = 150
	off_the_edgeY = 150

	card_width = 79
	card_height = 123


	THROW_TIME=100
	FRAME_WAIT_TIME = 40
	
	WHITE = (255, 255, 255)

	#Images:
	background_image_filename = 'Image/wood3.png'
	background = pygame.image.load(background_image_filename)

	cardz_image_file = 'Image/cardz.png'
	cardz = pygame.image.load(cardz_image_file)

	backcard_image_file = 'Image/back.jpg'
	backcard = pygame.image.load(backcard_image_file)

	dot_image_file = 'Image/dot.png'
	dot = pygame.image.load(dot_image_file).convert()

	red_dot_image_file = 'Image/reddot.png'
	reddot = pygame.image.load(red_dot_image_file).convert()

	green_dot_image_file = 'Image/greendot.png'
	greendot = pygame.image.load(green_dot_image_file).convert()
	
	
	
	
	def __init__(self):
		self.bidButtons = []
		
		self.bidButtons.append(box.Box(self.width/2 - 180, self.height/2 - 90, 110, 50))
		self.bidButtons.append(box.Box(self.width/2 - 60, self.height/2 - 90, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 - 0, self.height/2 - 90, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 + 60, self.height/2 - 90, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 + 120, self.height/2 - 90, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 - 180, self.height/2 - 30, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 - 120, self.height/2 - 30, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 - 60, self.height/2 - 30, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 - 0, self.height/2 - 30, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 + 60, self.height/2 - 30, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 + 120, self.height/2 - 30, 50, 50))
		self.bidButtons.append(box.Box(self.width/2 - 180, self.height/2 + 30, 110, 50))
		self.bidButtons.append(box.Box(self.width/2 - 60, self.height/2 + 30 , 110, 50))
		self.bidButtons.append(box.Box(self.width/2 + 60, self.height/2 + 30, 110, 50))
		
		#Alternative bid buttons:
		self.rebidButton = box.Box(self.width/2 - 180, self.height/2 + 90, 110, 50)
		self.nextBidButton = box.Box(self.width/2 + 60, self.height/2 + 90, 110, 50)
		
		self.userPressedRebid = 0
		
		self.southCardLock = threading.Lock()
		self.westCardLock = threading.Lock()
		self.northCardLock = threading.Lock()
		self.eastCardLock = threading.Lock()

		self.scoreLock = threading.Lock()
		
		
		self.tricks = 4*[0]
		
		#Variable to handle the animation of thrown cards:
		self.projectiles = []
		
			
		self.southCards = 13 * [-1]
		self.westCards = 13 * [0]
		self.northCards= 13 * [0]
		self.eastCards = 13 * [0]
		
		
		self.currentMsg = ''
		
		self.cardUserWantsToPlay = ''
		
		
		self.lastFrameTime = int(round(time.time() * 1000))
		
		self.isAwaitingBid = 0
		self.currentBid = -1
		
		self.isAwaitingAlternativeBid = 0
		self.currentAlternativeBids = []
		
		#Dealers:
		self.dealer = ''

		#if this is 1, the back is blue.
		#if this is 0, the back is red.
		#(I feel like this is a good way to troll people)
		self.backIsBlue = 1

		self.prevScoreForUs = 0
		self.prevScoreForThem = 0
		self.diffScoreUs =FIRST_ROUND
		self.diffScoreThem =FIRST_ROUND
		self.scoreForUs = 0
		self.scoreForThem = 0

		self.southBid = -1
		self.westBid = -1
		self.northBid = -1
		self.eastBid = -1
		
	
	def updateLastFrameTime(self):
		self.lastFrameTime = int(round(time.time() * 1000))
	
	def isStillRunning(self):
		if self.gameOver == 0:
			return 1
		else:
			print 'GAME OVER according to isStillRunning(self)'
			return 0
	
	#Functions called by some controller file:
	def setupCardsForNewDeck(self, southCardsInput):
		tempArray = []
		
		for index in range(0, len(southCardsInput)):
			tempArray.append(convertCardStringToNum(southCardsInput[index]))
		
		tempArray = sortCards(tempArray)
		
	
		self.southBid = -1
		self.westBid = -1
		self.northBid = -1
		self.eastBid = -1
		
		
		
		with self.southCardLock:
				with self.eastCardLock:
					with self.westCardLock:
						with self.northCardLock:
							self.southCards = tempArray
							self.westCards  =  13* [-1]
							self.northCards =  13* [-1]
							self.eastCards  =  13* [-1]
							
							self.tricks = 4 *[0]


	def resetAlternativeBids(self):
		self.currentAlternativeBids = []
	
	def setDealer(self, name):
		self.dealer = name
	
	def bidSouth(self, bid):
		#with self.bidLock:
		self.southBid = bid
		
	def bidWest(self, bid):
		#with self.bidLock:
		self.westBid = bid
		
	def bidNorth(self, bid):
		#with self.bidLock:
		self.northBid = bid
		
	def bidEast(self, bid):
		#with self.bidLock:
		self.eastBid = bid
			
	
	
	def updateScore(self, us, them):
	
		with self.scoreLock:
			self.prevScoreForUs = self.scoreForUs
			self.prevScoreForThem = self.scoreForThem
		
			self.diffScoreUs  =    us - self.prevScoreForUs
			self.diffScoreThem =  them - self.prevScoreForThem
			
			self.scoreForUs = us
			self.scoreForThem = them
		
	#END CONTROL FUNCTIONS
	def printScore(self):
	
		pygame.draw.rect(self.screen, (255, 255, 255, 0), ((1*self.width)/32, (4*self.height)/5 + 10, 300, 200))
		#Make summation lines:
		pygame.draw.rect(self.screen, (0, 0, 255, 0), ((1*self.width)/32, (4*self.height)/5 + 10 + 3*40, 60, 5))
		pygame.draw.rect(self.screen, (0, 0, 255, 0), ((1*self.width)/32 + 70, (4*self.height)/5 + 10 + 3*40, 60, 5))
		
		
		with self.scoreLock:
			myfont = pygame.font.SysFont("comicsansms", 30)
			
			
			labelExample1 = myfont.render("US       THEM", 1, (0,0,255))
			
			labelExample2 = myfont.render(str(self.prevScoreForUs) + "    " + str(self.prevScoreForThem), 1, (0,0,255))
			
			labelExample3 = myfont.render(" " + str(self.diffScoreUs) + "     " + str(self.diffScoreThem), 1, (0,0,255))
			
			labelExample4 = myfont.render(str(self.scoreForUs) + "    " + str(self.scoreForThem) + "  (" + self.dealer + ")", 1, (0,0,255))
			
			self.screen.blit(labelExample1, ((1*self.width)/32, (4*self.height)/5 + 10))
			
			if self.diffScoreThem == FIRST_ROUND:
				#If it's the first round and don't put the previous scores up...
				pass
			else:
				self.screen.blit(labelExample2, ((1*self.width)/32, (4*self.height)/5 + 10 + 1*40))
				self.screen.blit(labelExample3, ((1*self.width)/32, (4*self.height)/5 + 10 + 2*40))
			self.screen.blit(labelExample4, ((1*self.width)/32, (4*self.height)/5 + 10 + 3*40))
	
	def printTricks(self):
		myfont = pygame.font.SysFont("comicsansms", 30)
		
		labelTricksSouth = myfont.render(str(self.tricks[0]) + "/" + str(self.southBid), 1, (0,0,255))
		labelTricksWest = myfont.render(str(self.tricks[1]) + "/" + str(self.westBid), 1, (0,0,255))
		labelTricksNorth = myfont.render(str(self.tricks[2]) + "/" + str(self.northBid), 1, (0,0,255))
		labelTricksEast = myfont.render(str(self.tricks[3]) + "/" + str(self.eastBid), 1, (0,0,255))
		
		if self.westBid >= 0:
			self.screen.blit(labelTricksWest, (5, self.height/2))
		
		if self.eastBid >= 0:
			self.screen.blit(labelTricksEast, (1*self.width - 85, self.height/2))
		
		if self.northBid >= 0:
			self.screen.blit(labelTricksNorth, (self.width/2, self.height/20))
		
		if self.southBid >= 0:
			self.screen.blit(labelTricksSouth, (self.width/2, self.height - 90))
	
	def printcard(self, x, y, num, rotate90):
		if num >= 52:
			print 'ERROR: card num is greater than 52!'
			num = 0
			sys.exit(1)
		
		if num < 0:
			if rotate90 ==0:
				self.screen.blit(self.backcard, (x, y), (self.backIsBlue*self.card_width, 0, self.card_width, self.card_height))
			else:
				temp = pygame.transform.rotate(self.backcard, 270)
				self.screen.blit(temp, (x, y), (0, self.backIsBlue * self.card_width, self.card_height, self.card_width))
		else:
			if rotate90 ==0:
				self.screen.blit(self.cardz, (x, y), ((num%13) * self.card_width, (num/13) * self.card_height, self.card_width, self.card_height))
			else:
				temp = pygame.transform.rotate(self.cardz, 270)
				self.screen.blit(temp, (x, y), (((4-1) - num/13) * self.card_height, (num%13) * self.card_width, self.card_height, self.card_width))


	
	def printcardFromCenter(self, centerX, centerY, num, rotate90):
		if rotate90 == 0:
			self.printcard(int(centerX - self.card_width/2), int(centerY - self.card_height/2), num, rotate90)
		else:
			self.printcard(int(centerX - self.card_height/2), int(centerY - self.card_width/2), num, rotate90)

	def getXCordFirstCardNorthSouth(self, cardList):
		if cardList != None:
			firstX = self.screen_width/2
			if len(cardList) % 2 == 0:
				firstX = firstX + self.card_width/4
			
			firstX = firstX - int(len(cardList)/2)*(self.card_width/2)
			
			return firstX
		else:
			return 0


	def isMouseHoveringOverCard(self, mx, my):
		firstX = self.getXCordFirstCardNorthSouth(self.southCards)
		
		if my > self.screen_height - self.off_the_edgeY - self.card_height/2:
			if my< self.screen_height - self.off_the_edgeY + self.card_height/2:
				firstX = self.getXCordFirstCardNorthSouth(self.southCards)
				if mx > firstX - self.card_width/2:
					if mx < firstX + len(self.southCards) * self.card_width/2:
						return 1
		return 0

	def printcardSuitNum(self, x, y, suit, num):
		printcard(x, y, 13*suit + num, 1)

	def fill_background(self):
		for y in range(0, self.screen_height, self.background.get_height()):
			for x in range(0, self.screen_width, self.background.get_width()):
				self.screen.blit(self.background, (x, y))

	def printSouthCards(self, mx, my):
		currentX = self.getXCordFirstCardNorthSouth(self.southCards)
		
		indexOfMouseOnCard = self.getIndexCardHover(mx, my)
		mouseHoveringOverCard = self.isMouseHoveringOverCard(mx, my)
		
		with self.southCardLock:
			for x in range(0, len(self.southCards)):
				
				if mouseHoveringOverCard == 1 and indexOfMouseOnCard == x:
					self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY - self.card_height/4, self.southCards[x], 0)
				else:
					self.printcardFromCenter(currentX, self.screen_height - self.off_the_edgeY,  self.southCards[x], 0)
				currentX = currentX + (self.card_width/2)
	
		

	def printWestCards(self):
		firstY = self.screen_height/2
		if len(self.westCards) % 2 == 0:
			firstY = firstY + self.card_width/4
			
		firstY = firstY - int(len(self.westCards)/2)*(self.card_width/2)
		currentY = firstY
		
		for x in range(0, len(self.westCards)):
			self.printcardFromCenter(self.off_the_edgeX, currentY, -1, 1)
			currentY = currentY + (self.card_width/2)
		
		
	def printNorthCards(self):
		
		firstX = self.getXCordFirstCardNorthSouth(self.northCards)
		currentX = firstX
		
		for x in range(0, len(self.northCards)):
			self.printcardFromCenter(currentX, self.off_the_edgeY, -1, 0)
			currentX = currentX + (self.card_width/2)
		
	def printEastCards(self):
		firstY = self.screen_height/2
		if len(self.eastCards) % 2 == 0:
			firstY = firstY + self.card_width/4
			
		firstY = firstY - int(len(self.eastCards)/2)*(self.card_width/2)
		currentY = firstY
		
		for x in range(0, len(self.eastCards)):
			self.printcardFromCenter(self.screen_width - self.off_the_edgeX, currentY, -1, 1)
			currentY = currentY + (self.card_width/2)
		
	

	NOINDEX = -2
	def getIndexCardHover(self, mx, my):
		if my > self.screen_height - self.off_the_edgeY - self.card_height/2:
			if my< self.screen_height - self.off_the_edgeY + self.card_height/2:
				firstX = self.getXCordFirstCardNorthSouth(self.southCards)
				currentX = firstX
				for x in range(0, len(self.southCards)):
					if mx < currentX - self.card_width/2:
						return x-1
					
					currentX = currentX + (self.card_width/2)
				return len(self.southCards) - 1
				
		return self.NOINDEX

	#rearranges cards in the current players hand.
	def shiftSouthCards(self, origIndex, isLeft, numSpaces):
		#test some preconditions just in case
		if origIndex < len(self.southCards) and origIndex >= 0:
			if (origIndex + numSpaces < len(self.southCards) and isLeft == 0) or (origIndex - numSpaces >= 0 and isLeft == 1):
				temp = self.southCards[origIndex]
				if isLeft == 1:
					for x in range(0, numSpaces):
						self.southCards[origIndex - x] = self.southCards[origIndex - x - 1]
					self.southCards[origIndex - numSpaces] = temp
				else:
					for x in range(0, numSpaces):
						self.southCards[origIndex + x] = self.southCards[origIndex + x + 1]
					self.southCards[origIndex + numSpaces] = temp
		
		return self.southCards


	def getCardLocation(self, cardHeldIndex):
		currentX = self.getXCordFirstCardNorthSouth(self.southCards)
		return currentX + cardHeldIndex* (self.card_width/2)

	
	def reorgSouthCards(self, mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex):
		with self.southCardLock:
			indexOfMouseOnCard = self.getIndexCardHover(mx, my)
			
			mouseHoveringOverCard = self.isMouseHoveringOverCard(mx, my)
			
			#no card held:
			if mouseJustPressed == 1:
				
				if mouseHoveringOverCard == 1:
					cardHeldIndex = indexOfMouseOnCard
			
			
			if mouseJustRelease == 1:
				if self.isWaitingForBid() == 1:
					self.checkIfUserBidAfterClick(mx, my)
				elif self.isWaitingForAlternativeBids() == 1:
					self.checkIfUserBidAlternativeAfterClick(mx, my)
					self.checkIfUserPressedNext(mx, my)
					self.checkIfUserPressedRebid(mx, my)
				
				if my < self.screen_height - self.off_the_edgeY - self.card_height/2:
					if cardHeldIndex >= 0:
						if cardHeldIndex >=0 and cardHeldIndex < len(self.southCards):
							#print 'Trying to play: ' + str(convertCardNumToString(self.southCards[cardHeldIndex]))
							cardHeldIndex = self.NOINDEX
							
			
			if mouseHeld == 1:
				if mouseHoveringOverCard == 1:
					if cardHeldIndex > indexOfMouseOnCard:
						shiftAmount = cardHeldIndex - indexOfMouseOnCard
						self.southCards = self.shiftSouthCards(cardHeldIndex, 1, shiftAmount)
						cardHeldIndex = indexOfMouseOnCard
						
					elif cardHeldIndex < indexOfMouseOnCard:
						shiftAmount = indexOfMouseOnCard - cardHeldIndex
						self.southCards = self.shiftSouthCards(cardHeldIndex, 0, shiftAmount)
						cardHeldIndex = indexOfMouseOnCard
				
			return cardHeldIndex
	
	def setMessage(self, message):
		self.currentMsg = message
	
	def displayCenterGameMsg(self):
		myfont = pygame.font.SysFont("comicsansms", 30)
		xOffset = len(self.currentMsg)
		labelExample = myfont.render(str(self.currentMsg), 1, (0,0,255))
		#100 = rect height
		self.screen.blit(labelExample, (self.width/2 - 10 * xOffset, self.height/2 - 50 + 200))
	
	def displayBidChoices(self):
		
		pygame.draw.rect(self.screen, (255, 0, 255, 0), (self.width/2 - 200, self.height/2 - 100, 400, 200))
		
		myfont = pygame.font.SysFont("Bauhaus 93", 30)
		
		for i in range(0, len(self.bidButtons)):
			pygame.draw.rect(self.screen, (0, 0, 0, 0), self.bidButtons[i].getCoordBox())
			if i == 0:
				labelExample = myfont.render("Mellow", 1, (0,255,0))
			else:
				labelExample = myfont.render(str(i), 1, (0,255,0))
			
			self.screen.blit(labelExample, self.bidButtons[i].getTopLeftBox())
	
	def displayAlternativeBidChoices(self):
		
		pygame.draw.rect(self.screen, (255, 0, 255, 0), (self.width/2 - 200, self.height/2 - 100, 400, 200))
		
		myfont = pygame.font.SysFont("Bauhaus 93", 30)
		
		for i in range(0, len(self.bidButtons)):
			if i != self.southBid:
				if i in self.currentAlternativeBids:
					pygame.draw.rect(self.screen, (255, 255, 255, 0), self.bidButtons[i].getCoordBox())
				else:
					pygame.draw.rect(self.screen, (0, 0, 0, 0), self.bidButtons[i].getCoordBox())
				
				if i == 0:
					labelExample = myfont.render("Mellow", 1, (0,255,0))
				else:
					labelExample = myfont.render(str(i), 1, (0,255,0))
				
				self.screen.blit(labelExample, self.bidButtons[i].getTopLeftBox())
	
	def displayRebidAndNextButtons(self):
		
		pygame.draw.rect(self.screen, (255, 0, 255, 0), (self.width/2 - 200, self.height/2 + 100, 400, 50))
		
		myfont = pygame.font.SysFont("Bauhaus 93", 30)
		
		pygame.draw.rect(self.screen, (0, 0, 0, 0), self.rebidButton.getCoordBox())
		labelExample = myfont.render("Rebid", 1, (0,255,0))
		self.screen.blit(labelExample, self.rebidButton.getTopLeftBox())
		
		pygame.draw.rect(self.screen, (0, 0, 0, 0), self.nextBidButton.getCoordBox())
		labelExample = myfont.render("Next", 1, (0,255,0))
		self.screen.blit(labelExample, self.nextBidButton.getTopLeftBox())
		
		
	
	def askUserForBid(self):
		self.isAwaitingBid = 1
	
	def isWaitingForBid(self):
		return self.isAwaitingBid
	
	def checkIfUserBidAfterClick(self, x, y):
		for i in range(0, len(self.bidButtons)):
				if self.bidButtons[i].isWithinBox(x, y):
					print 'Clicked on ' + str(i)
					self.currentBid = i
		return -1
	
	#returns the bid if the user bid. Returns -1 otherwise.
	def consumeBid(self):
		if self.currentBid >= 0:
			self.isAwaitingBid = 0
		temp = self.currentBid
		self.currentBid = -1
		return temp	
	
	def askUserForAlternativeBids(self):
		self.isAwaitingAlternativeBid = 1

	def isWaitingForAlternativeBids(self):
		return self.isAwaitingAlternativeBid
	
	def isRebidPressed(self):
		return self.userPressedRebid
		
	def unpressRebid(self):
		self.userPressedRebid = 0
	
	def checkIfUserBidAlternativeAfterClick(self, x, y):
		for i in range(0, len(self.bidButtons)):
			if i != self.southBid and self.bidButtons[i].isWithinBox(x, y):
				print 'Clicked on ' + str(i) + ' for alternative'
				
				#TODO: I might need to make a lock
				if i in self.currentAlternativeBids:
					self.currentAlternativeBids.remove(i)
				else:
					self.currentAlternativeBids.append(i)
		return -1
		
	def checkIfUserPressedNext(self, x, y):
		if self.nextBidButton.isWithinBox(x, y):
			self.isAwaitingAlternativeBid = 0
	
	def checkIfUserPressedRebid(self, x, y):
		if self.rebidButton.isWithinBox(x, y):
			self.userPressedRebid = 1
	
	def consumeAlternativeBid(self):
		if self.isAwaitingAlternativeBid == 0:
			temp = self.currentAlternativeBids
		else:
			temp = []
		
		return temp
	
def convertCardNumToString(num):
	if num < 0:
		return '??'
	
	suit = ''
	if num >=0 and num <13:
		suit = 'C'
	elif num >=13 and num <26:
		suit = 'D'
	elif num >=26 and num <39:
		suit = 'H'
	elif num >=39 and num <52:
		suit = 'S'
	else:
		print 'ERROR: Trying to convert card with num ' + str(num) + ' in convertCardNumToString(num)'
		sys.exit(1)
	
	CardNumber = -1
	if num % 13 == 0:
		CardNumber = 'A'
	elif num % 13 == 9:
		CardNumber = 'T'
	elif num % 13 == 10:
		CardNumber = 'J'
	elif num % 13 == 11:
		CardNumber = 'Q'
	elif num % 13 == 12:
		CardNumber = 'K'
	else:
		CardNumber = str((num % 13) + 1)
	
	return str(CardNumber) + suit
	
#FUNCTIONS THAT OUTSIDE CLASSES SHOULD USE:
def convertCardStringToNum(card):
	row = 0
	if card[1:].find('C') != -1:
		row = 0
	elif card[1:].find('D') != -1:
		row = 1
	elif card[1:].find('H') != -1:
		row = 2
	elif card[1:].find('S') != -1:
		row = 3
	else:
		print card
		print str(len(card))
		print 'ERROR: unknown suit!'
		sys.exit(1)

	if card[:1].find('A') != -1:
		column = 0
	elif card[:1].find('T') != -1:
		column = 9
	elif card[:1].find('J') != -1:
		column = 10
	elif card[:1].find('Q') != -1:
		column = 11
	elif card[:1].find('K') != -1:
		column = 12
	else:
		column = int(card[0]) - 1
	
	return 13*row + column


def sortCards(tempArray):
	#Raise up heart so the suits can go red black red black (For Richard)
	for x in range(0, len(tempArray)):
			if tempArray[x] >=26 and  tempArray[x] < 39:
				tempArray[x] = tempArray[x] + 130


	#Ace values should increase so they can be properly sorted:
	for x in range(0, len(tempArray)):
		if tempArray[x] % 13 == 0:
			tempArray[x] = tempArray[x] + 13

	tempArray.sort()

	#put the ace values back to the way they were:
	for x in range(0, len(tempArray)):
		if tempArray[x] % 13 == 0:
			tempArray[x] = tempArray[x] - 13

			
	#lower  hearts so the suits can go red black red black (For Richard)
	for x in range(0, len(tempArray)):
			if tempArray[x] >=130 + 26 and  tempArray[x] < 130 + 39:
				tempArray[x] = tempArray[x] - 130
				
	return tempArray


def main():
	mellowGUI = MellowGUI()
	#keep track of the last frame/heartbeat so we can throw projectiles smoothly.
	mellowGUI.updateLastFrameTime()
	
	print 'Inside Mellow GUI main!'
	
	try:
		t = Thread(name = 'Testing', target=mellowLogic.gameLogic, args=(mellowGUI,))
		t.start()
	except:
		print "Error: unable to start thread for MellowLogic.py"
	
	
	#texting adding 
	myfont = pygame.font.SysFont("comicsansms", 30)
	
	clock = pygame.time.Clock()
	
	
	mellowLogo = pygame.image.load("MellowLogo.png").convert()
	transColor = mellowLogo.get_at((0,0))
	mellowLogo.set_colorkey(transColor)
	
	versNumber = pygame.image.load("versNumber.png").convert()
	transColor = versNumber.get_at((0,0))
	versNumber.set_colorkey(transColor)
	

	mouseJustPressed = 0
	mouseHeld = 0
	mouseJustRelease = 0
	cardHeldIndex = mellowGUI.NOINDEX
	
	
	while 1:
		
		#React to user events:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mellowGUI.gameOver = 1
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					mouseHeld=1
					mouseJustPressed = 1
			
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					mouseHeld = 0
					mouseJustRelease = 1
		
		mx,my = pygame.mouse.get_pos()
		
		cardHeldIndex = mellowGUI.reorgSouthCards(mx, my, mouseJustPressed, mouseHeld, mouseJustRelease, cardHeldIndex)
		
		
		#END React to user events:
		
		#Print Stuff:
		
		mellowGUI.fill_background()
		
		mellowGUI.screen.blit(mellowLogo, (0, 0, 500, 500), (0, 0, 500, 500))
		mellowGUI.screen.blit(versNumber, (20, 50, 500, 500), (0, 0, 500, 500))
		
		
		mellowGUI.printScore()
		
		mellowGUI.printSouthCards(mx, my)
		mellowGUI.printWestCards()
		mellowGUI.printNorthCards()
		mellowGUI.printEastCards()
		
		mellowGUI.printTricks()
		
		mellowGUI.displayCenterGameMsg()
		
		#Print colour of cursor depending on what user does:
		if mouseJustPressed == 1 or mouseJustRelease==1:
			mellowGUI.screen.blit(mellowGUI.greendot, (mx-5, my-5), (0, 0, 10, 10))
		elif mouseHeld == 1:
			mellowGUI.screen.blit(mellowGUI.reddot, (mx-5, my-5), (0, 0, 10, 10))
		else:
			mellowGUI.screen.blit(mellowGUI.dot, (mx-5, my-5), (0, 0, 10, 10))
		#end print colour of cursor.
		
		
		if mellowGUI.isWaitingForBid() == 1:
			mellowGUI.displayBidChoices()
		elif mellowGUI.isWaitingForAlternativeBids() == 1:
			mellowGUI.displayAlternativeBidChoices()
			mellowGUI.displayRebidAndNextButtons()
		
		pygame.display.update()
		
		
		mouseJustPressed = 0
		mouseJustRelease = 0
		
		#End print stuff.
		
		#Update to next frame:
		
		mellowGUI.updateLastFrameTime()
		clock.tick(1000/MellowGUI.FRAME_WAIT_TIME)
	
	
	mellowGUI.gameOver = 1

if __name__ == "__main__":
	args = sys.argv
	
	
	#parse arguments:
	for x in range (0, len(args)):
		print str(args[x])
	
	main()
	