import os

class textParser:

    @classmethod
    def assemble_List(self, fileName, fromDate, toDate):
        finalList = []
        # FILE IS FROM `/app/test-files` path
        filePath = os.path.join("app/test-files", fileName)
        with open(filePath, 'r') as f:
            for fLine in f:
                # fLine = f.readline()
                lineList = fLine.split()
                if lineList[0] >= fromDate and lineList[0] <= toDate:
                    entry = {
                        "eventTime" : lineList[0], 
                        "email" : lineList[1], 
                        "sessionId" : lineList[2]}
                    finalList.append(entry)
                elif lineList[0] > toDate:
                    break
        return finalList