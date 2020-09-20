from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import Qt,QtCore

class imageDisplay(QLabel):
	def __init__(self):
		super(imageDisplay, self).__init__()
		self.__display__()
	def __display__(self):
		self.mainLayout = QVBoxLayout()
		self.imageLayout = QVBoxLayout()
		self.buttonLayout = QHBoxLayout()

		self.mainLayout.addLayout(self.imageLayout)
		self.mainLayout.addLayout(self.buttonLayout)

		self.ImageLabel = QLabel()
		image = QPixmap(r"D:\ClusterWork\ImageClusters\file 1\1\bottom_view_2020-05-25-13-11-32-136597_18.tiff").scaledToWidth(1300)
		self.ImageLabel.setPixmap(image)
		self.imageLayout.addWidget(self.ImageLabel)	
		self.buttonLayout.addWidget(QPushButton("Quantize"))
		self.buttonLayout.addWidget(QPushButton("Brightness +"))
		self.buttonLayout.addWidget(QPushButton("Brightness -"))	




		#set the main layout
		self.setLayout(self.mainLayout)

	def setImg(self):
		image = QPixmap(self.imageLocList[self.index]).scaledToWidth(self.widthSize)
		self.ImageLabel.setPixmap(image)
		self.index = (self.index + 1) % self.len