#       -----  GLOBAL IMPORTS ------
import datetime  # Imports datetime module for getting date and time
import socket  # Imports socket module
import sys  # Imports sys module for system operations
import threading  # Imports threading module for threading
import time  # Imports time module for operations with time

#       -----  IMPORTS FROM PROJECT ------
import CSVExchanging
import MailExchanging
import virtualenv  # Imports virtual environment

#       -----  GLOBAL VARIABLES NEEDED FOR TCP ------
s = socket.socket()  # Creates a socket object
host = '192.168.8.201'  # Ip address of TCP server
port = 61470  # Reserves a port


#       -----  CLASS FOR THREADING ------
class myThread(threading.Thread):
    def __init__(self, name, times):
        threading.Thread.__init__(self)
        self.name = name
        self.times = times

    def run(self):
        if self.name == "ThreadPerform":
            print('Starting ' + self.name)
            runPerform()
            print('Finished ' + self.name)
        if self.name == "ThreadRaport":
            print('Starting ' + self.name)
            threadLock.acquire()
            runRaport()
            threadLock.release()
            print('Finished ' + self.name)
        if self.name == "ThreadDeleting":
            print('Starting ' + self.name)
            threadLock.acquire()
            runDeleting()
            threadLock.release()
            print('Finished ' + self.name)
        if self.name.startswith("ThreadSleep"):
            print('Starting ' + self.name)
            doSleep(int(self.times))
            print('Finished ' + self.name)


#       -----  FUNCTIONS FOR THREADING ------
def doSleep(x):
    time.sleep(x)


def runPerform():
    while True:
        # performTCP()
        time.sleep(1)


def runRaport():
    while True:
        if datetime.datetime.now().strftime('%X') == '00:00:00':
            CSVExchanging.sendDailyRaport()
            break


def runDeleting():
    while True:
        if datetime.datetime.now().strftime('%X') == '00:00:00':
            CSVExchanging.deleteSpool()
            break


#       -----  VARIABLES FOR THREADING ------
threadLock = threading.Lock()
threads = []

#       -----  CREATING NEW THREADS ------
threadPerform = myThread("ThreadPerform", None)
threadRaport = myThread("ThreadRaport", None)
threadDeleting = myThread("ThreadDeleting", None)
threadSleep5 = myThread("ThreadSleep5", 5)
threadSleep30 = myThread("ThreadSleep30", 30)

#       -----  ADDING THREADS TO THREADS LIST ------
threads.append(threadPerform)
threads.append(threadRaport)
threads.append(threadDeleting)
threads.append(threadSleep5)
threads.append(threadSleep30)


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
                if data == 'InitConnection':  # If data is "InitConnection" client sends "ConnectionOK"
                    toSend = 'ConnectionOK'
                    s.send(toSend.encode())
                    print(toSend)
                elif data == 'Wait':  # If data is "Wait" client sleeps for 5 sec
                    print(data)
                    threadSleep5.start()
                elif (data.startswith(
                        'ToGo')):  # If data is "ToGo..." client starts waiting for packets
                    toSend = 'ReadyToWrite'
                    s.send(toSend.encode())
                    print(toSend)
                elif (
                        data == 'Confirm'):  # If data is "Confirm" client sends "Confirmed" or "SaveTrouble"
                    lines = textToFile.split('\n')
                    firstLineSplit = lines[0].split(';')
                    nameOfFile = str(firstLineSplit[1])
                    try:
                        CSVExchanging.saveCSV(nameOfFile, textToFile)
                        textToFile = ''
                        try:
                            CSVExchanging.saveToDatabase(nameOfFile)
                            try:
                                toSend = 'Hashed:' + CSVExchanging.hashData(nameOfFile)
                                s.send(toSend.encode())
                                print(toSend)
                            except:
                                toSend = 'HashTrouble!'
                                s.send(toSend.encode())
                                print(toSend)
                                MailExchanging.sendMail(MailExchanging.MailVariables.subDataHashingError + nameOfFile,
                                                        MailExchanging.MailVariables.textDataHashingError + nameOfFile + '.',
                                                        MailExchanging.MailVariables.recMailsErrors)
                        except:
                            toSend = 'PSQLTrouble!'
                            s.send(toSend.encode())
                            print(toSend)
                            MailExchanging.sendMail(MailExchanging.MailVariables.subDatabaseError,
                                                    MailExchanging.MailVariables.textDatabaseError,
                                                    MailExchanging.MailVariables.recMailsErrors)
                    except:
                        toSend = 'SaveTrouble!'
                        s.send(toSend.encode())
                        print(toSend)
                        MailExchanging.sendMail(MailExchanging.MailVariables.subFileUnexpectedError + nameOfFile,
                                                MailExchanging.MailVariables.textFileUnexpectedError + nameOfFile + '.',
                                                MailExchanging.MailVariables.recMailsErrors)
                else:  # If data is a packet client saves it in CSV file in a loop that depends on number of packets
                    print('Writing...')
                    try:
                        textToFile += data
                        toSend = 'ReadyReceive'
                        s.send(toSend.encode())
                        print(toSend)
                    except:
                        MailExchanging.sendMail(MailExchanging.MailVariables.subFileAppendingError,
                                                MailExchanging.MailVariables.textFileAppendingError,
                                                MailExchanging.MailVariables.recMailsErrors)
                        print('Unexpected error:', sys.exc_info()[0])
                #   data = ''
            except OSError:
                print('Receiving data disallowed! Socket is probably not connected and no address was supplied.')
                MailExchanging.sendMail(MailExchanging.MailVariables.subDataReceivingError,
                                        MailExchanging.MailVariables.textDataReceivingError,
                                        MailExchanging.MailVariables.recMailsErrors)
                threadSleep5.start()
    except KeyboardInterrupt:
        print('Manual break by user!')
        s.close()
        print('Connection closed!')
        MailExchanging.sendMail(MailExchanging.MailVariables.subKeyboardInterruptError,
                                MailExchanging.MailVariables.textKeyboardInterruptError,
                                MailExchanging.MailVariables.recMailsErrors)


#       -----  MAIN FUNCTION ------
def main():
    while True:
        try:
            s.connect((host, port))  # Connects to server
            try:
                threadPerform.start()
                try:
                    threadRaport.start()
                except:
                    print('Error with creating and sending daily raport')
                    MailExchanging.sendMail(MailExchanging.MailVariables.subRaportError,
                                            MailExchanging.MailVariables.textRaportError,
                                            MailExchanging.MailVariables.recMailsErrors)
                try:
                    threadDeleting.start()
                except:
                    print('Error with deleting year-time spools')
                    MailExchanging.sendMail(MailExchanging.MailVariables.subDeletingError,
                                            MailExchanging.MailVariables.textDeletingError,
                                            MailExchanging.MailVariables.recMailsErrors)
                for t in threads:
                    t.join()
            except KeyboardInterrupt:
                print('Manual break by user')
                MailExchanging.sendMail(MailExchanging.MailVariables.subKeyboardInterruptError,
                                        MailExchanging.MailVariables.textKeyboardInterruptError,
                                        MailExchanging.MailVariables.recMailsErrors)
                break
        except TimeoutError:
            print('Connection declined! Trying again in 30 seconds.')
            #    MailExchanging.sendMail(MailExchanging.MailVariables.subConnectionError,
            #                            MailExchanging.MailVariables.textConnectionError,
            #                            MailExchanging.MailVariables.recMailsErrors)
            threadSleep30.start()


#       -----  MAIN FUNCTION CALL ------
if __name__ == '__main__':
    main()
