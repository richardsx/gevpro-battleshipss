#!/opt/local/bin/python3.4

from PyQt4 import QtGui, QtCore
import os, sys
import time
from random import randrange


class Zeeslag(QtGui.QWidget):
	def __init__(self, jouwboot, computerboot):
		super(Zeeslag, self).__init__()
		self.jouwboot = jouwboot
		self.computerboot = computerboot
		self.initUI()

	def initUI(self):
		"""maakt het de layout van het speelveld"""
		self.setWindowTitle("Zeeslag")
		self.setGeometry(1000, 1000, 1000, 1000)
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		self.stylesheet = open(os.getcwd() + '/styles.qss').read()
		self.userLabel = QtGui.QLabel('Jouw veld')
		self.botLabel = QtGui.QLabel('Computers veld')
		self.feedback = QtGui.QLabel(' ')
		self.feedback2=QtGui.QLabel(' hoi')
		
		"""maakt 100 vakjes voor jou en 100 voor computer"""
		self.jouwveld = {}
		for row in range(10):
			for column in range(1, 11):
				coordinaten = (row, column)
				self.jouwveld[coordinaten] = QtGui.QPushButton(str(row) + ":" + str(column))
				self.jouwveld[coordinaten].setStyleSheet(self.stylesheet)
				self.jouwveld[coordinaten].setObjectName('normaalbord')
				self.grid.addWidget(self.jouwveld[coordinaten], row, column)

		self.computersveld = {}
		for row in range(10):
			for column in range(12, 22):
				coordinaten = (row, column)
				self.computersveld[coordinaten] = QtGui.QPushButton(str(row) + ":" + str(column))
				self.computersveld[coordinaten].setStyleSheet(self.stylesheet)
				self.computersveld[coordinaten].setObjectName('normaalbord')
				self.grid.addWidget(self.computersveld[coordinaten], row, column)
				"""geeft coordinaten van waar jij hebt geschoten, en schiet vervoglens op jouw veld"""
				self.computersveld[coordinaten].clicked.connect(lambda c, x=row, y=column: self.schiet(x, y))
				
				
		"""voegt alles toe aan de widget"""
		self.grid.addWidget(self.userLabel, 0, 0)
		self.grid.addWidget(self.botLabel, 0, 11)
		self.grid.addWidget(self.feedback,1,11)
		self.grid.addWidget(self.feedback2,1,0)
		self.gekleurdeboot()
		self.show()

		
	def schiet(self, x, y):
		"""computer schiet op een random vakje"""
		if (self.controleer(x, y, self.computerboot, self.computersveld)) == True:
			self.computersveld[x,y].setObjectName('raak')
			self.computersveld[x,y].setStyleSheet(self.stylesheet)
			self.feedback.setText("raak")
			self.checkDestroyed(self.computerboot)
		else:
			self.computersveld[x,y].setObjectName('mis')
			self.computersveld[x,y].setStyleSheet(self.stylesheet)
			self.feedback.setText("mis")
		autox, autoy = self.random()
		if (self.controleer(autox, autoy, self.jouwboot, self.jouwveld)) == True:
			self.feedback2.setText("raak")
			self.jouwveld[autox, autoy].setObjectName('raak')
			self.jouwveld[autox, autoy].setStyleSheet(self.stylesheet)
			self.checkDestroyed2(self.jouwboot)
		else:
			self.jouwveld[autox, autoy].setObjectName('mis')
			self.jouwveld[autox, autoy].setStyleSheet(self.stylesheet)
			self.feedback2.setText("mis")

	def random(self):
		return randrange(10), randrange(1,10)

	def gekleurdeboot(self):
		"""zorgt ervoor dat jouw geplaatse boten rood zijn"""
		for a in self.jouwboot.values():
			for b in a:
				self.kleurboot(b)
	def kleurboot(self, coordinaten):
		self.jouwveld[coordinaten].setObjectName('Ship')
		self.jouwveld[coordinaten].setStyleSheet(self.stylesheet)

	def controleer(self, x, y, coords, field):
		"""checkt of je raak hebt geschoten"""
			
		print(coords)
		click = (x, y)
		coordsList = []
		for i in coords.values():
			for j in i:
				coordsList.append(j)
			
		for ship, coordinaten in coords.items():
			for element in coordinaten:
				if element == (click):
					coordinaten.remove(element)
					print(coordinaten)
					
		for a in coordsList:
			if a == click:
				return True
		

	def checkDestroyed(self, coords):
		"""kijkt of je het hele schip kapot hebt gemaakt """
		if 2 in coords:
			if coords[2]== []:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[2]
		if 3 in coords:
			if coords[3] == []:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[3]
		if 4 in coords:
			if coords[4]==[]:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[4]
		if 5 in coords:
			if coords[5]==[]:
				self.feedback.setText("deze boot is gezonken")
				del self.computerboot[5]
		if self.computerboot=={}:
			self.feedback.setText("Je hebt gewonnen")
			
			
	def checkDestroyed2(self, coords):
		"""kijkt of je het hele schip kapot hebt gemaakt """
		print("hallo")
		if 2 in coords:
			if coords[2]== []:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[2]
		if 3 in coords:
			if coords[3] == []:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[3]
		if 4 in coords:
			if coords[4]==[]:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[4]
		if 5 in coords:
			if coords[5]==[]:
				self.feedback2.setText("deze boot is gezonken")
				del self.jouwboot[5]
		if self.jouwboot=={}:
			self.feedback.setText("Je hebt verloren")
			

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	game = Zeeslag()
	game.show()
	app.exec_()
