import os
import random
import cv2
import sklearn.cluster import MiniBatchKmeans # Make sure you have sklearn--> pip install sklearn
class modelImage:
	def __init__(self):
		self.clusters = []
		self.clusterPath = None

	def get_cluster_list(self, listLocation):
		pass
	def get_cluster_images(self,clusterLocation, amount):
		pass

	def request_cluster_images(self, clusterLocation, amount="all"):
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

