from PyQt5.QtWidgets import *
from widgets.cluster_display import ClusterDisplay
from PyQt5 import Qt,QtCore, QtGui
import model
from functools import partial
import json
"""
QUESTION : Why importing widgets module work in this case!
"""
class RowInformtionWidget(QWidget):
	def __init__(self, parent, setSize=1000):
		super(RowInformtionWidget, self).__init__(parent)
		self._setup(setSize)
	def _setup(self,setSize=1000):
		if(setSize != None):
			self.setMaximumWidth(setSize)
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)


class ClusterListTab(QWidget):
	def __init__(self,parent):
		super(ClusterListTab, self).__init__(parent)
		self.model = model.modelImage()
		self.parent = parent
		self.__UIsetup__()		
		self.setConfigOptions()

	def __UIsetup__(self):
		self.mainLayoutClusterList = QGridLayout()
		#Location [row]
		self.locationInputUI = RowInformtionWidget(self)
		self.locationInputField = QLineEdit()
		self.locationInputUI.layout.addWidget(QLabel("Location:- "))
		self.locationInputUI.layout.addWidget(self.locationInputField)
		#Create structure [row]
		self.creteStructureInputUI = RowInformtionWidget(self)
		self.createStructureYes = QRadioButton("Yes")
		self.createStructureNo  = QRadioButton("No")
		self.creteStructureInputUI.layout.addWidget(QLabel("Structure Directory before cluster?"))
		self.creteStructureInputUI.layout.addWidget(self.createStructureYes)
		self.creteStructureInputUI.layout.addWidget(self.createStructureNo)
		#Choose config [row]
		self.configInputUI = RowInformtionWidget(self)
		self.configInputSelection = QComboBox()	
		self.configInputSelection.setMinimumWidth(300)	
		self.configInputSummary = QTextEdit()
		font = QtGui.QFont()
		font.setPointSize(10)
		self.configInputSummary.setFont(font)
		self.configInputSummary.setReadOnly(True)
		self.configInputSummary.setMaximumHeight(300)
		self.configInputUI.layout.addWidget(QLabel("Config :- "))
		self.configInputUI.layout.addWidget(self.configInputSelection)
		self.configInputUI.layout.addWidget(self.configInputSummary)
		self.initiateClusterButton = QPushButton("Start clustering")
		self.initiateClusterButton.clicked.connect(self.startClusteringProcess)
		#Console output text area [row]
		self.consoleOutputUI = RowInformtionWidget(self)
		self.consoleOutputArea = QTextEdit()
		self.consoleOutputArea.setReadOnly(True)
		self.consoleOutputArea.setMinimumWidth(500)
		self.consoleOutputArea.setMaximumHeight(500)
		self.consoleOutputUI.layout.addWidget(self.consoleOutputArea)
		#Set main layout
		self.mainLayoutClusterList.addWidget(self.locationInputUI, 0,0)
		self.mainLayoutClusterList.addWidget(self.creteStructureInputUI,1,0)
		self.mainLayoutClusterList.addWidget(self.configInputUI,2,0)
		self.mainLayoutClusterList.addWidget(self.initiateClusterButton,3,0)
		self.mainLayoutClusterList.addWidget(self.consoleOutputUI,4,0)
		self.setLayout(self.mainLayoutClusterList)


	def setConfigOptions(self):
		self.configValue = self.model.getAllConfigs() #Give List of config names and thier contents
		try:
			self.configInputSelection.clear()
		except:
			pass
		self.configInputSelection.addItems([keys for keys in self.configValue])
		self.displayConfigSummary()
	
	def displayConfigSummary(self):
		jsonVal = self.configValue[self.configInputSelection.itemText(self.configInputSelection.currentIndex())]
		self.configInputSummary.setText(json.dumps(jsonVal, indent=4))

	def startClusteringProcess(self):
		path = self.locationInputField.text().strip()
		structure = self.createStructureYes.isChecked()
		configFile = self.configInputSelection.itemText(self.configInputSelection.currentIndex())
		self.model.clusterProcess(path,structure,configFile)

	def clear_layout(self, layout):
	#Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
		for i in reversed(range(layout.count())): 
			layout.itemAt(i).widget().setParent(None)
