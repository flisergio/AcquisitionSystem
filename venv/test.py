import datetime
import time

import CSVExchanging
import MailExchanging
import Threading

try:
    Threading.threadPerform.start()
    try:
        Threading.threadRaport.start()
        Threading.threadSleep5.start()
    except:
        print('Error with creating and sending daily raport')
        MailExchanging.sendMail(MailExchanging.MailVariables.subRaportError,
                                MailExchanging.MailVariables.textRaportError,
                                MailExchanging.MailVariables.recMailsErrors)
    try:
        Threading.threadDeleting.start()
        Threading.threadSleep30.start()
    except:
        print('Error with deleting year-time spools')
        MailExchanging.sendMail(MailExchanging.MailVariables.subDeletingError,
                                MailExchanging.MailVariables.textDeletingError,
                                MailExchanging.MailVariables.recMailsErrors)
    for t in Threading.threads:
        t.join()
except KeyboardInterrupt:
    print('Manual break by user')
    MailExchanging.sendMail(MailExchanging.MailVariables.subKeyboardInterruptError,
                            MailExchanging.MailVariables.textKeyboardInterruptError,
                            MailExchanging.MailVariables.recMailsErrors)
