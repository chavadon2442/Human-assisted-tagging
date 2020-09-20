from PyQt5.QtWidgets import *
from widgets.cluster_display import ClusterDisplay
from PyQt5 import Qt,QtCore
import model
from functools import partial

"""
QUESTION : Why importing widgets module work in this case!
"""

class ClusterListTab(QWidget):
	def __init__(self,parent):
		super(ClusterListTab, self).__init__(parent)
		self.model = model.modelImage()
		self.parent = parent
		self.__UIsetup__()
	def __UIsetup__(self):
		self.mainLayoutClusterList = QVBoxLayout()
		self.topLayout = QHBoxLayout()
		self.clusterDisplayLayout = QVBoxLayout()
		self.mainLayoutClusterList.addLayout(self.topLayout)
		self.mainLayoutClusterList.addLayout(self.clusterDisplayLayout)
		self.locationLineEdit = QLineEdit("") 
		self.locSearchButton = QPushButton("Search")
		self.configButton = QPushButton("Config")
		self.locSearchButton.clicked.connect(self.request_cluster_display)
		self.topLayout.addWidget(self.locationLineEdit)
		self.topLayout.addWidget(self.locSearchButton)
		self.topLayout.addWidget(self.configButton)
		scrollArea = QScrollArea()
		self.contentInScroll = QWidget(scrollArea)
		self.imageLayout = QGridLayout()
		self.contentInScroll.setLayout(self.imageLayout)
		scrollArea.setWidget(self.contentInScroll)
		scrollArea.setWidgetResizable(True)
		scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.clusterDisplayLayout.addWidget(scrollArea)
		self.setLayout(self.mainLayoutClusterList)
	
	def clear_layout(self, layout):
	#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)
	def request_cluster_display(self):
		COLAMT = 3
		location = self.locationLineEdit.text()
		if(location):
			self.clear_layout(self.imageLayout)
			images = self.model.request_cluster_images(location, amount=10)
			SIZE = 600
			if(len(images) < 3):
				SIZE = 1920//len(images)
			for i,img in enumerate(images):
				row = i//COLAMT
				col = i%COLAMT
				displayImg = ClusterDisplay(imageLoc=images[img], title=img, imgSize=SIZE)
				displayImg.button.clicked.connect(partial(self.parent.switch_cluster_and_tab, img)) 
				self.imageLayout.addWidget(displayImg,row,col)
				self.imageLayout.setColumnMinimumWidth(col,500)
				self.imageLayout.setRowMinimumHeight(row,500)
				self.locationLineEdit.setText("")
