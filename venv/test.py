#import threading
import datetime
import time
import CSVExchanging
import MailExchanging
import ClientTCP

"""
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
       if self.name == "ThreadSleep":
           print('Starting ' + self.name)
           doSleep(int(self.times))
           print('Finished ' + self.name)


def doSleep(x):
    time.sleep(x)

def runPerform():
    for i in range(0,10):
        print(i)
        time.sleep(1)

def runRaport():
    while True:
        if datetime.datetime.now().strftime('%X') == '19:31:00':
            CSVExchanging.sendDailyRaport()
            break

def runDeleting():
    # Get lock to synchronize threads
    while True:
        if datetime.datetime.now().strftime('%X') == '19:31:00':
            CSVExchanging.deleteSpool()
            break
    # Free lock to release next thread

threadLock = threading.Lock()
threads = []
"""
try:
    ClientTCP.threadPerform.start()
    try:
        ClientTCP.threadRaport.start()
        ClientTCP.threadSleep5.start()
    except:
        print('Error with creating and sending daily raport')
        MailExchanging.sendMail(MailExchanging.MailVariables.subRaportError,
                                MailExchanging.MailVariables.textRaportError)
    try:
        ClientTCP.threadDeleting.start()
        ClientTCP.threadSleep30.start()
    except:
        print('Error with deleting year-time spools')
        MailExchanging.sendMail(MailExchanging.MailVariables.subDeletingError,
                                MailExchanging.MailVariables.textDeletingError)
    for t in ClientTCP.threads:
        t.join()
except KeyboardInterrupt:
    print('Manual break by user')
    MailExchanging.sendMail(MailExchanging.MailVariables.subKeyboardInterruptError,
                            MailExchanging.MailVariables.textKeyboardInterruptError)