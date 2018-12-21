#       -----  GLOBAL IMPORTS ------
import datetime  # Imports datetime module for getting date and time

#       -----  IMPORTS FROM PROJECT ------
import CSVExchanging
import MailExchanging
import psycopg2  # Imports psycopg2 module for communication with PostgreSQL


def sendDailyRaport():
    cur = CSVExchanging.connectDB().cursor()

    dateDayBeforeBadFormat = (datetime.datetime.now() - datetime.timedelta(hours=24))
    dateForMail = (dateDayBeforeBadFormat.strftime("%d.%m.%Y"))
    dateTimeDayBefore = (dateDayBeforeBadFormat.strftime("%Y-%m-%d"))

    diameterForMail = ''
    materialForMail = ''
    colorForMail = ''

    #  ----- FINDING TOTAL NUMBER OF SPOOLS BY DATE FOR MAIL -----
    queryForTotalNumber = 'SELECT COUNT(*) FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                          ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\';'
    cur.execute(queryForTotalNumber)
    numOfSpools = cur.fetchone()[0]

    #  ----- FINDING DIFFERENT DIAMETER VALUES BY DATE FOR MAIL -----
    queryForDiameterValues = 'SELECT DISTINCT diameter FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                             ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY diameter;'
    cur.execute(queryForDiameterValues)
    valOfSpoolDiameter = cur.fetchall()

    for value in valOfSpoolDiameter:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE diameter = \'' + str(value)[
                                                                                      1:-2] + '\' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolDiameter = cur.fetchone()[0]
        diameterSubtext = 'With diameter ' + str(value)[1:-2] + ': ' + str(numWithSpoolDiameter)
        diameterForMail = diameterForMail + diameterSubtext + '\n'

    '''
    #  ----- FINDING DIFFERENT MASS VALUES BY DATE FOR MAIL -----
    queryForMassValues = 'SELECT DISTINCT mass FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                         ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY mass;'
    cur.execute(queryForMassValues)
    valOfSpoolMass = cur.fetchall()

    for value in valOfSpoolMass:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE mass = \'' + str(value)[
                                                                                  1:-2] + '\' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolMass = cur.fetchone()[0]
        massSubtext = 'With mass ' + str(value)[1:-2] + ': ' + str(numWithSpoolMass)
        massForMail = massForMail + massSubtext + '\n'
    '''
    #  ----- FINDING DIFFERENT MATERIAL VALUES BY DATE FOR MAIL -----
    queryForMaterialValues = 'SELECT DISTINCT material FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                             ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY material;'
    cur.execute(queryForMaterialValues)
    valOfSpoolMaterial = cur.fetchall()

    for value in valOfSpoolMaterial:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE material = ' + str(value)[
                                                                                    1:-2] + ' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolMaterial = cur.fetchone()[0]
        materialSubtext = 'With material ' + str(value)[1:-2] + ': ' + str(numWithSpoolMaterial)
        materialForMail = materialForMail + materialSubtext + '\n'

    #  ----- FINDING DIFFERENT COLOR VALUES BY DATE FOR MAIL -----
    queryForColorValues = 'SELECT DISTINCT ColorName FROM spool WHERE date BETWEEN \'' + dateTimeDayBefore + \
                          ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\' ORDER BY ColorName;'
    cur.execute(queryForColorValues)
    valOfSpoolColor = cur.fetchall()

    for value in valOfSpoolColor:
        queryForSameValuesNumber = 'SELECT COUNT(*) FROM spool WHERE ColorName = ' + str(value)[
                                                                                     1:-2] + ' AND date BETWEEN \'' + \
                                   dateTimeDayBefore + ' 00:00:00\' AND \'' + dateTimeDayBefore + ' 23:59:59\''
        cur.execute(queryForSameValuesNumber)
        numWithSpoolColor = cur.fetchone()[0]
        colorSubtext = 'With color ' + str(value)[1:-2] + ': ' + str(numWithSpoolColor)
        colorForMail = colorForMail + colorSubtext + '\n'

    CSVExchanging.connectDB().close()

    mailSubject = 'Spool production raport for ' + dateForMail
    if numOfSpools > 0:
        mailText = 'Total spools produced: ' + str(numOfSpools) + '\n\n' + \
                   ' \t----- Diameter value: number of spools with this diameter ----- \n' + diameterForMail + '\n' + \
                   ' \t----- Material value: number of spools with this material ----- \n' + materialForMail + '\n' + \
                   ' \t----- Color value: number of spools with this color ----- \n' + colorForMail + '\n'
    else:
        mailText = 'Total spools produced: ' + str(numOfSpools) + '\n\n' + 'No spools produced this day!'
    MailExchanging.sendMail(mailSubject, mailText, MailExchanging.MailVariables.recMails)


def deleteSpool():
    cur = CSVExchanging.connectDB().cursor()

    dateTimeYearBeforeBadFormat = (datetime.datetime.now() - datetime.timedelta(days=366))
    dateYearBeforeForMail = (dateTimeYearBeforeBadFormat.strftime("%d.%m.%Y"))
    dateTimeYearBeforeStart = (dateTimeYearBeforeBadFormat.strftime("%Y-%m-%d") + ' 00:00:00')
    dateTimeYearBeforeEnd = (dateTimeYearBeforeBadFormat.strftime("%Y-%m-%d") + ' 23:59:59')

    queryDelete = 'DELETE FROM spool WHERE date = (SELECT date FROM spool WHERE date BETWEEN \'' + \
                  dateTimeYearBeforeStart + '\' AND \'' + dateTimeYearBeforeEnd + '\');'
    cur.execute(queryDelete)

    CSVExchanging.connectDB().close()

    mailSubject = 'Deleted all spools produced ' + dateYearBeforeForMail
    mailText = 'Spools that were produced ' + dateYearBeforeForMail + ' were deleted from database!'
    MailExchanging.sendMail(mailSubject, mailText, MailExchanging.MailVariables.recMails)


def main():
    while True:
        if datetime.datetime.now().strftime('%X') == '00:00:00':
            try:
                sendDailyRaport()
            except:
                print('Error with creating and sending daily raport')
                MailExchanging.sendMail(MailExchanging.MailVariables.subRaportError,
                                        MailExchanging.MailVariables.textRaportError,
                                        MailExchanging.MailVariables.recMailsErrors)
            try:
                deleteSpool()
            except:
                print('Error with deleting year-time spools')
                MailExchanging.sendMail(MailExchanging.MailVariables.subDeletingError,
                                        MailExchanging.MailVariables.textDeletingError,
                                        MailExchanging.MailVariables.recMailsErrors)


if __name__ == '__main__':
    main()
