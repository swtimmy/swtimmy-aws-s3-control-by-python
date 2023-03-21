import boto3	#pip install boto3
import os
from botocore.client import Config
import logging
from botocore.exceptions import ClientError
import Magic	#pip install python-magic-bin
from Core.Process import ProgressPercentage

class S3(object):
	def __init__(self,key,sec,bucketName):
		self._key = key
		self._sec = sec
		self._bucketName = bucketName
		self._updatedFile=0
		self._failedFile=0
			
	def getInfo(self):
		print("key:"+self._key)
		print("sec:"+self._sec)
		
	def getResource(self):
		self._resource = boto3.resource(
			's3',
			aws_access_key_id=self._key,
			aws_secret_access_key=self._sec,
		)
		
	def getClient(self):
		self._client = boto3.client(
			's3',
			aws_access_key_id=self._key,
			aws_secret_access_key=self._sec,
		)
		
	def getAllBucket(self):
		self.getResource()
		print("Existing buckets:")
		for bucket in self._resource.buckets.all():
			print("\t"+bucket.name)    

	def uploadFromThisDirectory(self,path="\\"):
		self.getClient()
		print("Scan directory folder and file:\n")
		self.getDirectory(path);

	def getDirectory(self,path="\\"):
		for folderName, subfolders, filenames in os.walk(path):
			if subfolders:
				for subfolder in subfolders:
					self.getDirectory(subfolder)
			correctFolderName = folderName.replace(path,"")
			#for window path, change all '\' to '/'
			correctFolderName = correctFolderName.replace("\\","/")
			print("Folder:"+correctFolderName+"")
			for filename in filenames:
				realPathFileName=folderName+"\\"+filename
				folderFileName=(correctFolderName+"/"+filename)[1:]
				print("\tFile:"+folderFileName)
				self.upload_file(realPathFileName, self._bucketName, folderFileName)
			print("\n")
			
	def upload_file(self,file_name,bucketName,object_name):
		print("\t\tget file data:")
		type = magic.Magic(mime=True,uncompress=True).from_file(file_name)
		with open(file_name,"rb") as file_data:
			data = file_data.read()
		print("\t\tsize: "+str(len(data)))
		print("\t\ttype: "+type)
		print("\t\tupload file:")
		try:
			#way 1:
			#self._client.put_object(
			#    ACL='public-read',
			#    Body=data,
			#    Bucket=bucketName,
			#    Key=object_name,
			#    ContentType=type,
			#)
			
			#way 2:
			self._client.upload_file(file_name,bucketName,object_name,ExtraArgs={'ACL':'public-read','ContentType':type},Callback=ProgressPercentage(file_name))
			print("\t\tupload successful.")
			self._updatedFile = self._updatedFile + 1
		except ClientError as e:
			logging.error(e)
			print("\t\t!!!!!!!!!!!!!!!!!!!Fail upload.")
			self._failedFile = self._failedFile + 1
			return False
		return True

	def getUploadStatus(self):
		print("\rThere are "+str(self._updatedFile)+" file(s) Done.")
		print("\rThere are "+str(self._failedFile)+" file(s) Fail.\n")