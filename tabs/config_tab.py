from PyQt5.QtWidgets import *
from widgets.cluster_display import ClusterDisplay
from PyQt5 import Qt,QtCore, QtGui
import model
from functools import partial
import json

class PipeLineWidget(QWidget):
    def __init__(self, itemList):
        super(PipeLineWidget, self).__init__()
        layout = QHBoxLayout()
        self.items = itemList
        self.estmList  = QComboBox()
        self.estmList.activated.connect(self.itemSelected)
        self.estmList.addItems([name for name, clf in itemList])
        self.paramsTable = QTableWidget()
        self.paramsTable.setMaximumHeight(150)
        layout.addWidget(self.estmList)
        layout.addWidget(self.paramsTable)
        self.setLayout(layout)
    def itemSelected(self):
        for name, model in self.items: 
            if(self.estmList.itemText(self.estmList.currentIndex()) == name):
                self.model = model()
                self.name = name
                break
        paramDict = self.model.get_params()
        self.paramsTable.setColumnCount(len(paramDict))
        self.paramsTable.setRowCount(len(paramDict))
        for i, names in enumerate(paramDict.keys()):
            label = QTableWidgetItem(names)
            value = QTableWidgetItem(str(paramDict[names]))
            label.setFlags(QtCore.Qt.ItemIsEnabled)
            self.paramsTable.setItem(0,i,label)
            self.paramsTable.setItem(1,i,value)
        
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
        self.queryGroupBox.setMaximumWidth(1000)
        self.queryGroupBox.setMaximumHeight(1000)
        self.horizontalGroupBox = QGroupBox("Configuration")
        self.horizontalGroupBox.setMaximumWidth(1000)
        self.horizontalGroupBox.setMaximumHeight(1000)
        self.advanceConfigGroupBox = QGroupBox("Advance config")
        self.advanceConfigGroupBox.setMaximumWidth(1000)
        self.advanceConfigGroupBox.setMaximumHeight(1000)
        layout = QGridLayout()
        querylayout = QGridLayout()
        mainConfigLayout = QVBoxLayout()
        configInfoLayout = QVBoxLayout()
        self.configLayout = QVBoxLayout()
        configButtonLayout = QHBoxLayout()
        mainConfigLayout.addLayout(configInfoLayout)
        mainConfigLayout.addLayout(self.configLayout)
        mainConfigLayout.addLayout(configButtonLayout)
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
        #Advance config 
        self.configNameWidget = QLineEdit("")
        self.errTextMessageWidget = QLabel("")
        self.configLayout.addWidget(PipeLineWidget(self.model.getAllEstimators()))
        self.addMorePipeReq = QPushButton("+")
        self.removeMorePipeReq = QPushButton("-")
        self.makePipeWidget = QPushButton("Ok")
        self.addMorePipeReq.clicked.connect(self.addMorePipe)
        self.removeMorePipeReq.clicked.connect(self.removePipe)
        self.makePipeWidget.clicked.connect(self.makePipeline)
        configButtonLayout.addWidget(self.addMorePipeReq)
        configButtonLayout.addWidget(self.removeMorePipeReq)
        configButtonLayout.addWidget(self.makePipeWidget)
        configInfoLayout.addWidget(self.configNameWidget)
        configInfoLayout.addWidget(self.errTextMessageWidget)
        #Setup main layout and widgets
        self.queryGroupBox.setLayout(querylayout)
        self.advanceConfigGroupBox.setLayout(mainConfigLayout)
        self.horizontalGroupBox.setLayout(layout)
        self.mainLayoutClusterList.addWidget(self.horizontalGroupBox)
        #self.mainLayoutClusterList.addWidget(self.queryGroupBox) 
        self.mainLayoutClusterList.addWidget(self.advanceConfigGroupBox)
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
    
    def addMorePipe(self):
        self.configLayout.addWidget(PipeLineWidget(self.model.getAllEstimators()))

    def removePipe(self):
        amount = self.configLayout.count()
        if(amount > 0):
            self.configLayout.itemAt(amount-1).widget().setParent(None)
    def makePipeline(self):
        amount = self.configLayout.count()
        name = self.configNameWidget.text()
        if(amount > 0 and name != ""):
            pipList = []
            for i in range(amount):
                pipList.append((self.configLayout.itemAt(i).widget().name,self.configLayout.itemAt(i).widget().model))
            if( self.model.makePipeline(pipList, name) == False ):
                self.errTextMessageWidget.setText("Model with this name already exists!")
            else:
                self.errTextMessageWidget.setText("Done")
        else:
            self.errTextMessageWidget.setText("No item in config or name not given")

    def clear_layout(self, layout):
    #Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
