"""
Few steps to make it work:
* Step 1 and 2 can be done by goin to link: https://www.google.com/settings/security/lesssecureapps *
1. Press icon of your account and under Safety go to 'Apps, that have access to your account';
2. There change the status on bottom to 'Unsafe apps allowed';
3. Go to link: https://accounts.google.com/DisplayUnlockCaptcha and follow steps that will allow to access accounts
from other apps.
* After this run the code *
"""
#       -----  GLOBAL IMPORTS ------
import smtplib  # Imports smtplib module for mail communication


#       -----  GLOBAL VARIABLES NEEDED FOR MAIL COMMUNICATION  ------
class MailVariables:
    subFileSavingError = 'Error with saving CSV file '
    textFileSavingError = 'Error exists. Could not save file '

    subFileReadingError = 'Error with reading CSV file '
    textFileReadingError = 'Error exists. Could not read file '

    subFileUnexpectedError = 'Unexpected error with CSV file '
    textFileUnexpectedError = 'Unexpected error appeared while tried to save file '

    subFileNotExistError = 'File does not exists'
    textFileNotExistError = 'Cant read file, bacause it does not exist.'

    subDataReceivingError = 'Error with receiving data'
    textDataReceivingError = 'Receiving data disallowed! Error appeared. ' \
                             'Socket is probably not connected and no address was supplied.'

    subDataHashingError = 'Unexpected error with hashing CSV file '
    textDataHashingError = 'Unexpected error appeared while tried to hash name of file '

    subDatabaseError = 'Error with writing to database'
    textDatabaseError = 'Error appeared with writing to database.'

    subRaportError = 'Error with creating and sending daily raport'
    textRaportError = 'Daily raport hasn\'t been sent! Error exists.'

    subDeletingError = 'Error with deleting year-time spools'
    textDeletingError = 'Spools produced year ago haven\'t been deleted! Error exists.'

    subFileAppendingError = 'Unexpected error with appending'
    textFileAppendingError = 'Unexpected error appeared while tried to append next CSV file.'

    subKeyboardInterruptError = 'Manual break by user'
    textKeyboardInterruptError = 'Executing stopped because of manual breaking by user (all connections closed).'

    subConnectionError = 'Error with connection to server'
    textConnectionError = 'Connection declined! Trying again in 30 seconds.'

    acqsysMail = 'acqsys@mora-solutions.com'
    acqsysPass = '!koMORA1'

    recMails = ['michal@spectrumfilaments.com', 'maciejjakubek@gmail.com', 'sergey.dko@gmail.com']
    recMailsErrors = ['maciejjakubek@gmail.com', 'sergey.dko@gmail.com']


#       -----  EXECUTES MAIL COMMUNICATION  ------
def sendMail(subject, text, mailsRecv):
    server = smtplib.SMTP('smtp.mora-solutions.com', 587)
    server.ehlo()
    server.starttls()
    server.login(MailVariables.acqsysMail, MailVariables.acqsysPass)
    for mailTo in mailsRecv:
        body = '\r\n'.join(['To: %s' % mailTo,
                            'From: %s' % MailVariables.acqsysMail,
                            'Subject: %s' % subject,
                            '', text])

        server.sendmail(MailVariables.acqsysMail, [mailTo], body)
    print('Email successfully sent!')
