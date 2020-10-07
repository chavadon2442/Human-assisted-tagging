from PyQt5.QtWidgets import *
from PyQt5 import Qt,QtCore
from PyQt5.QtGui import QIcon, QPixmap, QFont
from functools import partial
from widgets.image_display import imageDisplay
import model


class ClusterProfileTab(QWidget):
	def __init__(self,parent):
		super(ClusterProfileTab, self).__init__(parent)
		self.parent = parent
		self.clusterName = ""
		self.type = ""
		self.model = model.modelImage()
		self.chosenView = None
		self.__UIsetup__()
		self.__datasetup__()
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
		self.photoInfoFrame.setMaximumWidth(525)
		self.clusterInfoFrame.setMaximumHeight(100)
		self.photoInfoFrame.setMaximumHeight(400)
		self.photoInfoFrame.setFrameStyle(QFrame.Panel)
		self.clusterInfoFrame.setFrameStyle(QFrame.Panel)
		self.clusterInfoFrame.setStyleSheet("QFrame {border : 2px solid rgba(220,220,200,1); background-color: rgba(220,220,220,0.1)}")
		self.photoInfoFrame.setStyleSheet("QFrame {border : 2px solid rgba(220,220,200,1); background-color: rgba(220,220,220,0.1)}")
		self.infoLayout.addWidget(self.clusterInfoFrame)
		self.infoLayout.addWidget(self.photoInfoFrame)
		#Image 
		self.imageDisplay = imageDisplay() 
		self.imageLayout.addWidget(self.imageDisplay)
		#Cluster info
		self.clusterInfoLayout = QGridLayout()
		self.viewList = QComboBox()
		self.clusterList = QComboBox()
		self.imageLabel = QLabel("Image Label: ")
		self.viewList.activated.connect(self.getView)
		self.clusterList.activated.connect(self.setClusterImage)

		self.clusterInfoLayout.addWidget(QLabel("View"), 0,0)
		self.clusterInfoLayout.addWidget(self.viewList, 0,1)
		self.clusterInfoLayout.addWidget(QLabel("Cluster"), 1,0)
		self.clusterInfoLayout.addWidget(self.clusterList, 1,1)
		self.clusterInfoLayout.addWidget(self.imageLabel, 2,0,2,2)
		self.clusterInfoFrame.setLayout(self.clusterInfoLayout)

		#Photo info
		self.photoInfoLayout = QGridLayout()
		self.getNextPhotoButton = QPushButton("Next photo") 
		self.photoInfoLayout.addWidget(self.getNextPhotoButton, 0,0,1,2)
		self.photoDropDown = QListWidget()
		self.photoInfoLayout.addWidget(self.photoDropDown, 1,0,1,2)
		self.photoInfoLayout.addWidget(QPushButton("tag cluster"), 2,0,1,2)
		self.photoDropDown.addItem("Clean")
		self.photoDropDown.addItem("Dirty")
		self.photoDropDown.addItem("Broken")
		self.photoInfoFrame.setLayout(self.photoInfoLayout)
		##buttonsetup
		self.getNextPhotoButton.clicked.connect(self.getPhoto)
		#setup
		self.setLayout(self.mainLayout)

	def __datasetup__(self):
		self.mainData = self.model.get_views_clusters()
		[self.viewList.addItem(views) for views in self.mainData]
		self.getView()
	
	def getView(self): #Get view and setClusterImage is done because we QBoxList uses these functions
		self.currentView = self.viewList.itemText(self.viewList.currentIndex())
		self.setupClusterList()

	def setupClusterList(self):
		clusters = self.mainData[self.currentView]
		try:
			self.clusterList.clear()
		except:
			pass
		[self.clusterList.addItem(cluster) for cluster in clusters]
		self.setClusterImage()

	def setClusterImage(self):
		self.currentCluster = self.clusterList.itemText(self.clusterList.currentIndex())
		self.imgIndex = -1
		self.getPhoto()

	def getPhoto(self):
		curCluster = self.mainData[self.currentView][self.currentCluster]
		self.imgIndex = (self.imgIndex + 1) % curCluster.imgAmt
		imgPath = curCluster.images[self.imgIndex]

		self.imageLabel.setText("/".join(imgPath.split("/")[5:]))
		self.imageDisplay.setPhotoPath(imgPath)

	def clear_layout(self, layout):
	#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)