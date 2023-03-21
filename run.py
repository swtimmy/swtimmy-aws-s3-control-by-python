print("\n")
print("######################################### Start #########################################")
print("\n\n")

from Core.S3 import S3

# key&sec get from "My Security Credentials> AWS IAM credentials::Access keys for CLI, SDK, &API access"
key='Your Key' #XXXXXXXXXXXXXXXXXXXX
sec='Your Sec' #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
region='ap-southeast-1'
bucketName='Your bucketName' #xxxxxxxxxxxxx

run = S3(key,sec,bucketName)
run.getInfo()
run.uploadFromThisDirectory('Your-Absolute-Document-Folder-Path') #C:\\Users\\timmyso\\YourDocumentFolder
run.getUploadStatus()

#run.getAllBucket()

print("\n\n")
print("########################################### End ###########################################")
print("\n")