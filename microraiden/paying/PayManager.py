import sqlite3


CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS `content_buy` (
    `address` CHAR(42) NOT NULL,
    `content_id` CHAR(42) NOT NULL
)
'''

GET_CONTENT_BUY = '''
SELECT count(*) from content_buy
where address = '{address}' and content_id = '{content_id}'
'''

INSERT_CONTENT_BUY = '''
INSERT INTO `content_buy` (address, content_id) values ('{address}','{content_id}')
'''


class PayManager:
    def __init__(self):
        filename = 'buy_history.sqlite'
        self.filename = filename
        self.conn = sqlite3.connect(self.filename, isolation_level=None)
        self.conn.execute(CREATE_TABLE_SQL)

    def is_paid(self, address, content_id):
        cur = self.conn.cursor()
        cur.execute(GET_CONTENT_BUY.format(address=address, content_id=content_id))
        row_cnt = cur.fetchone()
        cur.close()
        if row_cnt[0]:
            return True
        else:
            return False

    def register_paid(self, address, content_id):
        cur = self.conn.cursor()
        cur.execute(INSERT_CONTENT_BUY.format(address=address, content_id=content_id))
        cur.close()


class PayManagerFactory:
    manager = None

    @classmethod
    def get_instance(cls):
        if cls.manager is None:
            cls.manager = PayManager()
        return cls.manager
