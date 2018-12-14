import csv  # Imports csv module for working with CSV files
import hashlib  # Imports module for hashing
import os.path  # Imports module for pathing
import time  # Imports time module for operations with time
import datetime   # Imports datetime module for getting date
import sys  # Imports sys module for system operations

#       -----  IMPORTS FROM PROJECT ------
import virtualenv
import psycopg2
import MailExchanging

#       -----  GLOBAL VARIABLES NEEDED FOR FILE FINDING  ------
pathClient = 'C:\\Users\\fliesrgio\\Work\\Maciek\\Filament control system\\Server\\'
longText = 'Probably it does not exist or currently located in some other place!'


#       -----  WRITES PACKETS IN CSV FILE AND AFTER SAVES THE FILE ------
def saveCSV(filename, data):

    pathCSV = pathClient + filename + str('.csv')

    try:
        """
        fileCSV = open(pathCSV, 'w')
        fileCSV.write(data)
        fileCSV.close()
        """
        with open(pathCSV, 'w', newline = '') as fileCSV:
            csv_writer = csv.writer(fileCSV, delimiter = ';')
            csv_writer.write(data)

    except IOError:
        print('Could not read file ' + filename + '! ' + longText)
        MailExchanging.sendMail(MailExchanging.subFileSavingError + filename, MailExchanging.textFileSavingError + filename + '.')
    except:
        print('Unexpected error:', sys.exc_info()[0])
        MailExchanging.sendMail(MailExchanging.subFileUnexpectedError + filename, MailExchanging.textFileUnexpectedError + filename + '.')

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
            MailExchanging.sendMail(MailExchanging.subFileReadingError + filename, MailExchanging.textFileReadingError + filename + '.')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            MailExchanging.sendMail(MailExchanging.subFileUnexpectedError + filename, MailExchanging.textFileUnexpectedError + filename + '.')

    else:
        raise ValueError("%s isn't a file!" % pathClient + filename)

#       -----  HASHES FILENAME FOR QR CODE GENERATION ------
def hashData(dataToHash):
    now = datetime.datetime.now()
    currentDate = now.strftime("%d.%m.%Y")
    newData = str(dataToHash) + '.' + currentDate
    print('Data to be hashed: ' + newData)
    hashObject = hashlib.md5(newData.encode())
    return hashObject.hexdigest()

#       -----  ESTABLISHES CONNECTION WITH DATABASE ------
def connectDB(q):

    hostname = '217.182.72.46'
    username = 'flisergio'
    password = '!koMORA'
    dbname = 'acqsys'

    def doQuery(conn):
        cur = conn.cursor()
        cur.execute(q)

    myConnection = psycopg2.connect(host=hostname, user=username, password=password, database=dbname, port = 5432)
    myConnection.autocommit = True
    doQuery(myConnection)
    myConnection.close()


#       -----  SAVES INFORMATION ABOUT SPOOL IN DATABASE ------
def saveToDatabase(filename):
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
    query = 'INSERT INTO spool VALUES (\'' + hashedName + '\', ' + nameOfFile + ', \'' + generationDateTime + '\', \'' + values[0] + \
            '\', \'' + values[1] + '\', \'' + values[2] + '\', ' + str(values[3]) + ', ' + str(values[4]) + ', ' + str(values[5]) + \
            ', ' + str(values[6]) + ', ' + str(values[7]) + ', ' + str(values[8]) + ', ' + str(values[9]) + ', \'' + pathClient + '\');'
    CSVExchanging.connectDB(query)
    #print(query)    # For printing result query
