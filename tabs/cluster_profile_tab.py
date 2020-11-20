from PyQt5.QtWidgets import *
from PyQt5 import Qt,QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QFont
from functools import partial
from widgets.image_display import imageDisplay
import model
import os

class ClusterProfileTab(QWidget):
	def __init__(self,parent, threadpool):
		super(ClusterProfileTab, self).__init__(parent)
		self.parent = parent
		self.clusterName = ""
		self.type = ""
		self.model = model.modelImage()
		self.chosenView = None
		self.threadpool = threadpool
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
		self.updateDataButton = QPushButton("Update data")
		self.updateDataButton.clicked.connect(self.__datasetup__)
		self.clusterInfoFrame.setMaximumWidth(525)
		self.photoInfoFrame.setMaximumWidth(525)
		self.clusterInfoFrame.setMaximumHeight(200)
		self.photoInfoFrame.setMaximumHeight(400)
		self.photoInfoFrame.setFrameStyle(QFrame.Panel)
		self.clusterInfoFrame.setFrameStyle(QFrame.Panel)
		self.clusterInfoFrame.setStyleSheet("QFrame {border : 2px solid rgba(220,220,200,1); background-color: rgba(220,220,220,0.1)}")
		self.photoInfoFrame.setStyleSheet("QFrame {border : 2px solid rgba(220,220,200,1); background-color: rgba(220,220,220,0.1)}")
		self.infoLayout.addWidget(self.updateDataButton)
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
		self.clusterLocationWidget = QLineEdit("")
		self.clusterLocationWidget.setStyleSheet("color: black; background-color: rgba(0,0,0,0.15);")
		self.browseClusterButton = QPushButton("Browse")
		self.clusterLocationWidget.setReadOnly(True)
		self.browseClusterButton.clicked.connect(self.getDirectoryLocation)
		self.viewList.activated.connect(self.setupClusterList)
		self.clusterList.activated.connect(self.getPhoto)
		self.clusterInfoLayout.addWidget(self.clusterLocationWidget,0,0)
		self.clusterInfoLayout.addWidget(self.browseClusterButton,0,1)
		self.clusterInfoLayout.addWidget(QLabel("View"), 1,0)
		self.clusterInfoLayout.addWidget(self.viewList, 1,1)
		self.clusterInfoLayout.addWidget(QLabel("Cluster"), 2,0)
		self.clusterInfoLayout.addWidget(self.clusterList, 2,1)
		self.clusterInfoLayout.addWidget(self.imageLabel, 3,0,2,2)
		self.clusterInfoFrame.setLayout(self.clusterInfoLayout)

		#Photo info
		self.tagButton = QPushButton("tag complete cluster")
		self.tagPhotoButton = QPushButton("tag current image")
		self.tagButton.clicked.connect(self.tagCluster)
		self.tagPhotoButton.clicked.connect(self.tagSelctedImage)
		#self.tagButton.setEnabled(False)
		self.photoInfoLayout = QGridLayout()
		self.getNextPhotoButton = QPushButton("Next photo") 
		self.photoInfoLayout.addWidget(self.getNextPhotoButton, 0,0,1,2)
		self.photoDropDown = QListWidget()
		self.photoDropDown.setSelectionMode(QListWidget.MultiSelection)
		self.photoInfoLayout.addWidget(self.photoDropDown, 1,0,1,2)
		self.photoInfoLayout.addWidget(self.tagButton, 2,0,1,2)
		self.photoInfoLayout.addWidget(self.tagPhotoButton, 3,0,1,2)
		tags  = self.model.DB.query_alltag()
		for tg in tags:
			self.photoDropDown.addItem(tg)
		self.photoDropDown.setCurrentRow(0)
		self.photoInfoFrame.setLayout(self.photoInfoLayout)
		##buttonsetup
		self.getNextPhotoButton.clicked.connect(self.getPhoto)
		#setup
		self.setLayout(self.mainLayout)


	def __datasetup__(self):
		newLocal = self.clusterLocationWidget.text()
		if(os.path.exists(newLocal) == True):
			self.viewList.clear()
			self.mainData = self.model.get_views_clusters(newLocal)
			[self.viewList.addItem(views) for views in self.mainData]
			self.setupClusterList()


	def setupClusterList(self):
		self.clusterList.clear()
		currentView, _ = self.getCurrentClusterAndView()
		clusters = self.mainData[currentView]
		[self.clusterList.addItem(cluster) for cluster in clusters]
		self.imgIndex = -1
		self.getPhoto()

	def getPhoto(self):
		currentView, currentCluster = self.getCurrentClusterAndView()
		curCluster = self.mainData[currentView][currentCluster]
		self.imgIndex = (self.imgIndex + 1) % curCluster.imgAmt
		currentImgPath = curCluster.images[self.imgIndex]
		self.imageLabel.setText(os.path.split(currentImgPath)[-1])
		self.imageDisplay.setPhotoPath(currentImgPath)
		self.tagPhotoButton.setEnabled(True)

	def tagCluster(self):
		currentView, currentCluster = self.getCurrentClusterAndView()
		tag = [item.text() for item in self.photoDropDown.selectedItems()]
		self.model.tagCluster(currentView, self.mainData[currentView][currentCluster].paths, tag)
		del self.mainData[currentView][currentCluster]
		self.setupClusterList()

	def tagSelctedImage(self):
		self.tagPhotoButton.setEnabled(False)
		currentView, currentCluster = self.getCurrentClusterAndView()
		curCluster = self.mainData[currentView][currentCluster]
		tag = [item.text() for item in self.photoDropDown.selectedItems()]
		if(self.model.tagImage(currentView, curCluster.images[self.imgIndex], tag) == True):
			curCluster.removeImages(self.imgIndex)
			self.getPhoto()
		else:
			print("Moving images failed!")

	def getCurrentClusterAndView(self):
		return self.viewList.itemText(self.viewList.currentIndex()), self.clusterList.itemText(self.clusterList.currentIndex())

	def getDirectoryLocation(self):
		fileLocal = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		if(fileLocal != None and fileLocal != ""):
			self.clusterLocationWidget.setText(fileLocal)
			self.__datasetup__()

	def clear_layout(self, layout):
	#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)