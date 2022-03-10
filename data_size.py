
class DataSize(object):
    # initializing the packet size to be transferred through medium to default value.
    chunkSize = 2048


def getChunkSize():
    return DataSize.chunkSize


# utility function to set packet size.
def setChunkSize(newSize):
    DataSize.chunkSize = newSize

