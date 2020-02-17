import boto3
import os
from rq import Queue
from worker import conn
import time


def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)
    # print(bucket.objects)
    # bucket.download_file("model/config.json", model/config.json)
    print("Start downloading...")
    print("dir: ", os.listdir(os.curdir))
    for s3_object in bucket.objects.filter(Prefix=remoteDirectoryName):

        print("Downloading ", s3_object.key)
        path, filename = os.path.split(s3_object.key)
        if filename != "":
            if not os.path.exists("./flaskr/" + os.path.dirname(s3_object.key)):
                os.makedirs("./flaskr/" + os.path.dirname(s3_object.key))
            bucket.download_file(s3_object.key, "./flaskr/" + s3_object.key)
    print("Finish downloading.")
    print("dir: ", os.listdir(os.curdir))


def initModel():
    print("##############START INIT MODEL")
    q = Queue('dl', connection=conn)
    # util.downloadDirectoryFroms3("indivprojcht116", "model")
    job = q.enqueue(downloadDirectoryFroms3,
                    "indivprojcht116", "model")

    print("Added job. Current number: ", len(q))
    secs = 0
    while job.get_status() != "finished" and job.get_status() != "failed":
        time.sleep(1)
        secs += 1
        if secs % 5 == 0:
            print("Waiting to finish job: ", secs)
    print("##############END INIT MODEL")
