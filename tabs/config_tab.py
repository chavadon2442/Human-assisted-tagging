from PyQt5.QtWidgets import *
from widgets.cluster_display import ClusterDisplay
from PyQt5 import Qt,QtCore, QtGui
import model
from functools import partial
import json
import os
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
        return (self.estimator[0], self.estimator[1]())

class RowWidget(QWidget):
    def __init__(self, parent):
        super(RowWidget, self).__init__(parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

class ConfigTab(QWidget):
    def __init__(self,parent, threadpool, db):
        super(ConfigTab, self).__init__(parent)
        self.model = model.modelImage(db)
        self.parent = parent
        self.threadpool = threadpool
        self.__UIsetup__()
    def __UIsetup__(self):
        #Main: init and setting layout
        self.mainLayoutClusterList = QHBoxLayout()
        #self.mainLayoutClusterList.setAlignment(QtCore.Qt.AlignCenter)
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
        self.filterDescriptionBox.setStyleSheet("font-size: 25px; font-family: "'Times New Roman'", Times, serif; font-weight: 350;")
        self.filterConsole = QLabel()
        ###Filter: item reaction!
        self.filterAddPipeButton.clicked.connect(self.addPipe)
        self.filterRemovePipeButton.clicked.connect(self.removePipe)
        self.filterCreatePipeButton.clicked.connect(self.createPipe)
        ###Filter: add item to dropdown#
        #self.filterViewDropDown.addItems(views)
        tags = ["ANY"] + self.model.DB.query_alltag() 
        self.filterTagDropDown.addItems(tags)
        ###Filter: Adding items to layout
        self.filterLayout.addWidget(QLabel("Name: "), 0,0)
        self.filterLayout.addWidget(self.filterNameUI, 0,1,1,4)
        #self.filterLayout.addWidget(QLabel("View: "), 1,0)
        #self.filterLayout.addWidget(self.filterViewDropDown, 1,1)
        self.filterLayout.addWidget(QLabel("Focus tag: "), 1,0)
        self.filterLayout.addWidget(self.filterTagDropDown, 1,1)
        self.filterLayout.addWidget(self.filterTrainableCheck, 1,3)
        self.filterLayout.addWidget(QLabel("Description: "), 2,0)
        self.filterLayout.addWidget(self.filterDescriptionBox, 2,1,1,4)
        self.filterLayout.addWidget(self.filterConsole, 5,0)
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


        ##TESTING FILTER:
        self.testFilterBox = QGroupBox("Test Filter")
        self.testFilterBox.setMaximumWidth(500)
        self.testFilterBox.setMaximumHeight(500)
        self.testFilterLayout = QVBoxLayout()
        ##TESTING FILTER: ITEMS
        self.selectLocationButton = QPushButton("Browse location")
        self.locationInputField = QLineEdit()
        self.filterListOption = QComboBox()
        self.filterParamListOptions = QComboBox()
        self.filterParamDetailButton = QPushButton("See Param")
        self.locationInputField.setReadOnly(True)
        self.locationInputField.setStyleSheet("color: black; background-color: rgba(0,0,0,0.15);")
        self.testFilterViewOption = QComboBox()
        self.testFilterPiplineOption = QComboBox()
        self.testFilterFocusName = QLabel()
        self.testFilterDescription = QTextEdit()
        self.testFilterViewOption = QComboBox()
        self.startFilteringButton = QPushButton("Start filtering!")
        self.transformProgress = QProgressBar(self)
        self.learningProgress = QProgressBar(self, textVisible=False)
        self.testFilterDescription.setReadOnly(True)
        self.testFilterDescription.setStyleSheet("color: black; background-color: rgba(0,0,0,0.15);")
        ##adding data to widgets
        self.startFilteringButton.clicked.connect(self.startFilteringProcess)
        view = self.model.DB.query("SELECT * FROM Image_views")
        [self.testFilterViewOption.addItem(v[0]) for v in view]
        #self.testFilterViewOption.addItems(view)
        self.selectLocationButton.clicked.connect(self.getDirectoryLocation)
        self.filterParamDict = self.model.getFilterAndParams()
        self.filterListOption.addItems(self.filterParamDict.keys())
        self.setupFilterInfo()
        self.filterListOption.activated.connect(self.setupFilterInfo)
        ##Setting up widgets
        row1 = RowWidget(self)
        row1.layout.addWidget(QLabel("Choose filter: "), 0, 0)
        row1.layout.addWidget(self.filterListOption, 0, 1)
        row1.layout.addWidget(QLabel("Choose params"), 0, 2)
        row1.layout.addWidget(self.filterParamListOptions, 0, 3)
        row1.layout.addWidget(self.filterParamDetailButton , 0, 4)
        row2 = RowWidget(self)
        row2.layout.addWidget(self.locationInputField, 0, 0)
        row2.layout.addWidget(self.selectLocationButton, 0, 1)
        row3 = RowWidget(self)
        row3.layout.addWidget(QLabel("Focus: "), 0, 0)
        row3.layout.addWidget(self.testFilterFocusName, 0, 1)
        row4 = RowWidget(self)
        row4.layout.addWidget(QLabel("Choose view"), 0, 0)
        row4.layout.addWidget(self.testFilterViewOption, 0, 1)
        row5 = RowWidget(self)  
        row5.layout.addWidget(QLabel("Description: "), 0, 0)
        row5.layout.addWidget(self.testFilterDescription, 0, 1)
        row6 = RowWidget(self)  
        row6.layout.addWidget(QLabel("Transform progress: "), 0, 0)
        row6.layout.addWidget(self.transformProgress, 0, 1)
        row7 = RowWidget(self)  
        row7.layout.addWidget(QLabel("Learning progress: "), 0, 0)
        row7.layout.addWidget(self.learningProgress, 0, 1)
        ##TESTING FILTER: add to layout
        self.testFilterLayout.addWidget(row1)
        self.testFilterLayout.addWidget(row3)
        self.testFilterLayout.addWidget(row2)
        self.testFilterLayout.addWidget(row4)
        self.testFilterLayout.addWidget(row5)
        self.testFilterLayout.addWidget(self.startFilteringButton)
        self.testFilterLayout.addWidget(row6)
        self.testFilterLayout.addWidget(row7)


        ###Filter: Setting layout and adding to main layout
        self.filterGroupBox.setLayout(self.filterLayout)
        self.testFilterBox.setLayout(self.testFilterLayout)
        self.mainLayoutClusterList.addWidget(self.filterGroupBox)
        self.mainLayoutClusterList.addWidget(self.testFilterBox)


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
        tag = self.filterTagDropDown.itemText(self.filterTagDropDown.currentIndex())
        create_req = self.model.makePipeline(piplist=pipline, name=name, descript=description, tag=tag, trainable=int(trainable == True))
        if(create_req == 0):
            self.resetAll()
        elif(create_req == -1):
            self.filterConsole.setText("Name already exists!")

    
    def resetAll(self):
        for index in range(len(self.filterPipeList)):
            self.removePipe()
        self.filterNameUI.setText("")
        self.filterDescriptionBox.clear()
        self.filterConsole.setText("CREATED SUCCESSFULLY!")

    def updateFilterList(self):
        print(self.model.DB.getAllFilter())

    def setupFilterInfo(self):
        curFilter = self.filterListOption.itemText(self.filterListOption.currentIndex())
        params = self.filterParamDict[curFilter]["params"]
        if(self.filterParamListOptions.count() > 0 ):
            self.filterParamListOptions.clear()
        self.filterParamListOptions.addItems(params)
        self.testFilterFocusName.setText(self.filterParamDict[curFilter]["focus"])
        self.testFilterDescription.setPlainText(self.filterParamDict[curFilter]["descript"])

    def getDirectoryLocation(self):
        fileLocal = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if(fileLocal != None and fileLocal != ""):
            self.locationInputField.setText(fileLocal)

    def startFilteringProcess(self):
        curFilter = self.filterListOption.itemText(self.filterListOption.currentIndex())
        curParam = self.filterParamListOptions.itemText(self.filterParamListOptions.currentIndex())
        selectedView = self.testFilterViewOption.itemText(self.testFilterViewOption.currentIndex())
        imageLocation = os.path.join(self.locationInputField.text(), selectedView)
        filterFile = self.model.getAndSetFilter(curFilter, curParam)
        noTransform = self.model.filterInfoCheck(imgLocal=imageLocation, filtername=curFilter, paramname=curParam, view=selectedView)
        if(noTransform != -1):
            self.startFilteringButton.setEnabled(False)
            filterThread = model.FilteringThread(filterFile, imageLocation, noTransform=noTransform)
            self.threadpool.start(filterThread)
            filterThread.signals.transformSignal.connect(self.progressBarHandle)
            filterThread.signals.learningSignal.connect(self.learningBarHandle)
        else:
            print("Working with same imagelocation, filter, parameter and view!")
    
    def progressBarHandle(self, message):
        if(message[0] == "size"):
            self.transformProgress.setMaximum(message[1])
            self.transformProgress.setValue(0)
        else:
            maxx = self.transformProgress.maximum()
            self.transformProgress.setValue(min(maxx, message[1]))

    def learningBarHandle(self, message):
        if(message[0] == "ended"):
            self.learningProgress.setMaximum(1)
            self.learningProgress.setValue(1)
            self.startFilteringButton.setEnabled(True)
        else:
            self.learningProgress.setMaximum(message[1])

    def clear_layout(self, layout):
    #Code reference [ https://www.semicolonworld.com/question/58072/clear-all-widgets-in-a-layout-in-pyqt ]
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)



    