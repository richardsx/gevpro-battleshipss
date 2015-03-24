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
		self.gekleurdeboot()
		self.show()

		
	def schiet(self, x, y):
		"""computer schiet op een random vakje"""
		self.checkShips(x, y, self.computerboot, self.computersveld)
		autox, autoy = self.random()
		time.sleep(1)
		self.checkShips(autox, autoy, self.jouwboot, self.jouwveld)

	def random(self):
		return randrange(10), randrange(10)

	def gekleurdeboot(self):
		"""zorgt ervoor dat jouw geplaatse boten rood zijn"""
		for l in self.jouwboot.values():
			for c in l:
				self.kleurboot(c)
	def kleurboot(self, coordinaten):
		self.jouwveld[coordinaten].setObjectName('Ship')
		self.jouwveld[coordinaten].setStyleSheet(self.stylesheet)

	def checkShips(self, x, y, coords, field):
		"""checkt of je raak hebt geschoten"""
		click = (x, y)
		print(coords)
		for ship, coordinaten in coords.items():
			for el in coordinaten:
				if click == el:
					field[el].setObjectName('raak')
					field[el].setStyleSheet(self.stylesheet)
					coordinaten.remove(el)
					self.checkDestroyed(coords)
					return True
				else: 
					"""als je mis schiet wordt het beschoten vakje grijs"""
					field[click].setObjectName('mis')
					field[click].setStyleSheet(self.stylesheet)
					return False

	def checkDestroyed(self, coords):
		"""kijkt of je het hele schip kapot hebt gemaakt """
		#dit werkt maar 1x?
		self.feedback.setText("deze boot is nog niet gezonken")
		for ship, coordinaten in coords.items():
			if coords.get(ship) == []:
				self.feedback.setText("deze boot is gezonken")

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	game = Zeeslag()
	game.show()
	app.exec_()
