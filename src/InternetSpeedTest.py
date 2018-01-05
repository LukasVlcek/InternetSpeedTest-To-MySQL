#!/usr/bin/env python

import os
import sys
from datetime import datetime
import mysql.connector

def main():
    try:
        doSpeedTest()
    except Exception as e:
        print 'Error: %s' % e
        sys.exit(1)

    sys.exit()

def doSpeedTest():
    date = datetime.now()
    result = os.popen("/usr/local/bin/speedtest-cli --simple").read()
    if 'Cannot' in result:
        sendDataToDB(date, -999, -999, -999)

    resultSet = result.split('\n')
    pingResult = resultSet[0]
    downloadResult = resultSet[1]
    uploadResult = resultSet[2]

    pingResult = float(pingResult.replace('Ping: ', '').replace(' ms', ''))
    downloadResult = float(downloadResult.replace('Download: ', '').replace(' Mbit/s', ''))
    uploadResult = float(uploadResult.replace('Upload: ', '').replace(' Mbit/s', ''))

    sendDataToDB(date, pingResult, downloadResult, uploadResult)

def sendDataToDB(date, pingResult, downloadResult, uploadResult):
    config = {
        'user': '',
        'password': '',
        'host': '',
        'database': '',
        'raise_on_warnings': True,
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    data_template = ("INSERT INTO internet "
                     "(datetime, download, upload, ping)"
                     "VALUES (%s, %s, %s, %s)")
    data = (date, downloadResult, uploadResult, pingResult)

    cursor.execute(data_template, data)
    cnx.close()


if __name__ == '__main__':
    main();
