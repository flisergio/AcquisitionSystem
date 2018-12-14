import csv  # Imports csv module for working with CSV files
import hashlib  # Imports module for hashing
import datetime   # Imports datetime module for getting date
import sys
import CSVExchanging


#       -----  SAVES INFORMATION ABOUT SPOOL IN DATABASE ------
def saveDB(filename):
    attributes = ['Material', 'ColorName', 'ColorRal', 'Diameter', 'Tolerance', 'Mass',
                  'PrintingTamp', 'SpoolDiaExt', 'SpoolDiaInt', 'SpoolWidth']
    values = ['!!!', '!!!', '!!!', 999, 999, 999, 999, 999, 999, 999]

    pathCSV = pathClient + filename + str('.csv')
    fileCSV = open(pathCSV, 'r')
    csv_reader = csv.reader(fileCSV, delimiter = ';')

    nameOfFile = filename
    hashedName = CSVExchanging.hashData(filename)

    next(csv_reader)
    #  ----- READING GENERATION DATE FROM FILE -----  #
    dateLineSplit = str(next(csv_reader)).split(';')
    dateLineFirstElement = dateLineSplit[0].split('#')
    dateLineFirstElementSplit = str(dateLineFirstElement).split(',')
    dateBadFormat = str(dateLineFirstElementSplit[2])
    dateBadFormatSplit = dateBadFormat.split('-')
    generationDate = (dateBadFormatSplit[0] + '-' + dateBadFormatSplit[1] + '-' + dateBadFormatSplit[2])[2:]
    generationTime = (dateBadFormatSplit[3])[:-1]
    generationDateTime = generationDate + ' ' + generationTime

    #  ----- SKIPPING UNNECESSARY LINES -----  #
    next(csv_reader)
    next(csv_reader)
    next(csv_reader)
    next(csv_reader)

    #  ----- READING EACH ATTRIBUTE FROM FILE -----  #
    for line in csv_reader:
        for attribute in attributes:
            attributeLineSplit = str(line).split(';')
            attributeNameValueSplit = str(attributeLineSplit).split(',')
            attributeNameBadFormat = str(attributeNameValueSplit[0])
            attributeName = attributeNameBadFormat[4:-1]
            if (attributeName == attribute):
                attributeValueSplit = str(attributeNameValueSplit[1])
                attributeValue = attributeValueSplit[2:-1]
                if(attributeValue == ''):
                    continue
                else:
                    values[attributes.index(attribute)] = attributeValue
    print(values)  # For printing values list
    #  ----- INSERTING ATTRIBUTE VALUES IN DATABASE -----  #
    query = 'INSERT INTO spool VALUES (\'' + hashedName + '\', ' + nameOfFile + ', \'' + generationDateTime + '\', \'' + values[0] + \
            '\', \'' + values[1] + '\', \'' + values[2] + '\', ' + str(values[3]) + ', ' + str(values[4]) + ', ' + str(values[5]) + \
            ', ' + str(values[6]) + ', ' + str(values[7]) + ', ' + str(values[8]) + ', ' + str(values[9]) + ', \'' + pathClient + '\');'
    CSVExchanging.connectDB(query)
    print(query)    # For printing result query


#       -----  MAIN FUNCTION ------
def main():
    saveDB('107')


#       -----  MAIN FUNCTION CALL ------
if __name__ == '__main__':
    main()
