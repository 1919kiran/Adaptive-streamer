
class DataSize(object):
    # initializing the packet size to be transferred through medium to default value.
    def __init__(self):
        self.chunkSize = 2048

    def getChunkSize(self):
        return self.chunkSize

    # utility function to set packet size.
    def setChunkSize(self, newSize):
        self.chunkSize = newSize

