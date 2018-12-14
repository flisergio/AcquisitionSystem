import socket  # Imports socket module
import sys  # Imports sys module for system operations
import time  # Imports time module for operations with time

import CSVExchanging
import MailExchanging
#       -----  IMPORTS FROM PROJECT ------
import virtualenv

#       -----  GLOBAL VARIABLES NEEDED FOR TCP ------
s = socket.socket()  # Creates a socket object
host = '192.168.8.201'  # Ip address of TCP server
port = 61470  # Reserves a port


#       -----  EXCHANGES CSV FILES WITH SERVER  ------
def performTCP():
    textToFile = ''
    data = ''

    try:
        while True:
            try:
                data = s.recv(8192).decode()  # Receives data from server
                print(data)
            except OSError:
                print('Receiving data disallowed! Socket is probably not connected and no address was supplied.')
                MailExchanging.sendMail(MailExchanging.subDataReceivingError, MailExchanging.textDataReceivingError)
                time.sleep(5)
            #       -----  PERFORMS ACTIONS DEPENDS ON DATA FROM SERVER  ------
            if data == 'InitConnection':  # If data is "InitConnection" client responds to server that connection OK
                toSend = 'ConnectionOK'
                s.send(toSend.encode())
                print(toSend)
            elif data == 'Wait':  # If data is "Wait" client sleeps for 5 sec
                print(data)
                time.sleep(5)
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
                            MailExchanging.sendMail(MailExchanging.subDataHashingError + nameOfFile,
                                                    MailExchanging.textDataHashingError + nameOfFile + '.')
                    except:
                        toSend = 'PSQLTrouble!'
                        s.send(toSend.encode())
                        print(toSend)
                        MailExchanging.sendMail(MailExchanging.subDatabaseError, MailExchanging.textDatabaseError)
                except:
                    toSend = 'SaveTrouble!'
                    s.send(toSend.encode())
                    print(toSend)
                    MailExchanging.sendMail(MailExchanging.subFileUnexpectedError + nameOfFile,
                                            MailExchanging.textFileUnexpectedError + nameOfFile + '.')
            else:  # If data is a packet client saves it in CSV file in a loop that depends on number of packets
                print('Writing...')
                try:
                    textToFile += data
                    toSend = 'ReadyReceive'
                    s.send(toSend.encode())
                    print(toSend)
                except:
                    MailExchanging.sendMail(MailExchanging.subFileAppendingError, MailExchanging.textFileAppendingError)
                    print('Unexpected error:', sys.exc_info()[0])
            data = ''
    except KeyboardInterrupt:
        print('Manual break by user!')
        s.close()
        print('Connection closed!')
        MailExchanging.sendMail(MailExchanging.subKeyboardInterruptError, MailExchanging.textKeyboardInterruptError)


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
                MailExchanging.sendMail(MailExchanging.subKeyboardInterruptError,
                                        MailExchanging.textKeyboardInterruptError)
                break
        except TimeoutError:
            print('Connection declined! Trying again in 30 seconds.')
            #    MailExchanging.sendMail(subConnectionError, textConnectionError)
            time.sleep(30)


#       -----  MAIN FUNCTION CALL ------
if __name__ == '__main__':
    main()
