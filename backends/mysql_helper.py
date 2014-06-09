import mysql.connector as mc


class Database():

    def __init__(self, host, user, passwd, database, debug=None):
        self.debug = debug
        self.conn = mc.connect(user=user, password=passwd,
                               host=host,
                               database=database)
        self.cursor = self.conn.cursor()

    def select(self, fields, tables, where='', group_by='', order_by='', limit=''):
        query = 'SELECT %s FROM %s' % (','.join(fields), tables)
        if where:
            query += ' WHERE %s' % where
        if group_by:
            query += ' GROUP BY %s' % group_by
        if order_by:
            query += ' ORDER BY %s' % order_by
        if limit:
            query += ' LIMIT %s' % limit

        if self.debug:
            print(query)
        self.cursor.execute(query)
        return True

    def insert(self, fieldvalues, table):
        fields = []
        values = []
        for f, v in fieldvalues.items():
            fields.append(f)
            if isinstance(v, int) or isinstance(v, float):
                values.append(v)
            elif isinstance(v, bytes):
                values.append('"' + v.decode('utf-8') + '"')
            else:
                values.append('"' + v + '"')

        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, ', '.join(fields), values)
        if self.debug:
            print(query)

        self.cursor.execute(query)
        self.conn.commit()
        return True

    def update(self, fieldvalues, table, where=''):
        newvalues = []
        for f, v in fieldvalues.items():
            if isinstance(v, int) or isinstance(v, float):
                newvalues.append(f + ' = ' + str(v))
            elif isinstance(v, bytes):
                newvalues.append(f + ' = "' + v.decode('utf-8') + '"')
            else:
                newvalues.append(f + ' = "' + v + '"')

        query = 'UPDATE %s SET %s' % (table, ', '.join(newvalues))
        if where:
            query += ' WHERE %s' % where

        if self.debug:
            print(query)
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()


