import indiv_models
import util

# model = indiv_models.PositiveRatioModel()
# model.predict()
bucketName = "indivprojcht116"
remoteDirectoryName = "model"
util.downloadDirectoryFroms3(bucketName, remoteDirectoryName)
