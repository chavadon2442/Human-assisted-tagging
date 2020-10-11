import os, shutil
import random
import cv2
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import json
from PyQt5 import Qt,QtCore, QtGui
from clusterLogic.model import View_cluster
import time

class cluster:
    def __init__(self):
        self.paths = []
        self.images = []
        self.imgAmtRequired = 30
    def addPath(self, path):
        self.paths.append(path)
    def addImages(self):
        amtFromEach = self.imgAmtRequired//len(self.paths)
        for path in self.paths:
            imgs = os.listdir(path)
            try:
                self.images = self.images +  random.sample(imgs, amtFromEach)
            except:
                self.images = self.images + imgs
            for i,localImgPath in enumerate(self.images):
            	self.images[i] = os.path.join(path, localImgPath)
        self.imgAmt = len(self.images)
    def removeImages(self, index):
        self.images.pop(index)
        self.imgAmt -= 1
        if(len(self.images) < 1):
            self.addImages()


class modelImage:
	def __init__(self):
		self.storageLocation = "./system information/"
		self.configLocation = "./system information/Config"
	def get_cluster_list(self, listLocation):
		pass
	def request_cluster_images(self, clusterLocation, amount="all"):
		imageDict = dict()
		clusters = os.listdir(clusterLocation)
		self.storeInfo(clusterPath=clusterLocation,clusterList=clusters)
		for cluster in clusters:
			clusterImages = os.listdir(clusterLocation+"\\"+cluster)
			clusterLen = len(clusterImages)
			if(amount=="all"):
				amount = clusterLen
			imageDict[cluster] = [clusterLocation+"\\"+cluster+"\\"+clusterImages[random.randint(0,clusterLen-1)] for i in range(amount)]
		return imageDict

	def request_dissimilar_images(self, clusterName):
		#[ (imagelocation, percentageDissimilar), (imagelocation, percentageDissimilar), (imagelocation, percentageDissimilar)... ]
		pass

	def get_cluster_image(self,clusterName,amount=1):
		data = self.getInfo()
		filePath =  data["clusterPath"] + "\\" + clusterName + "\\"
		return filePath + random.choice(os.listdir(filePath))


	def storeInfo(self, clusterPath, clusterList):
		data = dict()
		data["clusters"] = clusterList
		data["clusterPath"] = clusterPath
		with open(self.storageLocation, 'w') as outputfile:
			json.dump(data, outputfile)

	def getInfo(self):
		with open(self.storageLocation)  as inputFile:
			data = json.load(inputFile)
		return data

	def request_dissimilar_images(self, clusterName):
		#[ (imagelocation, percentageDissimilar), (imagelocation, percentageDissimilar), (imagelocation, percentageDissimilar)... ]
		pass

	def quant(self,image,cluster,isArr):
		if(not isArr):
			image = cv2.imread(image)
		(h,w) = image.shape[:2]
		image = image.reshape((image.shape[0] * image.shape[1], 3))
		clt = MiniBatchKMeans(n_clusters = 4)
		labels = clt.fit_predict(image)
		quant = clt.cluster_centers_.astype("uint8")[labels]
		quant = quant.reshape((h, w, 3))
		image = image.reshape((h, w, 3))
		quantized_image = np.hstack([image, quant])
		return quant


	def brightness(self, image, isArr=False, alpha=1.0, beta=0.0):
		print("asdad")
		if(not isArr):
			image = cv2.imread(image)
		result = cv2.addWeighted(image,alpha,np.zeros(image.shape,image.dtype),0,beta)		
		return result


	def getAllClusterLocal(self):
		with open(self.storageLocation + "cluster_info.json") as configData:
			information = json.load(configData)
			MAINPATH =  information["cluster_location"]
		return MAINPATH
		
	def get_views_clusters(self):
		with open(self.storageLocation + "cluster_info.json") as configData:
			information = json.load(configData)
			MAINPATH =  information["cluster_location"]
		#GET ALL DIRECTORIES
		VIEWS = [files  for files in os.listdir(MAINPATH) if files.find(".") == -1]
		VIEW_AND_CLUSTERS = dict()
		for directs in VIEWS:
		    VIEW_PATH  = os.path.join(os.path.abspath(MAINPATH), directs)
		    CLUSTERS = dict({})
		    #get all cluster of particular view
		    for root, subdirs, files in os.walk(VIEW_PATH):
		        for items in files:
		            if(items.find(".tiff") != -1):
		                clusterName = root.split("\\")[-1]
		                if(clusterName not in CLUSTERS):
		                    CLUSTERS[clusterName] = cluster()
		                CLUSTERS[clusterName].addPath(root)
		                break
		    #set up images for that cluster
		    for cls in CLUSTERS:
		        CLUSTERS[cls].addImages()
		    VIEW_AND_CLUSTERS[directs] = CLUSTERS
		return VIEW_AND_CLUSTERS

	def getAllConfigs(self):
		returnVAl = {}
		for conf in os.listdir(self.configLocation):
			with open(os.path.join(self.configLocation, conf)) as values:
				#confName = conf[:conf.find(".")]
				values = json.load(values)
				returnVAl[conf] = values
		return returnVAl

	def tagCluster(self, view, paths, tag):
		with open(os.path.join(self.storageLocation, "cluster_info.json")) as data:
			data = json.load(data)
			tagLocation = data["datasetLocation"]
		view_loc = os.path.join(tagLocation, view)
		if not os.path.exists(view_loc):
			os.mkdir(view_loc)
		tag_sub_loc = os.path.join(view_loc, tag)
		if not os.path.exists(tag_sub_loc):
			os.mkdir(tag_sub_loc)
		for pt in paths:
			allImgs = os.listdir(pt)
			allImgs = [os.path.join(pt, imgName) for imgName in allImgs]
			[ shutil.move(imgPath, tag_sub_loc) for imgPath in allImgs ]
			os.rmdir(pt)

	def validLocationCheck(self, location):
		try:
			os.listdir(location)
			return True
		except:
			return False


class threadSignals(QtCore.QObject):
	finished = QtCore.pyqtSignal()
	updateInfo = QtCore.pyqtSignal(str)
class ClusteringThread(QtCore.QRunnable):
	def __init__(self,path,structure,configFile):
		super(ClusteringThread, self).__init__()
		self.path = path
		self.structure = structure
		self.configFile = configFile
		self.signals = threadSignals()
		self.configLocation = "./system information/Config" ###########EITHER STORE CONFIG LOCATION SOMEWHERE OR MAKE IT FIXED##########################
	@QtCore.pyqtSlot()
	def run(self):
		configFileName = os.path.join(self.configLocation,self.configFile) 
		with open(configFileName) as vwConfig:
			vwConfig = json.load(vwConfig)
		all_views = [os.path.join(self.path,vw) for vw in os.listdir(self.path) if vw.find(".") == -1]
		for viewPath in all_views:
			vwName = os.path.split(viewPath)[-1] # get tail of path
			update = "Working on "+ vwName
			self.signals.updateInfo.emit(update)
			self.signals.updateInfo.emit("{} ==CONFIG==> {}".format(vwName, vwConfig[vwName]))
			vwClass = View_cluster(vwName, viewPath, self.signals)
			vwClass.START(model=vwConfig[vwName]["model"], isSave=vwConfig[vwName]["isSave"], k=vwConfig[vwName]["k"], focusPoint=vwConfig[vwName]["focusPoint"])
		self.signals.finished.emit()



if __name__ == "__main__":
	modelClass = modelImage()
	imges = modelClass.getAllConfigs()
	print(imges)