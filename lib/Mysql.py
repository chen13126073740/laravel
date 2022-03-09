import pymysql
from lib.Config import Config
from datetime import datetime, timedelta, timezone


class Mysql:
    _table = ''
    _where = ''
    _order = ''
    _limit = ''
    _select = ''

    def __init__(self, table):
        config = Config.get('database')
        self._table = config['prefix'] + table
        try:
            self.conn = pymysql.connect(
                host=config['host'],
                user=config['user'],
                passwd=config['passwd'],
                port=config['port'],
                charset=config['charset'],
                db=config['db']
            )
        except Exception as e:
            print(e)
        else:
            print(table + ': 连接成功')
            self.cur = self.conn.cursor()

    # 通用执行
    def execute(self, sql):
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        return res

    def _query(self, sql):
        self.cur.execute(sql)
        col = self.cur.description
        res = self.cur.fetchall()
        return col, res

    # 通用查询
    def query(self, sql):
        col, res = self._query(sql)
        result = []
        for re in res:
            row = {}
            for index in range(len(re)):
                row[col[index][0]] = re[index]
            result.append(row)

        return result

    # 处理条件
    def where_action(self, give='AND'):
        if self._where != '':
            self._where = self._where + give + ' '
        else:
            self._where = ' WHERE '

    # 条件
    # 'id','a1' 默认 =
    # 'id','>','2'
    def where(self, field, symbol, value=None):

        if value is None:
            value = symbol
            symbol = '='

        self.where_action()
        self._where = self._where + field + ' ' + symbol + ' \'' + value + '\' '
        return self

    def whereOr(self, field, symbol, value):
        self.where_action('OR')
        self._where = self._where + field + ' ' + symbol + ' \'' + value + '\' '
        return self

    def whereIn(self, field, data):
        self.where_action()
        data = data.split(',')
        for index in range(len(data)):
            data[index] = '\'' + data[index] + '\''
        data = ','.join(data)
        self._where = self._where + field + ' IN (' + data + ') '
        return self

    def orderBy(self, sort, order):
        self._order = self._order + 'ORDER BY ' + sort + ' ' + order + ' '
        return self

    def limit(self, start, count):
        self._limit = self._limit + 'LIMIT ' + str(start) + ',' + str(count) + ' '
        return self

    def select(self, field):
        field = ','.join(field)
        self._select = field
        return self

    # 操作
    def page(self, page, limit):
        self._limit = self._limit + 'LIMIT ' + str((page - 1) * limit) + ',' + str(limit) + ' '
        return self.get()

    def get(self):
        if self._select == '':
            self._select = '*'
        sql = 'SELECT ' + self._select + ' FROM ' + self._table + ' ' \
              + self._where + self._order + self._limit
        result = self.query(sql)
        return result

    def count(self):
        sql = 'SELECT count(35) FROM ' + self._table + ' ' \
              + self._where + self._order + self._limit
        result = self.query(sql)
        return int(result[0]['count(35)'])

    def first(self):
        return self.get()[0]

    def pluck(self, field):
        self._select = field
        sql = 'SELECT ' + self._select + ' FROM ' + self._table + ' ' \
              + self._where + self._order + self._limit
        col, res = self._query(sql)
        result = []
        for row in res:
            for column in row:
                result.append(column)
        return result

    def save(self, data):

        data['created_at'] = self._now()
        data['updated_at'] = self._now()

        field = []
        value = []
        for key in data:
            if data[key] is None:
                field.append(key)
                value.append('null')
            else:
                field.append(key)
                data[key] = data[key].replace('\'', '\'\'')
                value.append(data[key])

        field = self._format_value(field, char='')
        value = self._format_value(value)
        sql = 'INSERT INTO ' + self._table + ' (' + field + ') VALUES (' + value + ')'
        result = self.execute(sql)
        return data

    def update(self, data):
        data['updated_at'] = self._now()
        value = []
        for key in data:
            if data[key] is None:
                value.append(key + '=null')
            else:
                data[key] = data[key].replace('\'', '\'\'')
                value.append(key + '=\'' + data[key] + '\'')

        value = ','.join(value)
        sql = 'UPDATE ' + self._table + ' SET ' + value
        if self._where != '':
            sql = sql + ' WHERE ' + self._where
        self.execute(sql)
        return data

    def delete(self):
        obj = self.update({
            'deleted_at': self._now()
        })
        return obj


    # 判断是否已软删除
    def trashed(self):
        pass

    # 恢复软删除
    def restore(self):
        obj = self.update({
            'deleted_at': None
        })
        return obj

    # 物理删除
    def forceDelete(self):
        sql = 'DELETE FROM ' + self._table + self._where
        self.execute(sql)
        pass

    def updateOrCreate(self, condition, data):
        # where = ''
        where = 'deleted_at IS NULL'
        for key in condition:
            if where != '':
                where = where + ' AND '
            # where = where + '' + key + '=\'' + condition[key] + '\' '
            where = where + '' + key + '=\"' + condition[key] + '\" '
        self._where = where
        sql = 'SELECT * FROM ' + self._table + " WHERE " + where
        col, res = self._query(sql)
        # print(sql)
        if len(res) == 0:  # 创建
            return self.save(data)
        else:
            return self.update(data)

        # 返回对象
        # return len(res)

    def _now(self):
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        return cn_dt.strftime('%Y-%m-%d %H:%M:%S')

    def _format_value(self, list, delimit=',', char='\''):
        str = (char + delimit + char).join(list)
        str = char + str + char
        return str
