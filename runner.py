import httplib
import database
import logging

logging.basicConfig(filename='logs/worker.log', level=logging.DEBUG)
connection = database.Connection()

def send_message(number, pk):
    logging.debug('Working %d for %s' % (pk,number) )
    message = connection.get_message(pk)
    headers = {
        'X-Kannel-Username': 'traffic',
        'X-Kannel-Password': 'ThisIsMySecretKannelPassword',
        #'X-Kannel-SMSC': 'globetattoo',
        'X-Kannel-SMSC': 'fakesmsc',
        'X-Kannel-Coding': 0,
        'X-Kannel-From': '09154266531',
        'X-Kannel-To': number
    }

    logging.debug('Connecting to Kannel...' )
    http = httplib.HTTPConnection('localhost', 10002)
    http.request('POST', '/sendsms', message, headers)
    response = http.getresponse()
    http.close()

    if response.status != 200:
        logging.error('Error %d: %s' % (response.status, response.reason) )
    else:
        logging.debug('Sent message %d to %s' % (pk,number) )

