from PyQt5.QtWidgets import *
from widgets.cluster_display import ClusterDisplay
from PyQt5 import Qt,QtCore, QtGui
import model
from functools import partial
import json

class ConfigTab(QWidget):
    def __init__(self,parent, threadpool):
        super(ConfigTab, self).__init__(parent)
        self.model = model.modelImage()
        self.parent = parent
        self.threadpool = threadpool
        self.__UIsetup__()
    def __UIsetup__(self):
        self.mainLayoutClusterList = QVBoxLayout()
        self.mainLayoutClusterList.setAlignment(QtCore.Qt.AlignCenter)
        self.queryGroupBox = QGroupBox("Query")
        self.queryGroupBox.setMaximumWidth(750)
        self.queryGroupBox.setMaximumHeight(750)
        self.horizontalGroupBox = QGroupBox("Configuration")
        self.horizontalGroupBox.setMaximumWidth(750)
        self.horizontalGroupBox.setMaximumHeight(750)
        layout = QGridLayout()
        querylayout = QGridLayout()
        # layout.setColumnStretch(1, 4)
        # layout.setColumnStretch(2, 4)
        self.configNameInput = QLineEdit("")
        layout.addWidget(QLabel("Name: "),0,0)
        layout.addWidget(self.configNameInput,0,1)
        views = [vw + "_view"for vw in ["bottom","top", "left", "right"]]
        self.widgetMapConfig = dict()
        for index, vw in enumerate(views):
            widMap  = dict()
            modelList = QComboBox()
            kValInput = QLineEdit("10")
            modelList.addItem("resnet50")
            modelList.addItem("resnet152")
            modelList.addItem("resnet101")
            modelList.addItem("inception")
            modelList.addItem("nasnet")
            layout.addWidget(QLabel(vw),index + 1,0,1,3)
            layout.addWidget(QLabel("Model"),index + 1,4,1,1)
            layout.addWidget(modelList,index + 1,5,1,2)
            layout.addWidget(QLabel("K value"),index + 1,7,1,1)
            layout.addWidget(kValInput,index + 1,8,1,2)
            widMap["model"] = modelList
            widMap["k"] = kValInput
            self.widgetMapConfig[vw] = widMap
        self.createConfigButton = QPushButton("Create")
        self.createConfigButton.clicked.connect(self.createConfig)
        self.consoleOutput = QLabel("")
        self.consoleOutput.setMaximumHeight(50)
        layout.addWidget(self.createConfigButton, len(views)+1, 0)
        layout.addWidget(self.consoleOutput, len(views)+2, 0,1,3)
        
        #Query layout
        self.tagListWidget = QListWidget()
        self.outputLocationWidget = QLineEdit("")
        self.initiateQueryWidget = QPushButton("Start query")
        tags  = self.model.DB.query_alltag()
        for tg in tags:
            self.tagListWidget.addItem(tg)
        self.outputLocationWidget.setMaximumHeight(300)
        querylayout.addWidget(QLabel("Location to be stored:"), 0,0)
        querylayout.addWidget(self.outputLocationWidget, 1,0)
        querylayout.addWidget(self.tagListWidget, 2,0)
        querylayout.addWidget(self.initiateQueryWidget, 3,0)
        #Setup main layout and widgets
        self.queryGroupBox.setLayout(querylayout)
        self.horizontalGroupBox.setLayout(layout)
        self.mainLayoutClusterList.addWidget(self.horizontalGroupBox)
        self.mainLayoutClusterList.addWidget(self.queryGroupBox)
        self.setLayout(self.mainLayoutClusterList)


    def createConfig(self):
        config = dict()
        for vws in self.widgetMapConfig:
            vwDict = dict()
            for items in self.widgetMapConfig[vws]:
                widget = self.widgetMapConfig[vws][items]
                if(items == "model"):
                    value = widget.itemText(widget.currentIndex())
                else:
                    value = int(widget.text())
                vwDict[items] = value
            config[vws] = vwDict
            vwDict["focusPoint"] = ""
            vwDict["isSave"] = False
        if(self.configNameInput.text() == ""):
            self.consoleOutput.setText("Please give this config a name")
            return False
        result = self.model.createNewConfig(name=self.configNameInput.text(), mapVal=config)
        if(result == False):
            self.consoleOutput.setText("Config name already exists")
        else:
            self.consoleOutput.setText("Successful!")

    def clear_layout(self, layout):
    #Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
