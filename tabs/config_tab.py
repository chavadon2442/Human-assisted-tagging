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
        self.itemSelected()
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

class filterPipeItem(QWidget):
    def __init__(self, dataDict):
        super(filterPipeItem, self).__init__()
        self.data = dataDict
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        #Items
        self.typeList = QComboBox()
        self.estmList = QComboBox()
        self.typeList.addItems(self.data.keys())
        self.setData()
        self.typeList.activated.connect(self.setData)
        self.estmList.activated.connect(self.setEstm)
        #add items to layout
        self.layout.addWidget(QLabel("Type: "), 5, 0)
        self.layout.addWidget(self.typeList, 5, 1)
        self.layout.addWidget(QLabel("Function: "), 5, 2)
        self.layout.addWidget(self.estmList, 5, 3)
        self.layout.addWidget(QLabel("Params: "), 5, 4)
        self.layout.addWidget(QPushButton("select"), 5, 5)
    def setData(self):
        self.Piptype = self.typeList.itemText(self.typeList.currentIndex())
        try:
            self.estmList.clear()
        except:
            pass
        itemList = [items[0] for items in self.data[self.Piptype]]
        self.estmList.addItems(itemList)
        self.setEstm()

    def setEstm(self):
        estName = self.estmList.itemText(self.estmList.currentIndex())
        for items in self.data[self.Piptype]:
            if(items[0] == estName):
                self.estimator = items
                break
    def getVals(self):
        return self.estimator


class ConfigTab(QWidget):
    def __init__(self,parent, threadpool):
        super(ConfigTab, self).__init__(parent)
        self.model = model.modelImage()
        self.parent = parent
        self.threadpool = threadpool
        self.__UIsetup__()
    def __UIsetup__(self):
        #Main: init and setting layout
        self.mainLayoutClusterList = QVBoxLayout()
        self.mainLayoutClusterList.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayoutClusterList)
        ##Filter: groupbox
        self.filterGroupBox = QGroupBox("Filter")
        self.filterGroupBox.setMaximumWidth(1000)
        self.filterGroupBox.setMaximumHeight(1500)
        self.filterLayout = QGridLayout()
        ###Filter: items
        self.filterNameUI = QLineEdit("")
        self.filterViewDropDown = QComboBox()
        self.filterTagDropDown  = QComboBox()
        self.filterAddPipeButton  = QPushButton("add")
        self.filterRemovePipeButton  = QPushButton("remove")
        self.filterCreatePipeButton  = QPushButton("Create")
        self.filterTrainableCheck = QCheckBox("Trainable")
        self.filterDescriptionBox = QTextEdit()
        ###Filter: item reaction!
        self.filterAddPipeButton.clicked.connect(self.addPipe)
        self.filterRemovePipeButton.clicked.connect(self.removePipe)
        self.filterCreatePipeButton.clicked.connect(self.createPipe)
        ###Filter: add item to dropdown
        self.filterViewDropDown.addItems(["Top", "Bottom", "Left", "Right"])
        self.filterTagDropDown.addItems(self.model.DB.query_alltag())
        ###Filter: Adding items to layout
        self.filterLayout.addWidget(QLabel("Name: "), 0,0)
        self.filterLayout.addWidget(self.filterNameUI, 0,1,1,4)
        self.filterLayout.addWidget(QLabel("View: "), 1,0)
        self.filterLayout.addWidget(self.filterViewDropDown, 1,1)
        self.filterLayout.addWidget(QLabel("Tag: "), 1,2)
        self.filterLayout.addWidget(self.filterTagDropDown, 1,3)
        self.filterLayout.addWidget(self.filterTrainableCheck, 1,4)
        self.filterLayout.addWidget(QLabel("Description: "), 2,0)
        self.filterLayout.addWidget(self.filterDescriptionBox, 3,0,2,5)
        ####Filter: Items for pipes!
        self.filterPipeScroll = QScrollArea()
        self.filterPipeWidget = QWidget()
        self.filterPipeLayout = QVBoxLayout()
        self.filterPipeScroll.setMinimumHeight(500)
        self.filterPipeScroll.setMaximumHeight(750)
        self.filterPipeScroll.setMinimumWidth(500)
        self.filterPipeScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.filterPipeScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filterPipeScroll.setWidgetResizable(True)
        self.filterPipeWidget.setLayout(self.filterPipeLayout)
        self.filterPipeScroll.setWidget(self.filterPipeWidget)
        self.filterLayout.addWidget(self.filterPipeScroll, 5,0,2,5)
        self.filterLayout.addWidget(self.filterAddPipeButton, 7,0,1,1)
        self.filterLayout.addWidget(self.filterRemovePipeButton, 7,1,1,1)
        self.filterLayout.addWidget(self.filterCreatePipeButton, 7,4,1,1)
        #####Filter: Adding items to pipes
        self.filterPipeList = []
        ###Filter: Setting layout and adding to main layout
        self.filterGroupBox.setLayout(self.filterLayout)
        self.mainLayoutClusterList.addWidget(self.filterGroupBox)


    def addPipe(self):
        newPipe = filterPipeItem(dataDict=self.model.getAllEstimators())
        self.filterPipeList.append(newPipe)
        self.filterPipeLayout.addWidget(newPipe)

    def removePipe(self):
        try:
            targetWidget = self.filterPipeList.pop()
            targetWidget.setParent(None)
        except IndexError:
            pass
    
    def createPipe(self):
        pipline = []
        for items in self.filterPipeList:
            pipline.append(items.getVals())
        name = self.filterNameUI.text()
        description = self.filterDescriptionBox.toPlainText()
        trainable = self.filterTrainableCheck.isChecked()
        view = self.filterViewDropDown.itemText(self.filterViewDropDown.currentIndex())
        tag = self.filterTagDropDown.itemText(self.filterTagDropDown.currentIndex())

    def clear_layout(self, layout):
    #Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
