import re
import runner
from rq import Queue
from redis import Redis
from flask import Flask, request

app = Flask(__name__)
queue = Queue(connection=Redis())

globe = re.compile(r'You have just been shared P([0-9]+\.?[0-9]*) by (.+)\.')

@app.route('/', strict_slashes=False)
def receive_message():
    sender, message, secret = None, None, None
    try:
        sender = request.args['sender']
        message = request.args['message']
        secret = request.args['secret']
    except KeyError:
        return 'Nobody cares about you.'

    if secret != 'temporary' or sender != '2916':
        return 'Nobody cares about you too.'

    match = globe.match(message)
    if not match:
        return 'Nobody cares about you either.'

    amount = float(match.group(1))
    number = match.group(2)
    if amount < 1:
        return 'Nobody cares about you, cheapskate. %f'%amount

    for pk in xrange(0,5):
        queue.enqueue(runner.send_message, number, pk)

    return 'Well I care about you.'

if __name__ == '__main__':
    print 'Listening on port 8000...'
    app.run(host='127.0.0.1', port=8000, debug=True)

