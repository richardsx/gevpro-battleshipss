#!/opt/local/bin/python3.4
# Josine Rawee en Richards Zheng

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
		
		# maakt een widget waar de gebruiker zijn schepen kan neerzetten
		self.setGeometry(150, 150, 600, 600)
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		self.stylesheet = open(os.getcwd() + '/styles.qss').read()
		self.bord = {}
		
		# maakt 100 hokjes om de boten te plaatsen
		for rij in range(10):
			for kolom in range(0, 10):
				coordinaten = (rij, kolom)
				self.bord[coordinaten] = QtGui.QPushButton(str(rij) + ":" + str(kolom))
				self.bord[coordinaten].clicked.connect(lambda c, x = rij, y = kolom: self.plaatsboot(x, y))
				self.grid.addWidget(self.bord[coordinaten], rij, kolom)
				self.bord[coordinaten].setStyleSheet(self.stylesheet)
				self.bord[coordinaten].setObjectName('normaalbord')

		# maakt een knop om de boot neer te zetten
		self.plaats = QtGui.QPushButton('Plaats boot!', self)
		self.plaats.setObjectName('MenuButton')
		self.plaats.clicked.connect(self.maakbootdict)
		self.plaats.clicked.connect(self.feedback)
		self.plaats.setEnabled(False)
		
		# maakt een dictionary voor de boten
		self.botendict = {5: 'vijf', 4: 'vier', 3: 'drie', 2: 'twee'}
		self.coordboten = {}
		self.lengteboot = list(self.botendict.keys())
		
		# maakt labels
		self.feedback = QtGui.QLabel('klik waar je wilt dat de boot begint', self)
		self.feedback2 = QtGui.QLabel('De boten worden automatisch horizontaal geplaatst,\n let op dat je genoeg ruimte hebt rechts van het geklikte hokje, zodat de boot niet van het bord af valt',self)
		
		# maakt startknop
		self.startGame = QtGui.QPushButton('Spelen', self)
		self.startGame.setObjectName('MenuButton')
		self.startGame.setEnabled(False)
		self.startGame.clicked.connect(self.start)
		
		# voegt onderdelen toe aan widget
		self.grid.addWidget(self.plaats, 0, 11)
		self.grid.addWidget(self.startGame, 1, 11)
		self.grid.addWidget(self.feedback, 2, 11)
		self.grid.addWidget(self.feedback2, 3, 11)
		self.setWindowTitle("Zeeslag")
		self.show()
		
		# plaats boot
	def plaatsboot(self, x, y):
		self.rij = y
		self.kolom = x
		self.schipcoordinaten = []
		for i in range(self.lengteboot[0]):
			self.schipcoordinaten.append((int(self.kolom), int(self.rij) + int(i)))
		self.plaats.setEnabled(True)
		for a in self.coordboten.values():
			for b in a:
				self.kleur(b)
		
		# zet de geplaatste boten in een dictionary
	def maakbootdict(self):
		if self.schipcoordinaten != []:
			self.coordboten[self.botendict[self.lengteboot[0]]] = self.schipcoordinaten
		
			if len(self.lengteboot) >= 2:
				self.lengteboot.pop(0)
			elif len(self.lengteboot) == 1:
				self.lengteboot.pop(0)
				self.plaats.setEnabled(False)
				self.startGame.setEnabled(True)
				self.feedback.setText('Je kan beginnen!')
				
		# vertel de gebruiker wat hij/zij moet doen
	def feedback(self):
		if len(self.coordboten) == 1:
			self.feedback.setText('Klik op de beginplaats van de boot met een lengte van 3')
		if len(self.coordboten) == 2:
			self.feedback.setText('Klik op de beginplaats van de boot met een lengte van 4')
		if len(self.coordboten) == 3:
			self.feedback.setText('Klik op de beginplaats van de boot met een lengte van 5')
		if len(self.coordboten) == 4:
			self.feedback.setText('Je kan beginnen!')
		
		# verandert kleur van de geselecteerde hokjes
	def kleur(self, coordinaten):
		self.bord[coordinaten].setObjectName('Ship')
		self.bord[coordinaten].setStyleSheet(self.stylesheet)

		# plaatst random boten op de computer zijn veld
	def AIboten(self):
		self.AIbootCoords = {}
		lengte = [5,4,3,3,2]
		for i in lengte: # per boot
			self.checkAIoverlap(i)
		return self.AIbootCoords
		
	def checkAIoverlap(self, aantalboten):
		while(True):
				startX = randrange(10)
				startY = randrange(12,18)
				length = 0
				templist = []
				coordsList = [] # maak een lege coordinatenlijst
				for j in range(aantalboten): # per coordinaat vd boot
					if not ((int(startX),int(startY)+int(j)) in coordsList): # als de huidige coordinaat nog beschikbaar is
						length += 1
						templist.append((int(startX),int(startY)+int(j)))  
						if length == aantalboten: # in het geval dat alle coordinaten van boot i goed zijn
							coordsList.extend(templist)
							self.AIbootCoords[aantalboten] = coordsList
							return self.AIbootCoords		
							
		# verlaat het scherm wanneer alle boten zijn geplaatst en opent het speelscherm					
	def start(self):
		self.close()
		spelen.Zeeslag(self.coordboten, self.AIboten())
		
def main(argv):
		
	app = QtGui.QApplication(sys.argv)
	ex = Boten()
	sys.exit(app.exec_())
	
main(sys.argv)
