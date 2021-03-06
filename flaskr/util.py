import boto3
import os
# from rq import Queue
# from worker import conn
import time


def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)
    # print(bucket.objects)
    # bucket.download_file("model/config.json", model/config.json)
    print("Start downloading...")
    print("dir: ", os.listdir(os.curdir))
    for s3_object in bucket.objects.filter(Prefix=remoteDirectoryName):

        path, filename = os.path.split(s3_object.key)
        if filename != "" and path == "model":
            # if not os.path.exists(os.path.dirname(s3_object.key)):
            #     os.makedirs(os.path.dirname(s3_object.key))
            # bucket.download_file(s3_object.key, s3_object.key)
            if not os.path.exists("/app/" + os.path.dirname(s3_object.key)):
                os.makedirs("/app/" + os.path.dirname(s3_object.key))
            try:
                print("Downloading ", s3_object.key)
                bucket.download_file(s3_object.key, "/app/" + s3_object.key)
            except botocore.exceptions.ClientError as e:
                print("ERR: ", e)
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise
    print("Finish downloading.")
    print("path: ", os.path.dirname(os.path.abspath(__file__)))
    print("dir: ", os.listdir(os.curdir))


# def initModel():
#     print("##############START INIT MODEL")
#     q = Queue('dl', connection=conn)
#     # util.downloadDirectoryFroms3("indivprojcht116", "model")
#     job = q.enqueue(downloadDirectoryFroms3, "indivprojcht116", "model")

#     print("Added job. Current number: ", len(q))
#     secs = 0
#     while job.get_status() != "finished" and job.get_status() != "failed":
#         time.sleep(1)
#         secs += 1
#         if secs % 5 == 0:
#             print("Waiting to finish job: ", secs)
#     print("##############END INIT MODEL")
#     return job
