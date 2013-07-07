import sqlite3
import logging

import os
abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname)

class Connection:
    def __init__(self, database='sqlite3.db'):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        logging.info('Opened database %s' % database)

    def __del__(self):
        self.connection.close()
        logging.info('Closed database')

    def get_message(self, pk):
        self.cursor.execute('SELECT data FROM messages WHERE pk=?', (pk,) )
        return self.cursor.fetchone()[0]

    def update_messages(self, messages):
      for msg in messages:
          self.cursor.execute('UPDATE messages SET data=? WHERE pk=?', (msg['data'], msg['pk']) )
      self.connection.commit()

    def initialize(self, messages):
        try:
            self.cursor.execute('CREATE TABLE messages (pk integer primary key, data varchar)')
            logging.info('Created message table!')
        except sqlite3.OperationalError:
            logging.info('Failed to create messages table since it exists.')
            return False

        for msg in messages:
            try:
                self.cursor.execute('INSERT INTO messages (pk, data) VALUES(?, ?)', (msg['pk'], msg['data']) )
            except sqlite3.IntegrityError:
                logging.warning('Attempted to INSERT an existing message.')
        self.connection.commit()
        return True

