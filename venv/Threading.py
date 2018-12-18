from __future__ import with_statement

#       -----  GLOBAL IMPORTS ------
import datetime  # Imports datetime module for getting date and time
import threading  # Imports threading module for threading
import time  # Imports time module for operations with time

import CSVExchanging
#       -----  IMPORTS FROM PROJECT ------
import ClientTCP
import MailExchanging


#       -----  CLASS FOR THREADING ------
class myThread(threading.Thread):
    def __init__(self, threadID, name, times):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.times = times

    def run(self):
        if self.name == "ThreadPerform":
            #   print('Starting ' + self.name + '\n')  # For tests
            with threadLockPerform:
                runPerform()
            #   print('Finished ' + self.name + '\n')  # For tests
        if self.name == "ThreadRaport":
            #   print('Starting ' + self.name + '\n')  # For tests
            with threadLockRaport:
                runRaport()
            #   print('Finished ' + self.name + '\n')  # For tests
        if self.name == "ThreadDeleting":
            #   print('Starting ' + self.name + '\n')  # For tests
            with threadingLockDelete:
                runDeleting()
            #   print('Finished ' + self.name + '\n')  # For tests
        if self.name.startswith("ThreadSleep"):
            #   print('Starting ' + self.name + '\n')  # For tests
            doSleep(self.name, self.times)
            #   print('Finished ' + self.name + '\n')  # For tests


#       -----  FUNCTIONS FOR THREADING ------

def doSleep(name, x):
    time.sleep(x)
    '''
    for i in range(1, (x + 1)):
        print('[' + name + '] - Sleeping: ' + str(i) + '\n')
        time.sleep(1)
    '''


def runPerform():
    while True:
        ClientTCP.performTCP()
        #  ----- FOR TESTS: -----
        #   print('Performing . . .' + '\n')
        #   time.sleep(1)


def runRaport():
    while True:
        time.sleep(.5)
        if datetime.datetime.now().strftime('%X') == '00:00:00':
            CSVExchanging.sendDailyRaport()


def runDeleting():
    while True:
        time.sleep(.5)
        if datetime.datetime.now().strftime('%X') == '00:00:00':
            CSVExchanging.deleteSpool()


#       -----  VARIABLES FOR THREADING ------
threadLockPerform = threading.RLock()
threadLockRaport = threading.RLock()
threadingLockDelete = threading.RLock()
threadLockSleep5 = threading.RLock()
threadLockSleep30 = threading.RLock()
threads5 = []
threads30 = []

#       -----  CREATING NEW THREADS ------
threadPerform = myThread(1, "ThreadPerform", None)
threadRaport = myThread(2, "ThreadRaport", None)
threadDeleting = myThread(3, "ThreadDeleting", None)
