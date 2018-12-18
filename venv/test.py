from __future__ import with_statement

#       -----  GLOBAL IMPORTS ------
import datetime  # Imports datetime module for getting date and time
import threading  # Imports threading module for threading
import time  # Imports time module for operations with time

#       -----  IMPORTS FROM PROJECT ------
import CSVExchanging
import MailExchanging
import Threading

while True:
    try:
        if not Threading.threadPerform.is_alive():
            Threading.threadPerform.start()
        try:
            if not Threading.threadRaport.is_alive():
                Threading.threadRaport.start()
            try:
                with Threading.threadLockSleep5:
                    for t in Threading.threads5:
                        t.join()
                    threadSleep5 = Threading.myThread(4, "ThreadSleep5", 5)
                    threadSleep5.start()
                    Threading.threads5.append(threadSleep5)
            except:
                print('Error sleep')
        except:
            print('Error with creating and sending daily raport')
            MailExchanging.sendMail(MailExchanging.MailVariables.subRaportError,
                                    MailExchanging.MailVariables.textRaportError,
                                    MailExchanging.MailVariables.recMailsErrors)
        try:
            if not Threading.threadDeleting.is_alive():
                Threading.threadDeleting.start()
            try:
                with Threading.threadLockSleep30:
                    for t in Threading.threads30:
                        t.join()
                    threadSleep30 = Threading.myThread(5, "ThreadSleep30", 30)
                    threadSleep30.start()
                    Threading.threads30.append(threadSleep30)
            except:
                    print('Error sleep')
        except:
            print('Error with deleting year-time spools')
            MailExchanging.sendMail(MailExchanging.MailVariables.subDeletingError,
                                    MailExchanging.MailVariables.textDeletingError,
                                    MailExchanging.MailVariables.recMailsErrors)
    except KeyboardInterrupt:
        print('Manual break by user')
        MailExchanging.sendMail(MailExchanging.MailVariables.subKeyboardInterruptError,
                                MailExchanging.MailVariables.textKeyboardInterruptError,
                                MailExchanging.MailVariables.recMailsErrors)
    try:
        with Threading.threadLockSleep5:
            for t in Threading.threads5:
                t.join()
            threadSleep5 = Threading.myThread(4, "ThreadSleep5", 5)
            threadSleep5.start()
            Threading.threads5.append(threadSleep5)
    except:
        print('Error sleep HERE')
