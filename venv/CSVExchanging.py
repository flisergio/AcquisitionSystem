#       -----  GLOBAL IMPORTS ------
import csv  # Imports csv module for working with CSV files
import datetime  # Imports datetime module for getting date and time
import hashlib  # Imports module for hashing
import os.path  # Imports module for pathing
import sys  # Imports sys module for system operations
import time  # Imports time module for operations with time

#       -----  IMPORTS FROM PROJECT ------
import ClientTCP
import MailExchanging
import psycopg2  # Imports psycopg2 module for communication with PostgreSQL
import virtualenv  # Imports virtual environment

#       -----  GLOBAL VARIABLES NEEDED FOR FILE FINDING  ------
pathClient = 'C:\\Users\\fliesrgio\\Downloads\\'
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
        threadSleep5 = ClientTCP.myThread("ThreadSleep5", 5)
        ClientTCP.threads.append(threadSleep5)
        threadSleep5.start()
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
    attributes = ['Material', 'ColorName', 'ColorRal', 'Diameter', 'Tolerance', 'Mass',
                  'PrintingTamp', 'SpoolDiaExt', 'SpoolDiaInt', 'SpoolWidth']
    values = ['!!!', '!!!', '!!!', 999, 999, 999, 999, 999, 999, 999]

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
    next(csv_reader)
    next(csv_reader)
    next(csv_reader)
    next(csv_reader)

    #  ----- READING EACH ATTRIBUTE FROM FILE -----  #
    for line in csv_reader:
        for attribute in attributes:
            attributeNameValueSplit = str(line).split(',')
            attributeNameBadFormat = str(attributeNameValueSplit[0])
            attributeName = attributeNameBadFormat[4:-1]
            if attributeName == attribute:
                print(line)
                attributeValueSplit = str(attributeNameValueSplit[1])
                attributeValue = attributeValueSplit[1:-3]
                if attributeValue == '999':
                    print('a')
                    if attributes.index(attribute) == 0 or attributes.index(attribute) == 1 or attributes.index(
                            attribute) == 2:
                        values[attributes.index(attribute)] = '!!!'
                    else:
                        values[attributes.index(attribute)] = 999
                    continue
                else:
                    values[attributes.index(attribute)] = attributeValue
    fileCSV.close()

    #  ----- INSERTING ATTRIBUTE VALUES IN DATABASE -----  #
    query = 'INSERT INTO spool VALUES (\'' + str(hashedName) + '\', ' + str(nameOfFile) + ', \'' + str(
        generationDateTime) + '\', \'' + \
            str(values[0]) + '\', \'' + str(values[1]) + '\', \'' + str(values[2]) + '\', ' + str(
        float(values[3])) + ', ' + str(float(values[4])) + ', ' + str(
        values[5]) + ', ' + str(values[6]) + ', ' + str(values[7]) + ', ' + str(values[8]) + ', ' + str(
        values[9]) + ', \'' + pathClient + '\');'
    cur = connectDB().cursor()
    cur.execute(query)
    connectDB().close()


def sendDailyRaport():
    cur = connectDB().cursor()

    dateDayBeforeBadFormat = (datetime.datetime.now() - datetime.timedelta(hours=24))
    dateForMail = (dateDayBeforeBadFormat.strftime("%d.%m.%Y"))
    dateTimeDayBefore = (dateDayBeforeBadFormat.strftime("%Y-%m-%d"))

    diameterForMail = ''
    massForMail = ''
    materialForMail = ''
    colorForMail = ''

    #  ----- FINDING TOTAL NUMBER OF SPOOLS BY DATE FOR MAIL -----
    queryForTotalNumber = 'SELECT COUNT(*) FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                          ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\';'
    cur.execute(queryForTotalNumber)
    numOfSpools = cur.fetchone()[0]

    #  ----- FINDING DIFFERENT DIAMETER VALUES BY DATE FOR MAIL -----
    queryForDiameterValues = 'SELECT DISTINCT diameter FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                             ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY diameter;'
    cur.execute(queryForDiameterValues)
    valOfSpoolDiameter = cur.fetchall()

    for value in valOfSpoolDiameter:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE diameter = \'' + str(value)[
                                                                                      1:-2] + '\' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolDiameter = cur.fetchone()[0]
        diameterSubtext = 'With diameter ' + str(value)[1:-2] + ': ' + str(numWithSpoolDiameter)
        diameterForMail = diameterForMail + diameterSubtext + '\n'

    #  ----- FINDING DIFFERENT MASS VALUES BY DATE FOR MAIL -----
    queryForMassValues = 'SELECT DISTINCT mass FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                         ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY mass;'
    cur.execute(queryForMassValues)
    valOfSpoolMass = cur.fetchall()

    for value in valOfSpoolMass:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE mass = \'' + str(value)[
                                                                                  1:-2] + '\' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolMass = cur.fetchone()[0]
        massSubtext = 'With mass ' + str(value)[1:-2] + ': ' + str(numWithSpoolMass)
        massForMail = massForMail + massSubtext + '\n'

    #  ----- FINDING DIFFERENT MATERIAL VALUES BY DATE FOR MAIL -----
    queryForMaterialValues = 'SELECT DISTINCT material FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                             ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY material;'
    cur.execute(queryForMaterialValues)
    valOfSpoolMaterial = cur.fetchall()

    for value in valOfSpoolMaterial:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE material = ' + str(value)[
                                                                                    1:-2] + ' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolMaterial = cur.fetchone()[0]
        materialSubtext = 'With material ' + str(value)[1:-2] + ': ' + str(numWithSpoolMaterial)
        materialForMail = materialForMail + materialSubtext + '\n'

    #  ----- FINDING DIFFERENT COLOR VALUES BY DATE FOR MAIL -----
    queryForColorValues = 'SELECT DISTINCT ColorName FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                          ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY ColorName;'
    cur.execute(queryForColorValues)
    valOfSpoolColor = cur.fetchall()

    for value in valOfSpoolColor:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE ColorName = ' + str(value)[
                                                                                     1:-2] + ' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolColor = cur.fetchone()[0]
        colorSubtext = 'With color ' + str(value)[1:-2] + ': ' + str(numWithSpoolColor)
        colorForMail = colorForMail + colorSubtext + '\n'

    connectDB().close()

    mailSubject = 'Spool production raport for ' + dateForMail
    if numOfSpools > 0:
        mailText = 'Total spools produced: ' + str(numOfSpools) + '\n\n' + \
                   ' \t\t\t----- Diameter value: number of spools with this diameter ----- \n' + diameterForMail + '\n' + \
                   ' \t\t\t----- Mass value: number of spools with this mass ----- \n' + massForMail + '\n' + \
                   ' \t\t\t----- Material value: number of spools with this material ----- \n' + materialForMail + '\n' + \
                   ' \t\t\t----- Color value: number of spools with this color ----- \n' + colorForMail + '\n'
    else:
        mailText = 'Total spools produced: ' + str(numOfSpools) + '\n\n' + 'No spools produced this day!'
    MailExchanging.sendMail(mailSubject, mailText, MailExchanging.MailVariables.recMails)


def deleteSpool():
    cur = connectDB().cursor()

    dateTimeYearBeforeBadFormat = (datetime.datetime.now() - datetime.timedelta(days=366))
    dateYearBeforeForMail = (dateTimeYearBeforeBadFormat.strftime("%d.%m.%Y"))
    dateTimeYearBeforeStart = (dateTimeYearBeforeBadFormat.strftime("%Y-%m-%d") + ' 00:00:00')
    dateTimeYearBeforeEnd = (dateTimeYearBeforeBadFormat.strftime("%Y-%m-%d") + ' 23:59:59')

    queryDelete = 'DELETE FROM spool WHERE date = (SELECT date FROM spool WHERE date BETWEEN \'' + \
                  dateTimeYearBeforeStart + '\' AND \'' + dateTimeYearBeforeEnd + '\');'
    cur.execute(queryDelete)

    connectDB().close()

    mailSubject = 'Deleted all spools produced ' + dateYearBeforeForMail
    mailText = 'Spools that were produced ' + dateYearBeforeForMail + ' were deleted from database!'
    MailExchanging.sendMail(mailSubject, mailText, MailExchanging.MailVariables.recMails)
