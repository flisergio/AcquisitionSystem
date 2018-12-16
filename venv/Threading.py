#       -----  GLOBAL IMPORTS ------
import datetime  # Imports datetime module for getting date and time
import threading  # Imports threading module for threading
import time  # Imports time module for operations with time

import CSVExchanging
#       -----  IMPORTS FROM PROJECT ------
import ClientTCP


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
        # ClientTCP.performTCP()
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
