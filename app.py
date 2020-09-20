from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import Qt,QtCore
from tabs.cluster_list_tab import ClusterListTab
from tabs.cluster_profile_tab import ClusterProfileTab
import os
import sys


class MainWindow(QWidget):
	def __init__(self, width, height, title, pos = [0,0]):
		super(MainWindow, self).__init__()
		self.setWindowTitle(title)
		self.setWindowIcon(QIcon('./localmedia/icon.png')) 
		self.setGeometry(pos[0],pos[1],width,height)
		self.__setupUI__() 
		
	def __setupUI__(self):
		self.mainLayout = QVBoxLayout()
		self.windowTab = QTabWidget(self)
		self.clusterListTab = ClusterListTab(self)
		self.clusterProfileTab = ClusterProfileTab(self)
		self.windowTab.addTab(self.clusterListTab, "Cluster location")
		self.windowTab.addTab(self.clusterProfileTab, "Cluster profile")
		self.mainLayout.addWidget(self.windowTab)
		self.setLayout(self.mainLayout)
	def switch_cluster_and_tab(self, name):
		self.clusterProfileTab.label.setText("Cluster " +  name)
		self.windowTab.setCurrentIndex(1)




if (__name__ == "__main__"):
	app = QApplication(sys.argv)
	window = MainWindow(width=1920, height=1080, title="Cluster assistant")
	window.show()
	sys.exit(app.exec_())