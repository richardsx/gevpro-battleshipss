from collections import Counter
import sys
from PyQt4 import QtCore, QtGui
class Board(QtGui.QWidget):
	
	def __init__ (self):
		super(Board,self).__init__()

		self.initUI()
	def initUI(self):
		self.table = QtGui.QTableWidget(self)
		self.table.setRowCount(10)
		self.table.setColumnCount(10)
		grid=QtGui.QGridLayout()
		grid.addWidget(self.table,1,0)
		self.setLayout(grid)
		self.setGeometry(100,300,1050,400)
		self.show()
def main(argv):
		
	app = QtGui.QApplication(sys.argv)
	ex = Board()
	sys.exit(app.exec_())
	
main(sys.argv)
