import httplib
import database
import logging

import os
abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname)

logging.basicConfig(filename='logs/worker.log', level=logging.ERROR)
connection = database.Connection()

def send_message(number, pk):
    message = connection.get_message(pk)
    headers = {
        'X-Kannel-Username': 'traffic',
        'X-Kannel-Password': 'ThisIsMySecretKannelPassword',
        'X-Kannel-SMSC': 'smsc0',
        #'X-Kannel-SMSC': 'fakesmsc',
        'X-Kannel-Coding': 0,
        'X-Kannel-From': '09154266531',
        'X-Kannel-To': number
    }

    http = httplib.HTTPConnection('localhost', 10002)
    http.request('POST', '/sendsms', message, headers)
    response = http.getresponse()
    http.close()

    if response.status != 200:
        logging.error('Error %d: %s' % (response.status, response.reason) )
    else:
        logging.info('Sent message %d to %s' % (pk,number) )

