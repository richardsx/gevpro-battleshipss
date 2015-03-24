#!/opt/local/bin/python3.4
from collections import Counter
import sys
import os, sys
from PyQt4 import QtCore, QtGui
import spelen
from random import randrange
class Boten(QtGui.QWidget):
	
	def __init__ (self):
		super(Boten,self).__init__()
		self.initUI()

	def initUI(self):
		"""maakt een widget waarin de gebruiker zijn schepen kan neerzetten"""
		
		self.setGeometry(150, 150, 600, 600)
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		self.stylesheet = open(os.getcwd() + '/styles.qss').read()
		self.bord = {}
		
		for rij in range(10):
			for kolom in range(0, 11):
				coordinaten = (rij, kolom)
				self.bord[coordinaten] = QtGui.QPushButton(str(rij) + ":" + str(kolom))
				self.bord[coordinaten].clicked.connect(lambda c, x=rij, y=kolom: self.plaatsboot(x, y))
				self.grid.addWidget(self.bord[coordinaten], rij, kolom)
				self.bord[coordinaten].setStyleSheet(self.stylesheet)
				self.bord[coordinaten].setObjectName('normaalbord')

		"""maakt een knop om de boot neer te zetten"""
		self.plaats = QtGui.QPushButton('Plaats boot!', self)
		self.plaats.setObjectName('MenuButton')
		self.plaats.clicked.connect(self.maakbootdict)
		self.plaats.setEnabled(False)
		
		"""maakt een dictionary voor de boten"""
		self.botendict = {5: "vijf", 4: "vier", 3: "drie", 2: "twee"}
		self.coordboten = {}
		self.lengteboot = list(self.botendict.keys())
		
		"""maakt feedback labels"""
		self.feedback = QtGui.QLabel('klik waar je wilt dat de boot begint', self)
		self.feedback2=QtGui.QLabel('De boten worden automatisch horizontaal geplaatst',self)
		
		"""maakt een knop om het spel te starten"""
		self.startGame = QtGui.QPushButton('Spelen', self)
		self.startGame.setObjectName('MenuButton')
		self.startGame.setEnabled(False)
		self.startGame.clicked.connect(self.start)
		
		"""voegt alle onderdelen toe aan widget"""
		self.grid.addWidget(self.plaats, 0, 11)
		self.grid.addWidget(self.startGame, 1, 11)
		self.grid.addWidget(self.feedback, 2, 11)
		self.grid.addWidget(self.feedback2, 3, 11)
		self.setWindowTitle("Zeeslag")
		self.show()
		
	def plaatsboot(self, x, y):
		"""Zet een boot neer"""
		self.rij = y
		self.kolom = x
		self.schipcoordinaten = []
		for i in range(self.lengteboot[0]):
			self.schipcoordinaten.append((int(self.kolom), int(self.rij) + int(i)))
		self.plaats.setEnabled(True)
		for l in self.coordboten.values():
			for c in l:
				self.kleur(c)
		
	def maakbootdict(self):
		"""Zet de coordinaten van neergezette boot in een dictionairy"""
		if self.schipcoordinaten != []:
			self.coordboten[self.botendict[self.lengteboot[0]]] = self.schipcoordinaten
		
			if len(self.lengteboot) >= 2:
				self.lengteboot.pop(0)
			elif len(self.lengteboot) == 1:
				self.lengteboot.pop(0)
				self.plaats.setEnabled(False)
				self.startGame.setEnabled(True)
				self.feedback.setText('Je kan beginnen!')
		
	def feedback(self):
		"""vertelt de gebruiker wat hij moet doen"""
		if len(self.coordboten)==1:
			self.feedback.setText('Klik op de beginplaats van de boot met een lengte van 3')
		if len(self.coordboten)==2:
			self.feedback.setText('Klik op de beginplaats van de boot met een lengte van 4')
		if len(self.coordboten)==3:
			self.feedback.setText('Klik op de beginplaats van de boot met een lengte van 5')
		if len(self.coordboten)==4:
			self.feedback.setText('Je kan beginnen!')
			
	def kleur(self, coordinaten):
		"""verandert de kleur van de aangeklikte tegels."""
		self.bord[coordinaten].setObjectName('Ship')
		self.bord[coordinaten].setStyleSheet(self.stylesheet)

	def AIboten(self):
		"""zet random boten neer voor de computer """
		self.AIbootCoords={}
		lengte = [5,4,3,3,2]

		while lengte != []:
			coordsList = []
			direction = randrange(2)
			
			startX = randrange(10)
			startY = randrange(12,21)
			
			for i in range(lengte[0]):
				coordsList.append((int(startX), int(startY) + int(i)))
			
			self.AIbootCoords[lengte[0]] = coordsList
			lengte.pop(0)
		return self.AIbootCoords

	def start(self):
		"""verlaat het scherm van boten neerzetten en opent het speelscherm"""
		self.close()
		spelen.Zeeslag(self.coordboten, self.AIboten())
		
def main(argv):
		
	app = QtGui.QApplication(sys.argv)
	ex = Boten()
	sys.exit(app.exec_())
	
main(sys.argv)
