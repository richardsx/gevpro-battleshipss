#!/opt/local/bin/python3.4
# Josine Rawee en Richards Zheng

from PyQt4 import QtGui, QtCore
import os, sys
from random import randrange


class Zeeslag(QtGui.QWidget):
	
	def __init__(self, jouwboot, computerboot):
		super(Zeeslag, self).__init__()
		self.jouwboot = jouwboot
		self.computerboot = computerboot
		self.initUI()

	# maakt het speelveld en voegt labels toe
	def initUI(self):
		self.setWindowTitle("Zeeslag")
		self.setGeometry(1000, 1000, 1000, 1000)
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		self.stylesheet = open(os.getcwd() + '/styles.qss').read()
		self.userLabel = QtGui.QLabel('Jouw veld')
		self.botLabel = QtGui.QLabel('Computers veld')
		self.feedback = QtGui.QLabel(' ')
		self.feedback2 = QtGui.QLabel(' ')
		self.setObjectName('achtergrond')
		self.setStyleSheet(self.stylesheet)
		
		# maakt hokjes om het spel te spelen
		# 100 voor de user en 100 voor de computer
		self.spelersveld = {}
		for rij in range(10):
			for kolom in range(1, 11):
				coordinaten = (rij, kolom)
				self.spelersveld[coordinaten] = QtGui.QPushButton(str(rij) + ":" + str(kolom))
				self.spelersveld[coordinaten].setStyleSheet(self.stylesheet)
				self.spelersveld[coordinaten].setObjectName('normaalbord')
				self.grid.addWidget(self.spelersveld[coordinaten], rij, kolom)

		self.computersveld = {}
		for rij in range(10):
			for kolom in range(12, 22):
				coordinaten = (rij, kolom)
				self.computersveld[coordinaten] = QtGui.QPushButton(str(rij) + ":" + str(kolom))
				self.computersveld[coordinaten].setStyleSheet(self.stylesheet)
				self.computersveld[coordinaten].setObjectName('normaalbord')
				self.grid.addWidget(self.computersveld[coordinaten], rij, kolom)
				
				# geeft de coordinaten door en schiet vervolgens op het hokje waar je op hebt geklikt
				# computer schiet terug op jouw veld
				self.computersveld[coordinaten].clicked.connect(lambda c, x = rij, y = kolom: self.schiet(x, y))
					
		# voegt onderdelen toe aan widget
		self.grid.addWidget(self.userLabel, 0, 0)
		self.grid.addWidget(self.botLabel, 0, 11)
		self.grid.addWidget(self.feedback,1,11)
		self.grid.addWidget(self.feedback2,1,0)
		self.gekleurdeboot()
		self.show()

	#kleurt jouw eerder geplaatste boten rood
	def gekleurdeboot(self):
		for a in self.jouwboot.values():
			for b in a:
				self.kleurboot(b)
	def kleurboot(self, coordinaten):
		self.spelersveld[coordinaten].setObjectName('Ship')
		self.spelersveld[coordinaten].setStyleSheet(self.stylesheet)
		
	# schiet op het hokje waar je op geklikt hebt
	# zet de feedbacklabel naar 'raak' wanneer deze raak is en kleurt het hokje groen
	# zet de feedbacklabel naar 'mis' wanneer deze mis is en kleurt het hokje grijs
	def schiet(self, x, y):
		if (self.controleer(x, y, self.computerboot, self.computersveld)) == True:
			self.computersveld[x,y].setObjectName('raak')
			self.computersveld[x,y].setStyleSheet(self.stylesheet)
			self.feedback.setText("raak")
			self.checkDestroyed(self.computerboot)
		else:
			self.computersveld[x,y].setObjectName('mis')
			self.computersveld[x,y].setStyleSheet(self.stylesheet)
			self.feedback.setText("mis")
			
		# schiet willeukeurig voor de computer, random gegenereerde x en y
		# doet het zelfde voor de kleur van het hokje en feedbacklabel als voor de gebruiker
		autox, autoy = self.random()
		if (self.controleer(autox, autoy, self.jouwboot, self.spelersveld)) == True:
			self.feedback2.setText("raak")
			self.spelersveld[autox, autoy].setObjectName('raak')
			self.spelersveld[autox, autoy].setStyleSheet(self.stylesheet)
			self.checkDestroyedAI(self.jouwboot)
		else:
			self.spelersveld[autox, autoy].setObjectName('mis')
			self.spelersveld[autox, autoy].setStyleSheet(self.stylesheet)
			self.feedback2.setText("mis")

	# returnt willekeurige coordinaten voor de computer
	def random(self):
		return randrange(10), randrange(1,10)

	# controleert of een gedeelte van het schip geraakt is
	# returnt true als dit zo is
	def controleer(self, x, y, coords, field):
		print(coords)
		click = (x, y)
		coordsList = []
		for i in coords.values():
			for j in i:
				coordsList.append(j)
				
		#verwijdert de geraakte coordinaat uit de dictionairy.
		for ship, coordinaten in coords.items():
			for element in coordinaten:
				if element == (click):
					coordinaten.remove(element)
					print(coordinaten)
					
		for a in coordsList:
			if a == click:
				return True
		
	# controleert per schip of het hele schip van de computer geraakt is
	# als een heel schip geraakt is, wordt het label gezet naar "deze boot is gezonken"
	# wanneer alle schepen in hun geheel zijn geraakt, wordt het label gezet naar "Je hebt gewonnen"
	def checkDestroyed(self, coords):
		if 2 in coords:
			if coords[2] == []:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[2]
		if 3 in coords:
			if coords[3] == []:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[3]
		if 4 in coords:
			if coords[4] == []:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[4]
		if 5 in coords:
			if coords[5] == []:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[5]
		if self.computerboot == {}:
			self.feedback.setText("Je hebt gewonnen!! :)")
			
	# controleert per schip of het hele schip van de gebruiker geraakt is
	# als een heel schip geraakt is, wordt het label gezet naar "deze boot is gezonken"
	# wanneer alle schepen in hun geheel zijn geraakt, wordt het label gezet naar "Je hebt verloren"
	def checkDestroyedAI(self, coords):
		if 2 in coords:
			if coords[2] == []:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[2]
		if 3 in coords:
			if coords[3] == []:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[3]
		if 4 in coords:
			if coords[4] == []:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[4]
		if 5 in coords:
			if coords[5] == []:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[5]
		if self.jouwboot == {}:
			self.feedback.setText("Je hebt verloren :(")

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	game = Zeeslag()
	game.show()
	app.exec_()
