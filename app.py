from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import Qt,QtCore
from tabs.cluster_list_tab import ClusterListTab
from tabs.cluster_profile_tab import ClusterProfileTab
from tabs.config_tab import ConfigTab
from tabs.training_tab import TrainTab
import os
import sys

class MainWindow(QWidget):
	def __init__(self, width, height, title, pos = [0,0]):
		super(MainWindow, self).__init__()
		self.setWindowTitle(title)
		self.setWindowIcon(QIcon('./localmedia/icon.png')) 
		self.setGeometry(pos[0],pos[1],width,height)
		self.threadPool = QtCore.QThreadPool()
		self.__setupUI__() 
		
	def __setupUI__(self):
		self.mainLayout = QVBoxLayout()
		self.windowTab = QTabWidget(self)
		self.clusterListTab = ClusterListTab(self, threadpool=self.threadPool)
		self.clusterProfileTab = ClusterProfileTab(self, threadpool=self.threadPool)
		self.configTab = ConfigTab(self, threadpool=self.threadPool)
		self.trainingTab = TrainTab(self, threadpool=self.threadPool)
		self.windowTab.addTab(self.clusterListTab, "Cluster location")
		self.windowTab.addTab(self.clusterProfileTab, "Cluster profile")
		self.windowTab.addTab(self.configTab, "Configuration")
		self.windowTab.addTab(self.trainingTab, "Training")
		self.mainLayout.addWidget(self.windowTab)
		self.setLayout(self.mainLayout)
	def switch_cluster_and_tab(self, name):
		self.clusterProfileTab.newClusterRequest(name)
		self.windowTab.setCurrentIndex(1)




if (__name__ == "__main__"):
	app = QApplication(sys.argv)
	window = MainWindow(width=1920, height=1080, title="Cluster assistant")
	window.show()
	sys.exit(app.exec_())