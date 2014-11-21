import logging
import os
import sqlite3
from datetime import datetime


class SQLiteHandler(logging.Handler): # Inherit from logging.Handler
    """
    Logging handler that write logs to SQLite DB
    """
    def __init__(self, filename):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Our custom argument
        self.baseFilename = filename
        self.db = sqlite3.connect(filename) # might need to use self.filename
        self.db.execute("CREATE TABLE IF NOT EXISTS logging(created datetime, name text, level text, pathname text, lineno integer, func text, msg text)")
        self.db.commit()

    def emit(self, record):
        # record.message is the log message
        thisdate = datetime.now()
        self.db.execute(
            'INSERT INTO logging(created, name, level, pathname, lineno, func, msg) VALUES(?,?,?,?,?,?,?)',
            (
                datetime.fromtimestamp(record.created),
                record.name,
                record.levelname,
                os.path.abspath(record.filename),
                record.lineno,
                record.funcName,
                record.getMessage(),
            )
        )
        self.db.commit()
