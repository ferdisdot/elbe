import logging
import os
import sqlite3
from datetime import datetime

create_table_sql  ="""CREATE TABLE IF NOT EXISTS logging(
    created datetime,
    name text,
    level integer,
    levelname text,
    module text,
    pathname text,
    lineno integer,
    func text,
    process int,
    thread text,
    threadName text,
    Exception text, 
    msg text
)"""

insert_sql = """INSERT INTO logging(
    created,
    name,
    level,
    levelname,
    module,
    pathname,
    lineno,
    func,
    process,
    thread,
    threadName,
    exception,
    msg
)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"""

class SQLiteHandler(logging.Handler): # Inherit from logging.Handler
    """
    Logging handler that write logs to SQLite DB
    """
    def __init__(self, filename):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Our custom argument
        self.baseFilename = filename
        self.db = sqlite3.connect(self.baseFilename)
        self.db.execute(create_table_sql)
        self.db.commit()

    def emit(self, record):
        if record.exc_info:
            exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            exc_text = None
        self.db.execute(insert_sql,
            (
                datetime.fromtimestamp(record.created),
                record.name,
                record.levelno,
                record.levelname,
                record.module,
                os.path.abspath(record.filename),
                record.lineno,
                record.funcName,
                record.process,
                record.thread,
                record.threadName,
                exc_text,
                record.getMessage(),
            )
        )
        self.db.commit()
