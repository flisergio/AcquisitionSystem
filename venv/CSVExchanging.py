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
#import pg

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

    # Simple routine to run a query on a database and print the results:
    def doQuery(conn):
        cur = conn.cursor()
        cur.execute(q)

    myConnection = psycopg2.connect(host=hostname, user=username, password=password, database=dbname, port = 5432)
    myConnection.autocommit = True
    doQuery(myConnection)
    myConnection.close()
    """
    conn = pg.DB(host='217.182.72.46', user='flisergio', passwd='!koMORA', dbname='acqsys')
    conn.query(q)

    conn.close()
    """

#       -----  SAVES INFORMATION ABOUT SPOOL IN DATABASE ------
def saveToDatabase(filename):
    attributes = ['Material', 'ColorName', 'ColorRAL', 'Diameter', 'Tolerance', 'Mass',
                  'PrintingTemperature', 'SpoolDiameterExternal', 'SpoolDiameterInternal', 'SpoolWidth']
    values = ['', '', '', 0.0, 0.0, 0, 0, 0, 0, 0]

    pathCSV = pathClient + filename + str('.csv')
    fileCSV = open(pathCSV, 'r')
    csv_reader = csv.reader(fileCSV, delimiter = ';')

    nameOfFile = int(filename)
    hashedName = hashData(filename)

    next(csv_reader)

    generationDate = str(next(csv_reader).split(';'))

    for line in csv_reader:
        for attribute in attributes:
            if line.startswith(attribute):
                lineSplit = line.split(';')
                temp = str(lineSplit[1])
                if[(attributes.index(attribute) == 0) or (attributes.index(attribute) == 1) or (attributes.index(attribute) == 2)]:
                    if temp == '':
                        values[attributes.index(attribute)] = '!'
                    else:
                        values[attributes.index(attribute)] = temp
                if[(attributes.index(attribute) == 3) or (attributes.index(attribute) == 4)]:
                    if temp == '':
                        values[attributes.index(attribute)] = 999
                    else:
                        values[attributes.index(attribute)] = float(temp)
                if [(attributes.index(attribute) == 5) or (attributes.index(attribute) == 6) or (attributes.index(attribute) == 7)
                        or (attributes.index(attribute) == 8) or (attributes.index(attribute) == 9)]:
                    if temp == '':
                        values[attributes.index(attribute)] = 999
                    else:
                        values[attributes.index(attribute)] = int(temp)

    query = 'INSERT INTO spool VALUES (\'' + hashedName + '\', ' + nameOfFile + ', \'' + generationDate + '\', \''  + \
        values[0] + '\', \'' + values[1] + '\', \'' + values[2] + '\', ' + values[3] + ', ' + values[4] + ', ' + values[5] + \
        ', ' + values[6] + ', ' + values[7] + ', ' + values[8] + ', ' + values[9] + ', \'' + pathCSV + '\');'
    connectDB(query)
