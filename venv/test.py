import csv
import json
import datetime
#   import matplotlib.pyplot as plt
#   import mpld3

import hashids
import CSVExchanging

# testcode = "121.12.10.1999"
# CSVExchanging.hashData(testcode)

# def hashData(dataToHash):
#     now = datetime.datetime.now()
#     currentDate = now.strftime("%d.%m.%Y")
#     # newDataToHash = str(dataToHash) + currentDate
#     currentDateSplit = currentDate.split('.')
#     currentMonth = currentDateSplit[1]
#     currentYear = currentDateSplit[2]
#     currentYearLastTwo = currentYear[2:]
#     # hashObject = hashlib.md5(newDataToHash.encode())
#     # return hashObject.hexdigest()
#     hashidsCode = hashids.Hashids(salt="Mora-Solutions")
#     hashID = hashidsCode.encode(int(dataToHash), int(currentMonth), int(currentYearLastTwo))
#     # print(hashidsCode.decode(hashID))
#     if (len(hashID) > 10):
#         difference = len(hashID) - 10
#         hashID = hashID[:-difference]
#     return hashID

def hashData(dataToHash):
    now = datetime.datetime.now()
    currentDate = now.strftime("%d.%m.%Y")
    newData = str(dataToHash) + '.' + currentDate
    hashObject = hashlib.md5(newData.encode())
    return hashObject.hexdigest()

# hashids = hashids.Hashids(salt="Mora-Solutions")
# id = hashids.encode(123, 12, 10, 1999)
# numbers = hashids.decode(id)

print(hashData('1207'))

