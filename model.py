import os
import random


class modelImage:
	def __init__(self):
		self.clusters = []
		self.clusterPath = None

	def getClusterList(self, listLocation):
		pass
	def getClusterImages(self,clusterLocation, amount):
		pass

	def requestClusterImages(self, clusterLocation, amount="all"):
		imageDict = dict()
		self.clusters = os.listdir(clusterLocation)
		self.clusterPath = clusterLocation
		for cluster in self.clusters:
			clusterImages = os.listdir(clusterLocation+"\\"+cluster)
			clusterLen = len(clusterImages)
			if(amount=="all"):
				amount = clusterLen
			imageDict[cluster] = [clusterLocation+"\\"+cluster+"\\"+clusterImages[random.randint(0,clusterLen-1)] for i in range(amount)]
		return imageDict

	def requestDissimilarImages(self, clusterName):
		#[ (imagelocation, percentageDissimilar), (imagelocation, percentageDissimilar), (imagelocation, percentageDissimilar)... ]
		pass