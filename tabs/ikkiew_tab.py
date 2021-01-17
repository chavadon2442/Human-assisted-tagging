from PyQt5.QtWidgets import *
from widgets.cluster_display import ClusterDisplay
from PyQt5 import Qt,QtCore, QtGui, QtWidgets
import model
from functools import partial
import json
import webbrowser
import requests
import win32api
import threading


class IkkiewTab(QWidget):
	def __init__(self,parent, threadpool, db):
		super(IkkiewTab, self).__init__(parent)
		self.model = model.modelImage(db)
		self.parent = parent
		self.threadpool = threadpool
		self.__UIsetup__()
		

		
		
	
	
	def __UIsetup__(self):
		f=open("version.txt","r")
		
		response = requests.get('https://raw.githubusercontent.com/adarsh2012/Human-assisted-tagging/deploy_experiment/version.txt')
		data = response.text
		self.mainLayoutClusterList = QGridLayout()

		#Set main layout
		self.mainLayoutClusterList.addWidget(QLabel("Current Version"),0,0)
		self.mainLayoutClusterList.addWidget(QLabel(str(f.read())), 1,0)
		
		self.mainLayoutClusterList.addWidget(QPushButton("Check Update"),2,0)
		self.mainLayoutClusterList.addWidget(QLabel("New version"),3,0)
		self.mainLayoutClusterList.addWidget(QLabel(str(data)),4,0)
		self.setLayout(self.mainLayoutClusterList)


	def clear_layout(self, layout):
	#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)



	
	
	
	


