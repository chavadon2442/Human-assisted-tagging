from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import Qt,QtCore
import os
import sys
import model



class ClusterDisplay(QLabel):
	def __init__(self, imageLoc, title):
		super(ClusterDisplay, self).__init__()
		self.len = len(imageLoc)
		self.index = 0
		self.title = title
		self.imageLocList = imageLoc
		self.__display__()
		self.__timerSetup__()
	def __display__(self):
		self.layout = QVBoxLayout()
		self.ImageLabel = QLabel()
		self.setImg()
		self.layout.addWidget(self.ImageLabel)
		self.layout.addWidget(QPushButton("Cluster: " +  self.title))
		self.setLayout(self.layout)
	def setImg(self):
		image = QPixmap(self.imageLocList[self.index]).scaledToWidth(500)
		self.ImageLabel.setPixmap(image)
		self.index = (self.index + 1) % self.len
	def __timerSetup__(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.setImg)
		self.timer.start(5000)

class MainWindow(QScrollArea):
	def __init__(self, width, height, title, pos = [0,0]):
		super(MainWindow, self).__init__()
		self.setWindowTitle(title)
		self.setWindowIcon(QIcon('icon.png')) 
		self.setGeometry(pos[0],pos[1],width,height)
		self.model = model.modelImage()
		self.__setupUI__()

	def __setupUI__(self):
		widget = QWidget()
		self.mainLayout = QVBoxLayout(widget)
		self.topLayout = QHBoxLayout()
		self.clusterDisplayLayout = QVBoxLayout()
		#contruct layout
		self.mainLayout.addLayout(self.topLayout)
		self.mainLayout.addLayout(self.clusterDisplayLayout)
		self.setWidget(widget)
		self.setWidgetResizable(True)
		#add widget
			#Top layout
		self.locationLineEdit = QLineEdit("") 
		self.locSearchButton = QPushButton("Search")
		self.configButton = QPushButton("Config")
		self.locSearchButton.clicked.connect(self.requestClusterDisply)
		self.topLayout.addWidget(self.locationLineEdit)
		self.topLayout.addWidget(self.locSearchButton)
		self.topLayout.addWidget(self.configButton)
			#Cluster
		self.imageLayout = QGridLayout()
		self.frame = QFrame()
		self.frame.setFrameShape(QFrame.StyledPanel)
		self.frame.setLineWidth(1)
		self.frame.setLayout(self.imageLayout)
		self.clusterDisplayLayout.addWidget(self.frame)
		#set main layout 
		self.setLayout(self.mainLayout)
		################SCROLL#######################
		self.scroll = QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		# self.scroll.setWidget()
		self.scroll.setWidgetResizable(True)
        ################SCROLL#######################
	def clearLayout(self, layout):
		#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)

	def requestClusterDisply(self):
		# Give me images for each cluster 
		COLAMT = 4
		location = self.locationLineEdit.text()
		if(location):
			images = self.model.requestClusterImages(location, amount=10)
			for i,img in enumerate(images):
				row = i//COLAMT
				col = i%COLAMT
				self.imageLayout.addWidget(ClusterDisplay(imageLoc=images[img], title=img),row,col)
				self.locationLineEdit.setText("")



if (__name__ == "__main__"):
	app = QApplication(sys.argv)
	window = MainWindow(width=1920, height=1080, title="Cluster assistant")
	window.show()
	sys.exit(app.exec_())