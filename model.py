import os
import random
import cv2
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import json
from PyQt5 import Qt,QtCore, QtGui

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
		self.storingFile = "./system information/currentClusterInfo.txt"

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
		with open(self.storingFile, 'w') as outputfile:
			json.dump(data, outputfile)

	def getInfo(self):
		with open(self.storingFile) as inputFile:
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

	def get_views_clusters(self):
		#PATH CURRENTLY HARD CODED
		MAINPATH = "/home/adarsh/codingWork/Cluster"
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
		                clusterName = root.split("/")[-1]
		                if(clusterName not in CLUSTERS):
		                    CLUSTERS[clusterName] = cluster()
		                CLUSTERS[clusterName].addPath(root)
		                break
		    #set up images for that cluster
		    for cls in CLUSTERS:
		        CLUSTERS[cls].addImages()
		    VIEW_AND_CLUSTERS[directs] = CLUSTERS
		return VIEW_AND_CLUSTERS