import csv
import json

import CSVExchanging


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        str(o).replace('T', ' ')
        return o.isoformat()


def JSONWrite(hashid):
    cur = CSVExchanging.connectDB().cursor()

    queryForCSV = 'SELECT spoolnumber, pathcsv FROM spool WHERE hashid = \'' + hashid + '\';'
    cur.execute(queryForCSV)
    queryForCSVResult = cur.fetchone()

    filePathAttributes = str(queryForCSVResult).split(', ')
    fileLocation = str(filePathAttributes[1])[1:-2]
    fileName = str(filePathAttributes[0])[1:]
    filePath = fileLocation + str(fileName) + '.csv'

    myFilePath = 'spools/' + str(fileName) + '.csv'

    attributes = ['Ovality', 'Mean', 'StdDev', 'Length']
    values = [999, 999, 999, 999]
    valuesX = []
    valuesY = []

    fileCSV = open(myFilePath, 'r')
    csv_reader = csv.reader(fileCSV, delimiter=';')

    while True:
        try:
            for line in csv_reader:
                if len(line) == 5:
                    valueY = str(str(line).split(', ')[2])[1:-1]
                    if valueY != 'Length':
                        valueY = float(valueY)
                        firstValueX = float(str(line).split(', ')[3][1:-1])
                        secondValueX = float(str(line).split(', ')[4][1:-2])
                        valueXBadFormat = (firstValueX + secondValueX) / 2
                        valueX = round(valueXBadFormat, 3)

                        valuesX.append(valueX)
                        valuesY.append(valueY)
                try:
                    for attribute in attributes:
                        attributeNameValueSplit = str(line).split(',')
                        attributeNameBadFormat = str(attributeNameValueSplit[0])
                        attributeName = attributeNameBadFormat[2:-1]
                        if attributeName == attribute:
                            attributeValueSplit = str(attributeNameValueSplit[1])
                            attributeValue = attributeValueSplit[2:-2]
                            if attributeValue == '999':
                                if attributes.index(attribute) == 0 or attributes.index(
                                        attribute) == 1 or attributes.index(
                                    attribute) == 2:
                                    values[attributes.index(attribute)] = '!!!'
                                else:
                                    values[attributes.index(attribute)] = 999
                                continue
                            else:
                                values[attributes.index(attribute)] = attributeValue
                            break
                except:
                    break
            JSONOvality = values[0]
            JSONMean = values[1]
            JSONDev = values[2]
            JSONLength = values[3]

            fileCSV.close()
        except csv.Error:
            str(line).replace('\0', '')
            continue
        break

    queryForJSON = 'SELECT date, material, colorname, colorral, diameter, tolerance FROM spool WHERE hashid = \'' + hashid + '\';'
    cur.execute(queryForJSON)
    queryForJSONResult = cur.fetchone()
    JSONDate = queryForJSONResult[0]

    attributeListBadFormat = str(queryForJSONResult).split(')')
    attributeList = attributeListBadFormat[1]
    attributeListSplit = str(attributeList).split(', ')

    JSONMaterial = attributeListSplit[1]
    JSONColorName = attributeListSplit[2]
    JSONColorRal = attributeListSplit[3]
    JSONDiameter = attributeListSplit[4]
    JSONTolerance = attributeListSplit[5]

    spool = {
        'dateprod': str(JSONDate),
        'material': JSONMaterial[1:-1],
        'color': JSONColorName[1:-1],
        'ral': JSONColorRal[1:-1],
        'diameter': float(JSONDiameter),
        'tolerance': float(JSONTolerance),
        'ovality': float(JSONOvality),
        'mean': float(JSONMean),
        'deviation': float(JSONDev),
        'length': float(JSONLength),
        'labelY': valuesY,
        'labelX': valuesX
    }

    JSONSpool = json.dumps(spool, sort_keys=True, indent=1, default=default)
    print(type(JSONSpool))
    return str(JSONSpool)
