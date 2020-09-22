import os
import random
import cv2
import sklearn.cluster import MiniBatchKmeans # Make sure you have sklearn--> pip install sklearn
import numpy as np
import json
from PyQt5 import Qt,QtCore, QtGui


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

        def brightness(self, image, alpha=1.0, beta=2.0):

            self.image = cv2.imread(image)

            result = cv2.addWeighted(image,alpha,np.zeros(image.shape,image.dtype),0,beta)

            return result

        def quant(self,image,cluster):
 
            self.image = cv2.imread(image)
            (h,w) = image.shape(:2)
            image = cv2.cvtColor((image.shape[0] * image.shape[1],3))
            
            clt = MiniBatchKMeans(n_clusters = cluster)
            quant = clt.cluster_centers_.astype("uint8")[labels]

            quant = quant.reshape((h,w,3))
            image = image.reshape((h,w,3))

            quantized_image = cv2.hstack([image,quant])

            return quantized_image


	def brightness(self, image, isArr=False, alpha=1.0, beta=0.0):
		if(not isArr):
			image = cv2.imread(image)
		# kernel = np.ones((5,5),np.float32)/25
		# result = cv2.filter2D(image,-1,kernel)
		result = cv2.addWeighted(image,alpha,np.zeros(image.shape,image.dtype),0,beta)		
		return result

