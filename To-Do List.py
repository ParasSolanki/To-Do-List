import sys
import os
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QLabel, QDateTimeEdit
from PyQt5.QtWidgets import QMenuBar, QMessageBox, QDialog, QVBoxLayout, QAction
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):
	switch_window = QtCore.pyqtSignal()
	def __init__(self):
		super().__init__()
		self.title = "To-Do List"                # set title..
		self.left = 70                          # x-pos when you open application..
		self.top = 60                          # y-pos when you open application..
		self.width = 500                     # width of the application..
		self.height = 500                    # height of the application..
		self.fName = 'To-Do List File.txt'                     # set file name when you save your file..
		self.uncompletedTaskFile, self.completedTaskFile = 'UncompletedTask.txt', 'CompletedTask.txt'
		self.initUI()                # initialize the UI of the application..

	def makeLabel(self, x, y, text):         # make label method...
		self.taskLabel = QLabel(self)
		self.taskLabel.setText(text)
		self.taskLabel.move(x, y)

	def createTaskFile(self):
		if not os.path.exists(self.uncompletedTaskFile) and not os.path.exists(self.completedTaskFile):
			with open(self.uncompletedTaskFile, 'w') as f:
				f.close()
			with open(self.completedTaskFile, 'w') as g:
				g.close()

	def setMenuBarAction(self):              # add Action to the menu bar...
		self.saveAction = QAction('Save', self)         # save Action..
		self.saveAction.setStatusTip('Sae The To-Do')
		self.saveAction.setShortcut("Ctrl+S")
		self.saveAction.triggered.connect(self.saveFile)

		self.saveAllAction = QAction('Save All', self)         # save All Action..
		self.saveAllAction.setStatusTip('Save All To-Do')
		self.saveAllAction.triggered.connect(self.saveAllFile)

		self.exitAction = QAction('Exit', self)          # Exit Action..
		self.exitAction.setStatusTip('Exit')
		self.exitAction.triggered.connect(self.exitApp)

		self.aboutToDo = QAction('About To-Do List', self)              # About Action..
		self.aboutToDo.triggered.connect(self.aboutInfo)
		

	def appMenuBar(self):
		menuBar = self.menuBar()                   # Create Menu Bar..

		self.setMenuBarAction()                       # Set Action for Menu Bar..

		self.homeMenu = menuBar.addMenu('File')                # Set File Menu to The MenuBar..
		self.helpMenu = menuBar.addMenu('Help')                    # Set Help Menu to The MenuBar..
 
		self.homeMenu.addAction(self.saveAction)                # Save Action Added to File Menu..
		self.homeMenu.addAction(self.saveAllAction)                 # Save All Action Added to File Menu..
		self.homeMenu.addAction(self.exitAction)                   # Exit Action Added to File Menu..
	
		self.helpMenu.addAction(self.aboutToDo)                    # Abouut Action Added to Help Menu..

	def initUI(self):
		self.setWindowTitle(self.title)                            # Set title for the Application.. 
		self.setWindowIcon(QIcon("./logo.png"))                               # set Icon for the Application
		self.setGeometry(self.left, self.top, self.width, self.height)                  # set app size..
		self.setMaximumSize(QtCore.QSize(self.width, self.height))                # disabling Application Maximize button..

		self.appMenuBar()                                # Set application MenuBar..
		self.createTaskFile()                                # creating Task File for application..
	 
		# Task Text Input..
		self.taskText = QLineEdit(self)
		self.taskText.move(10, 45)
		self.taskText.resize(self.width//2-20, 50)
		self.taskText.setPlaceholderText('Enter Task Here..')

		# setting up uncompleted task text Area...
		self.textArea = QTextEdit(self)
		self.textArea.setReadOnly(True)                           # readonly text area..
		self.textArea.move(self.width//2, 45)
		self.textArea.resize(self.width//2-2, self.height-50)
		self.textArea.setLineWrapMode(QTextEdit.NoWrap)	
		self.textArea.setTextColor(QColor(180, 0, 0))                # give font color to red..
		self.textArea.setFontPointSize(10)                              # font size = 10..

		# make Labels.....
		self.makeLabel(10, 21, 'Add Task Here')
		self.makeLabel(self.width//2, 20, 'Uncompleted Task')
		self.makeLabel(5, self.height//2-15, 'Completed Task List')
		self.makeLabel(10, 95, 'Set Reminder')

		# setting up completed task text Area..
		self.completedtextArea = QTextEdit(self)
		self.completedtextArea.setReadOnly(True)                     # readonly text area..
		self.completedtextArea.move(5, self.height//2+10)
		self.completedtextArea.resize(self.width//2-13, self.height//2-15)
		self.completedtextArea.setLineWrapMode(QTextEdit.NoWrap)
		self.completedtextArea.setTextColor(QColor(0, 180, 0))                  # give font color to green..
		self.completedtextArea.setFontPointSize(10)                         # font size = 10..

		self.dateTimeBox = QDateTimeEdit(self)
		self.dateTimeBox.setGeometry(10, 125, 140, 25)

		self.loadTask()                      # loading preveiously stord To-Do Task..
 
		self.Buttons()                        # make all the buttons for the Application..

		self.show()                           # display the application..a

	def Buttons(self):
		# Add To-Do Button
		self.addButton = QPushButton("Add To-Do", self)
		self.addButton.move(15, 164)

		# Add Clear All Button
		self.clearAllButton = QPushButton("Clear All", self)
		self.clearAllButton.move(130, 164)

		# Adding Mark All Completed Button..
		self.completedButton = QPushButton("Mark All Completed", self)
		self.completedButton.move(58, 203)
		self.completedButton.resize(140, 30)

		# Button events..
		self.addButton.clicked.connect(self.onClick)
		self.clearAllButton.clicked.connect(self.clearAll)
		self.completedButton.clicked.connect(self.completeTask)

	def loadTask(self):
		if os.path.exists(self.uncompletedTaskFile):
			with open(self.uncompletedTaskFile, 'r') as f:
				text = f.read()
				if text != '':
					self.textArea.append(text)
		if os.path.exists(self.completedTaskFile):
			with open(self.completedTaskFile, 'r') as g:
				texts = g.read().split('\n')
				for text in texts:
					if text != '':
						self.completedtextArea.append(text)

	@pyqtSlot()
	def saveFile(self):
		file = self.textArea.toPlainText()
		try:
			fHandle = open(self.fName, 'a')
			fHandle.write(file)
		except:
			with open(self.fName, 'w') as f:
				f.write(file)
		fHandle.close()

	@pyqtSlot()
	def saveAllFile(self):
		uncompletedToDOText = self.textArea.toPlainText()
		completedToDOText = self.completedtextArea.toPlainText()
		if uncompletedToDOText  == '':                      # if there is no task in uncompleted task list then skip it..
			with open(self.fName, 'w') as f:
				f.write('Completed To-Do Task:\n\n')
				f.write(completedToDOText)
		elif completedToDOText == '':                        # if there is no task in completed task list then skip it..
			with open(self.fName, 'w') as f:
				f.write('Uncompleted To-Do Task:\n\n')
				f.write(uncompletedToDOText +'\n\n')
		else:
			with open(self.fName, 'w') as f:                   # both..
				f.write('Uncompleted To-Do Task:\n\n')
				f.write(uncompletedToDOText +'\n\n')
				f.write('Completed To-Do Task:\n\n')
				f.write(completedToDOText)

	@pyqtSlot()
	def aboutInfo(self):

		msg = QMessageBox()
		msg.setWindowTitle('To-Do List')
		msg.setGeometry(280, 190, 500, 420)
		msg.setWindowIcon(QIcon('logo.png'))
		msg.setText('''Add Your Daily To-Do Task \n   Bulid With Python & PyQt5.
			        ''')
		msg.exec_()



	@pyqtSlot()
	def exitApp(self):
		sys.exit()               # exit from the App..

	@pyqtSlot()
	def onClick(self):
		textvalue = self.taskText.text()
		date = self.dateTimeBox.date()
		time = self.dateTimeBox.time()
		text = f'{textvalue}  Date: {date.toPyDate()} Time: {time.toPyTime()}\n'            # convert to string..
		if textvalue == '':                                        # If textvalue in taskText is blank then return don't update textArea..
			return
		else:
			if os.path.exists(self.uncompletedTaskFile):
				with open(self.uncompletedTaskFile, 'a') as f:
					f.write(text)
			else:
				with open(self.uncompletedTaskFile, 'w') as f:
					f.write(text)
			self.textArea.append(text) 	                       # else update textArea..
			self.taskText.setText('')                          #clear taskText..

	@pyqtSlot()
	def clearAll(self):
		self.textArea.setText('')                             # clear uncompleted task list textArea..
		self.completedtextArea.setText('')                    # clear completed task list textArea..
		with open(self.uncompletedTaskFile, 'w') as f, open(self.completedTaskFile, 'w') as g:
			f.close()
			g.close()


	@pyqtSlot()
	def completeTask(self):
		textValue = self.textArea.toPlainText()                   # get uncompleted task list text..
		with open(self.uncompletedTaskFile, 'r+') as g:
			dataFile = g.read().split('\n')
			texts = textValue.split('\n')
			for text in texts:
				for data in dataFile:
					if data.startswith(text):
						g.truncate(0)
		if textValue == '':
			return 
		else:
			if os.path.exists(self.completedTaskFile):
				with open(self.completedTaskFile, 'a') as f:
					texts = textValue.split('\n')
					for text in texts:
						if text != '':
							f.write(textValue)
			else:
				with open(self.completedTaskFile, 'w') as f:
					texts = textValue.split('\n')
					for text in texts:
						if text != '':
							f.write(textValue)
			texts = textValue.split('\n')
			for text in texts:
				if text != '':
					self.completedtextArea.append(text)                   # append to completed task list section..
			self.textArea.setText('')


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())              # exit app..
