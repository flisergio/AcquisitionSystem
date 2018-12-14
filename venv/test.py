import csv  # Imports csv module for working with CSV files
import hashlib  # Imports module for hashing
import os.path  # Imports module for pathing
import time  # Imports time module for operations with time
import datetime   # Imports datetime module for getting date
import sys  # Imports sys module for system operations

#       -----  IMPORTS FROM PROJECT ------
import virtualenv
import psycopg2
import CSVExchanging
import MailExchanging

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
            if attributeName == attribute:
                attributeValueSplit = str(attributeNameValueSplit[1])
                attributeValue = attributeValueSplit[2:-1]
                if attributeValue == '':
                    continue
                else:
                    values[attributes.index(attribute)] = attributeValue
    #print(values)  # For printing values list

    #  ----- INSERTING ATTRIBUTE VALUES IN DATABASE -----  #
    queryInsertSpool = 'INSERT INTO spool VALUES (\'' + hashedName + '\', ' + nameOfFile + ', \'' + generationDateTime + '\', \'' + values[0] + \
            '\', \'' + values[1] + '\', \'' + values[2] + '\', ' + str(values[3]) + ', ' + str(values[4]) + ', ' + str(values[5]) + \
            ', ' + str(values[6]) + ', ' + str(values[7]) + ', ' + str(values[8]) + ', ' + str(values[9]) + ', \'' + pathClient + '\');'
    cur = CSVExchanging.connectDB().cursor()
    cur.execute(queryInsertSpool)
    CSVExchanging.connectDB().close()
    #print(query)    # For printing result query


def sendDailyRaport():
    cur = CSVExchanging.connectDB().cursor()

    #queryForDate = 'SELECT date FROM spool;'
    #cur.execute(queryForDate)
    #dateTime = cur.fetchone()[0]

    #generationDate = (str(dateTime).split(' '))[0]
    dateDayBeforeBadFormat = (datetime.datetime.now()-datetime.timedelta(hours=24))
    dateForMail = (dateDayBeforeBadFormat.strftime("%d.%m.%Y"))
    dateTimeDayBefore = (dateDayBeforeBadFormat.strftime("%Y-%m-%d"))
    #print(dateTimeDayBefore)
    #print(dateForMail)

    diameterForMail = ''
    massForMail = ''
    materialForMail = ''
    colorForMail = ''

    queryForTotalNumber = 'SELECT COUNT(*) FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                             ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\';'
    #print(queryForTotalNumber)
    cur.execute(queryForTotalNumber)
    numOfSpools = cur.fetchone()[0]
    #print(numOfSpools)

    queryForDiameterValues = 'SELECT DISTINCT diameter FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                             ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY diameter;'
    #print(queryForDiameterValues)
    cur.execute(queryForDiameterValues)
    valOfSpoolDiameter = cur.fetchall()
    #print(valOfSpoolDiameter)
    for value in valOfSpoolDiameter:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE diameter = \'' + str(value)[1:-2] + '\' AND date BETWEEN \'' + \
                             dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        #print(queryForSameValuesNumber)
        cur.execute(queryForSameValuesNumber)
        numWithSpoolDiameter = cur.fetchone()[0]
        diameterSubtext = 'With diameter ' + str(value)[1:-2] + ': ' + str(numWithSpoolDiameter)
        diameterForMail = diameterForMail + diameterSubtext + '\n'
        #print('For ' + str(value)[1:-2] + ': ' + str(numWithSpoolDiameter))

    queryForMassValues = 'SELECT DISTINCT mass FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                             ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY mass;'
    #print(queryForDiameterValues)
    cur.execute(queryForMassValues)
    valOfSpoolMass = cur.fetchall()
    # print(valOfSpoolMass)
    for value in valOfSpoolMass:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE mass = \'' + str(value)[1:-2] + '\' AND date BETWEEN \'' + \
                             dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        #print(queryForSameValuesNumber)
        cur.execute(queryForSameValuesNumber)
        numWithSpoolMass = cur.fetchone()[0]
        massSubtext = 'With mass ' + str(value)[1:-2] + ': ' + str(numWithSpoolMass)
        massForMail = massForMail + massSubtext + '\n'
        #print('For ' + str(value)[1:-2] + ': ' + str(numWithSpoolMass))

    queryForMaterialValues = 'SELECT DISTINCT material FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                         ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY material;'
    # print(queryForDiameterValues)
    cur.execute(queryForMaterialValues)
    valOfSpoolMaterial = cur.fetchall()
    # print(valOfSpoolMass)
    for value in valOfSpoolMaterial:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE material = ' + str(value)[1:-2] + ' AND date BETWEEN \'' + \
                             dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        #print(queryForSameValuesNumber)
        cur.execute(queryForSameValuesNumber)
        numWithSpoolMaterial = cur.fetchone()[0]
        materialSubtext = 'With material ' + str(value)[1:-2] + ': ' + str(numWithSpoolMaterial)
        materialForMail = materialForMail + materialSubtext + '\n'
        #print('For ' + str(value)[1:-2] + ': ' + str(numWithSpoolMaterial))

    queryForColorValues = 'SELECT DISTINCT ColorName FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                          ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY ColorName;'
    # print(queryForDiameterValues)
    cur.execute(queryForColorValues)
    valOfSpoolColor = cur.fetchall()
    # print(valOfSpoolMass)
    for value in valOfSpoolColor:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE ColorName = ' + str(value)[
                                                                                 1:-2] + ' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        # print(queryForSameValuesNumber)
        cur.execute(queryForSameValuesNumber)
        numWithSpoolColor = cur.fetchone()[0]
        colorSubtext = 'With color ' + str(value)[1:-2] + ': ' + str(numWithSpoolColor)
        colorForMail = colorForMail + colorSubtext + '\n'
        #print('For ' + str(value)[1:-2] + ': ' + str(numWithSpoolColor))

    CSVExchanging.connectDB().close()

    mailSubject = 'Spool production raport for ' + dateForMail
    mailText = 'Spools producted: ' + str(numOfSpools) + '\n\n' + diameterForMail + massForMail + materialForMail + colorForMail
    MailExchanging.sendMail(mailSubject, mailText)


#       -----  MAIN FUNCTION ------
def main():
    #saveDB('107')
    sendDailyRaport()


#       -----  MAIN FUNCTION CALL ------
if __name__ == '__main__':
    main()
