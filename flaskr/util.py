import boto3
import os


def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)
    # print("1")
    # print(bucket.objects)
    # bucket.download_file("model/config.json", model/config.json)
    print("Start downloading...")
    for s3_object in bucket.objects.filter(Prefix=remoteDirectoryName):

        # print("2")
        print("Downloading ", s3_object)
        path, filename = os.path.split(s3_object.key)
        if filename != "":
            if not os.path.exists(os.path.dirname(s3_object.key)):
                os.makedirs(os.path.dirname(s3_object.key))
            bucket.download_file(s3_object.key, s3_object.key)
    print("Finish downloading.")
