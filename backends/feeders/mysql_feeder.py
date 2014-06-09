from backends.mysql_helper import Database


class MySQLDomainFeeder():

    def __init__(self, credentials, conf):
        self.db = Database(credentials['host'], credentials['user'],
                      credentials['pass'], credentials['database'])
        self.src_table = conf.pop('src_table', None)
        self.src_fields = conf.pop('src_column', None)
        self.where = conf.pop('src_where', '')
        self.groupby = conf.pop('src_groupby', '')
        self.orderby = conf.pop('src_orderby', '')

    def domainloader(self):
        limit = '%d,%d' % (self.counter, self.load_count)
        self.db.select(self.src_fields, self.src_table, self.groupby, self.orderby, limit)
        while True:
            domain = self.db.cursor.fetchone()
            if not domain:
                break
            yield domain
        return False