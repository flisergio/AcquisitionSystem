"""
Few steps to make it work:
* Step 1 and 2 can be done by goin to link: https://www.google.com/settings/security/lesssecureapps *
1. Press icon of your account and under Safety go to 'Apps, that have access to your account';
2. There change the status on bottom to 'Unsafe apps allowed';
3. Go to link: https://accounts.google.com/DisplayUnlockCaptcha and follow steps that will allow to access accounts
from other apps.
* After this run the code *
"""

import smtplib  # Imports smtplib module for mail communication

#       -----  GLOBAL VARIABLES NEEDED FOR MAIL COMMUNICATION  ------
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

subFileAppendingError = 'Unexpected error with appending'
textFileAppendingError = 'Unexpected error appeared while tried to append next CSV file.'

subKeyboardInterruptError = 'Manual break by user'
textKeyboardInterruptError = 'Executing stopped because of manual breaking by user (all connections closed).'

subConnectionError = 'Error with connection to server'
textConnectionError = 'Connection declined! Trying again in 30 seconds.'

myPass = '!koMORA1'


#       -----  EXECUTES MAIL COMMUNICATION  ------
def sendMail(subject, text):
    myMail = 'acqsys@mora-solutions.com'
    recMails = ['maciejjakubek@gmail.com', 'sergey.dko@gmail.com']
    server = smtplib.SMTP('smtp.mora-solutions.com', 587)
    server.ehlo()
    server.starttls()
    server.login(myMail, myPass)
    for recMail in recMails:
        body = '\r\n'.join(['To: %s' % recMail,
                            'From: %s' % myMail,
                            'Subject: %s' % subject,
                            '', text])

        server.sendmail(myMail, [recMail], body)
    print('Emails successfully sent!')
