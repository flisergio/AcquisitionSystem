import datetime  # Imports datetime module for getting date and time
import socket  # Imports socket module
import sys  # Imports sys module for system operations
import threading  # Imports threading module for threading
import time  # Imports time module for operations with time

#       -----  IMPORTS FROM PROJECT ------
import CSVExchanging
import MailExchanging
import schedule  # Imports schedule module for scheduling
import virtualenv

#       -----  GLOBAL VARIABLES NEEDED FOR TCP ------
s = socket.socket()  # Creates a socket object
host = '192.168.8.201'  # Ip address of TCP server
port = 61470  # Reserves a port


#  ----- CLASS FOR MULTITHREADING -----
class Multithreading:
    #  ----- FOR DAILY RAPORT -----
    def dailyRaport(self):
        while True:
            if datetime.datetime.now().strftime('%X') == '00:00:00':
                CSVExchanging.sendDailyRaport()
                break

    #  ----- FOR DELETING SPOOLS -----
    def deleteSpool(self):
        while True:
            if datetime.datetime.now().strftime('%X') == '00:00:00':
                CSVExchanging.deleteSpool()
                break

    #  ----- FOR SLEEPING FUNCTIONS -----
    def doSleep(self, x):
        time.sleep(x)


#       -----  EXCHANGES CSV FILES WITH SERVER  ------
def performTCP():
    textToFile = ''
    data = ''

    try:
        while True:
            try:
                data = s.recv(8192).decode()  # Receives data from server
                print(data)
                #       -----  PERFORMS ACTIONS DEPENDS ON DATA FROM SERVER  ------
                if data == 'InitConnection':  # If data is "InitConnection" client responds to server that connection OK
                    toSend = 'ConnectionOK'
                    s.send(toSend.encode())
                    print(toSend)
                elif data == 'Wait':  # If data is "Wait" client sleeps for 5 sec
                    print(data)
                    thSleep5 = threading.Thread(target=Multithreading().doSleep, args=(5,)).start()
                elif (data.startswith(
                        'ToGo')):  # If data is "ToGo..." client sends "Ready,0" to server and starts waiting for packets
                    toSend = 'ReadyToWrite'
                    s.send(toSend.encode())
                    print(toSend)
                elif (
                        data == 'Confirm'):  # If data is "Confirm" client responds to server "Confirmed" if saving OK or "SaveTrouble" if not
                    lines = textToFile.split('\n')
                    firstLineSplit = lines[0].split(';')
                    nameOfFile = str(firstLineSplit[1])
                    try:
                        CSVExchanging.saveCSV(nameOfFile, textToFile)
                        textToFile = ''
                        try:
                            CSVExchanging.saveToDatabase(nameOfFile)
                            try:
                                toSend = CSVExchanging.hashData(nameOfFile)
                                s.send(toSend.encode())
                                print('Hashed:' + toSend)
                            except:
                                toSend = 'HashTrouble!'
                                s.send(toSend.encode())
                                print(toSend)
                                MailExchanging.sendMail(MailExchanging.MailVariables.subDataHashingError + nameOfFile,
                                                        MailExchanging.MailVariables.textDataHashingError + nameOfFile + '.')
                        except:
                            toSend = 'PSQLTrouble!'
                            s.send(toSend.encode())
                            print(toSend)
                            MailExchanging.sendMail(MailExchanging.MailVariables.subDatabaseError, MailExchanging.MailVariables.textDatabaseError)
                    except:
                        toSend = 'SaveTrouble!'
                        s.send(toSend.encode())
                        print(toSend)
                        MailExchanging.sendMail(MailExchanging.MailVariables.subFileUnexpectedError + nameOfFile,
                                                MailExchanging.MailVariables.textFileUnexpectedError + nameOfFile + '.')
                else:  # If data is a packet client saves it in CSV file in a loop that depends on number of packets
                    print('Writing...')
                    try:
                        textToFile += data
                        toSend = 'ReadyReceive'
                        s.send(toSend.encode())
                        print(toSend)
                    except:
                        MailExchanging.sendMail(MailExchanging.MailVariables.subFileAppendingError,
                                                MailExchanging.MailVariables.textFileAppendingError)
                        print('Unexpected error:', sys.exc_info()[0])
                data = ''
            except OSError:
                print('Receiving data disallowed! Socket is probably not connected and no address was supplied.')
                MailExchanging.sendMail(MailExchanging.MailVariables.subDataReceivingError, MailExchanging.MailVariables.textDataReceivingError)
                thSleep5 = threading.Thread(target=Multithreading().doSleep, args=(5,)).start()
    except KeyboardInterrupt:
        print('Manual break by user!')
        s.close()
        print('Connection closed!')
        MailExchanging.sendMail(MailExchanging.MailVariables.subKeyboardInterruptError, MailExchanging.MailVariables.textKeyboardInterruptError)


#       -----  MAIN FUNCTION ------
def main():
    while True:
        try:
            s.connect((host, port))  # Connects to server
            try:
                while True:
                    performTCP()
            except KeyboardInterrupt:
                print('Manual break by user')
                MailExchanging.sendMail(MailExchanging.MailVariables.subKeyboardInterruptError,
                                        MailExchanging.MailVariables.textKeyboardInterruptError)
                break
        except TimeoutError:
            print('Connection declined! Trying again in 30 seconds.')
            #    MailExchanging.sendMail(MailExchanging.MailVariables.subConnectionError, MailExchanging.MailVariables.textConnectionError)
            thSleep30 = threading.Thread(target=Multithreading().doSleep, args=(30,)).start()
        try:
            thRaport = threading.Thread(target=Multithreading().dailyRaport).start()
        except:
            print('Error with creating and sending daily raport')
            MailExchanging.sendMail(MailExchanging.MailVariables.subRaportError, MailExchanging.MailVariables.textRaportError)
        try:
            thDelete = threading.Thread(target=Multithreading().deleteSpool).start()
        except:
            print('Error with deleting year-time spools')
            MailExchanging.sendMail(MailExchanging.MailVariables.subDeletingError, MailExchanging.MailVariables.textDeletingError)


#       -----  MAIN FUNCTION CALL ------
if __name__ == '__main__':
    main()
