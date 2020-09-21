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
		self.currentPhoto = ""
		self.type = ""
		self.model = model.modelImage()
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
		self.photoInfoFrame.setMaximumWidth(525)
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
		self.clusterInfoLayout.addWidget(QPushButton("Next cluster"), 0,0,1,2)
		self.clusterNameWidget = QLabel("Cluster Name: ")
		self.clusterTypeWidget = QLabel("Type: ")
		self.clusterImageAmountWidget = QLabel("Image amount: ")
		self.clusterInfoLayout.addWidget(self.clusterNameWidget, 1,0,1,2)
		self.clusterInfoLayout.addWidget(self.clusterTypeWidget, 2, 0)
		self.clusterInfoLayout.addWidget(self.clusterImageAmountWidget, 2,1)
		self.dropDown = QComboBox()
		self.dropDown.addItem("Clean")
		self.dropDown.addItem("Dirty")
		self.dropDown.addItem("Broken")
		self.clusterInfoLayout.addWidget(self.dropDown, 3,0,1,2)
		self.clusterInfoLayout.addWidget(QPushButton("tag cluster"), 4,0,1,2)
		self.clusterInfoFrame.setLayout(self.clusterInfoLayout)

		#Photo info
		self.photoInfoLayout = QGridLayout()
		self.getNextPhotoButton = QPushButton("Next random photo") 
		self.filenameLabel = QLabel("File name: ")
		self.mostSimilarToLabel = QLabel("Tag recommended: ")
		self.photoInfoLayout.addWidget(self.getNextPhotoButton, 0,0,1,2)
		self.photoInfoLayout.addWidget(QPushButton("Get outlier"), 1,0,1,2)
		self.photoInfoLayout.addWidget(self.filenameLabel, 2,0,1,2)
		self.photoInfoLayout.addWidget(self.mostSimilarToLabel, 3,0,1,2)
		self.photoDropDown = QComboBox()
		self.photoDropDown.addItem("Clean")
		self.photoDropDown.addItem("Dirty")
		self.photoDropDown.addItem("Broken")
		self.photoInfoLayout.addWidget(self.photoDropDown, 4,0,1,2)
		self.photoInfoLayout.addWidget(QPushButton("tag image"), 5,0,1,2)
		self.photoInfoFrame.setLayout(self.photoInfoLayout)
		##buttonsetup
		self.getNextPhotoButton.clicked.connect(self.getPhoto)
		#setup
		self.setLayout(self.mainLayout)

	def getPhoto(self):
		newImage = self.model.get_cluster_image(self.clusterName)
		self.imageDisplay.setPhotoPath(newImage)
		self.filenameLabel.setText("File name: " + newImage.split("\\")[-1])
		return newImage

	def newClusterRequest(self, clusterName):
		self.clusterName = clusterName
		self.clusterNameWidget.setText("Cluster Name: " + clusterName)
		imgType = self.getPhoto()
		imgType = imgType.split("\\")[-1]
		imgType = imgType.split("_")
		self.clusterTypeWidget.setText("Type: " + imgType[0])

	def clear_layout(self, layout):
	#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)