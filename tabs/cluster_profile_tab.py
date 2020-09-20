from PyQt5.QtWidgets import *
from PyQt5 import Qt,QtCore
from PyQt5.QtGui import QIcon, QPixmap, QFont
from functools import partial
from widgets.image_display import imageDisplay




class ClusterProfileTab(QWidget):
	def __init__(self,parent):
		super(ClusterProfileTab, self).__init__(parent)
		self.parent = parent
		self.__UIsetup__()
	def __UIsetup__(self):
		#Layout
		self.mainLayout = QHBoxLayout()
		self.imageLayout = QVBoxLayout()
		self.infoLayout = QVBoxLayout()
		#Set Layout
		self.mainLayout.addLayout(self.imageLayout)
		self.mainLayout.addLayout(self.infoLayout)
		#Info layout
		self.clusterInfoFrame = QFrame()
		self.photoInfoFrame = QFrame()
		self.clusterInfoFrame.setMaximumWidth(525)
		self.clusterInfoFrame.setStyleSheet("background-color: rgba(250, 252, 171,0.3)")
		self.photoInfoFrame.setMaximumWidth(525)
		self.photoInfoFrame.setStyleSheet("background-color: rgba(250, 252, 171,0.3)")
		self.infoLayout.addWidget(self.clusterInfoFrame)
		self.infoLayout.addWidget(self.photoInfoFrame)
		#Image 
		self.imageLayout.addWidget(imageDisplay())
		#Cluster info
		self.clusterInfoLayout = QGridLayout()
		self.clusterInfoLayout.addWidget(QLabel("Cluster Name: "), 0,0,1,2)
		self.clusterInfoLayout.addWidget(QLabel("Type: Bottom"), 1, 0)
		self.clusterInfoLayout.addWidget(QLabel("Image amount: 1244"), 1,1)
		self.dropDown = QComboBox()
		self.dropDown.addItem("Clean")
		self.dropDown.addItem("Dirty")
		self.dropDown.addItem("Broken")
		self.clusterInfoLayout.addWidget(self.dropDown, 2,0,1,2)
		self.clusterInfoLayout.addWidget(QPushButton("tag cluster"), 3,0,1,2)
		self.clusterInfoFrame.setLayout(self.clusterInfoLayout)
		#setup
		self.setLayout(self.mainLayout)
	
	def clear_layout(self, layout):
	#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)