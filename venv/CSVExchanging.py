#       -----  GLOBAL IMPORTS ------
import csv  # Imports csv module for working with CSV files
import datetime  # Imports datetime module for getting date and time
import hashlib  # Imports module for hashing
import os.path  # Imports module for pathing
import sys  # Imports sys module for system operations
import time  # Imports time module for operations with time

#       -----  IMPORTS FROM PROJECT ------
import MailExchanging
import psycopg2  # Imports psycopg2 module for communication with PostgreSQL
import virtualenv  # Imports virtual environment

#       -----  GLOBAL VARIABLES NEEDED FOR FILE FINDING  ------
pathClient = 'C:\\Users\\fliesrgio\\Downloads\\CSV_Files_AcqSys\\spool\\'
pathForDB = '/spool-data/'
longText = 'Probably it does not exist or currently located in some other place!'


#       -----  WRITES PACKETS IN CSV FILE AND AFTER SAVES THE FILE ------
def saveCSV(filename, data):
    pathCSV = pathClient + filename + str('.csv')

    try:

        fileCSV = open(pathCSV, 'w')
        fileCSV.write(data)
        fileCSV.close()
        """
        with open(pathCSV, 'w', newline='') as fileCSV:
            csv_writer = csv.writer(fileCSV, delimiter=';')
            csv_writer.write(data)
        """
    except IOError:
        print('Could not read file ' + filename + '! ' + longText)
        MailExchanging.sendMail(MailExchanging.MailVariables.subFileSavingError + filename,
                                MailExchanging.MailVariables.textFileSavingError + filename + '.',
                                MailExchanging.MailVariables.recMailsErrors)
    except:
        print('Unexpected error:', sys.exc_info()[0])
        MailExchanging.sendMail(MailExchanging.MailVariables.subFileUnexpectedError + filename,
                                MailExchanging.MailVariables.textFileUnexpectedError + filename + '.')


#       -----  READS CSV FILE IF EXISTS ------
def readCSV(filename):
    pathCSV = pathClient + filename + str('.csv')

    while not os.path.exists(pathCSV):
        time.sleep(5)
    if os.path.isfile(pathCSV):
        try:
            with open(pathCSV, 'r') as csv_file_r:
                csv_reader = csv.reader(csv_file_r)

                for line in csv_reader:
                    print(line)
        except IOError:
            print('Could not read file ' + filename + '! ' + longText)
            MailExchanging.sendMail(MailExchanging.MailVariables.subFileReadingError + filename,
                                    MailExchanging.MailVariables.textFileReadingError + filename + '.',
                                    MailExchanging.MailVariables.recMailsErrors)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            MailExchanging.sendMail(MailExchanging.MailVariables.subFileUnexpectedError + filename,
                                    MailExchanging.MailVariables.textFileUnexpectedError + filename + '.',
                                    MailExchanging.MailVariables.recMailsErrors)

    else:
        raise ValueError("%s isn't a file!" % pathClient + filename)


#       -----  HASHES FILENAME FOR QR CODE GENERATION ------
def hashData(dataToHash):
    now = datetime.datetime.now()
    currentDate = now.strftime("%d.%m.%Y")
    newData = str(dataToHash) + '.' + currentDate
    hashObject = hashlib.md5(newData.encode())
    return hashObject.hexdigest()


#       -----  ESTABLISHES CONNECTION WITH DATABASE ------
def connectDB():
    hostname = '217.182.72.46'
    username = 'flisergio'
    password = '!koMORA'
    dbname = 'acqsys'

    myConnection = psycopg2.connect(host=hostname, user=username, password=password, database=dbname, port=5432)
    myConnection.autocommit = True
    return myConnection


#       -----  SAVES INFORMATION ABOUT SPOOL IN DATABASE ------
def saveToDatabase(filename):
    attributes = ['Material', 'ColorName', 'ColorRal', 'Diameter', 'Tolerance',
                  'PrintingTemp', 'SpoolDiaExt', 'SpoolDiaInt', 'SpoolWidth']
    values = ['!!!', '!!!', '!!!', 999, 999, 999, 999, 999, 999]

    pathCSV = pathClient + filename + str('.csv')
    fileCSV = open(pathCSV, 'r')
    csv_reader = csv.reader(fileCSV, delimiter=';')

    nameOfFile = filename
    hashedName = hashData(filename)

    next(csv_reader)  # Skipping one line

    #  ----- READING GENERATION DATE FROM FILE -----  #
    dateLineSplit = str(next(csv_reader)).split(';')
    dateLineFirstElement = dateLineSplit[0].split('#')
    dateLineFirstElementSplit = str(dateLineFirstElement).split(',')
    dateBadFormat = str(dateLineFirstElementSplit[2])
    dateBadFormatSplit = dateBadFormat.split('-')
    generationDate = (dateBadFormatSplit[0] + '-' + dateBadFormatSplit[1] + '-' + dateBadFormatSplit[2])[2:]
    generationTime = (dateBadFormatSplit[3])[:-1]
    generationDateTime = (generationDate + ' ' + generationTime)[:-3]

    #  ----- SKIPPING FOUR UNNECESSARY LINES -----  #
    for i in range(0, 4):
        next(csv_reader)

    #  ----- READING EACH ATTRIBUTE FROM FILE -----  #
    while True:
        try:
            for line in csv_reader:
                try:
                    for attribute in attributes:
                        attributeNameValueSplit = str(line).split(',')
                        attributeNameBadFormat = str(attributeNameValueSplit[0])
                        attributeName = attributeNameBadFormat[2:-1]
                        if attributeName == attribute:
                            attributeValueSplit = str(attributeNameValueSplit[1])
                            attributeValue = attributeValueSplit[2:-2]
                            if attributeValue == '999':
                                if attributes.index(attribute) == 0 or attributes.index(attribute) == 1 or attributes.index(
                                        attribute) == 2:
                                    values[attributes.index(attribute)] = '!!!'
                                else:
                                    values[attributes.index(attribute)] = 999
                                continue
                            else:
                                values[attributes.index(attribute)] = attributeValue
                            break
                except:
                    break
            print(values)
            fileCSV.close()
        except csv.Error:
            str(line).replace('\0', '')
        break

    #  ----- INSERTING ATTRIBUTE VALUES IN DATABASE -----  #
    query = 'INSERT INTO spool VALUES (\'' + str(hashedName) + '\', ' + str(nameOfFile) + ', \'' + \
            str(generationDateTime) \
            + '\', \'' + str(values[0]) + '\', \'' + str(values[1]) + '\', \'' + str(values[2]) + '\', ' \
            + str(float(values[3])) + ', ' + str(float(values[4])) + ', ' + str(values[5]) + ', ' \
            + str(values[6]) + ', ' + str(values[7]) + ', ' + str(values[8]) + ', \'' + pathForDB + '\');'

    cur = connectDB().cursor()
    cur.execute(query)
    connectDB().close()
