from pkg.database import *
from pypika import (
    AliasedQuery,
    Case,
    Field as F,
    MySQLQuery,
    Table,
    Tables,
    functions as fn,
)
from pypika.functions import (
    Avg,
    Cast,
)
from pypika.terms import *
from pkg import utils
from datetime import datetime

import pymysql
from pymysql import cursors

class MySQL(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    @property
    def connect(self):
        if self.app.config['pymysql_kwargs']:
            kwargs = self.app.config['pymysql_kwargs']
            if 'cursorclass' in kwargs.keys():
                kwargs['cursorclass'] = getattr(cursors, kwargs['cursorclass'])
        else:
            kwargs = dict()

        return pymysql.connect(**kwargs)

    @property
    def connection(self):
        try:
            ctx = self.app.app_context()
            if ctx is not None:
                if not hasattr(ctx, 'mysql_db'):
                    ctx.mysql_db = self.connect
                return ctx.mysql_db
        except Exception as e:
            print("Eror: ", e)

    def teardown(self, exception):
        ctx = self.app.app_context()
        if hasattr(ctx, 'mysql_db'):
            ctx.mysql_db.close()

class MysqlBuilder():
    def __init__(self, mysql_client, table) -> None:
        self.database = mysql_client
        self.cursor = self.database.cursor()
        self.table = Table(table)
    
    def set_table(self, table):
        self.table = Table(table)

    def table(self):
        return self.table
    
    def query(self):
        return MySQLQuery().from_(self.table)

    def upsert(self, data):
        try:
            q = MySQLQuery.into(self.table).columns(*data.keys()).insert(*data.values())
            for column, value in data.items():
                q = q.on_duplicate_key_update(self.table[column], Values(self.table[column]))
        except Exception as e:
            raise e
        else:
            self.cursor.execute(q.get_sql())
            self.database.commit()
            return  self.cursor.lastrowid
        
    def insert(self, data):
        try:
            q = MySQLQuery.into(self.table).columns(*data.keys()).insert(*data.values())
        except Exception as e:
            raise e
        else:
            self.cursor.execute(q.get_sql())
            self.database.commit()
            return  self.cursor.lastrowid

    def exec(self, query):
        q = query.get_sql()
        try:
            self.cursor.execute(q)
        except Exception as e:
            raise e
        else:
            return self.cursor
        
    def meta(self, q, limit, page):
        q = q.select(fn.Count('*').as_('total'))
        query = q.get_sql()
        try:
            self.cursor.execute(query)
        except Exception as e:
            raise e
        else:
            return {
                'total': self.cursor.fetchone()['total'],
                'page': page if page <= 0 else page,
                'limit': limit,
                'page_next': page+1
            }
        
    def fetch(self, query):
        q = query.get_sql()
        print(q)
        try:
            self.cursor.execute(q)
        except Exception as e:
            raise e
        else:
            return self.cursor.fetchall()
        
    def fetch_row(self, query):
        q = query.get_sql()
        try:
            self.cursor.execute(q)
        except Exception as e:
            raise e
        else:
            return self.cursor.fetchone()
        
    def delete(self, id):
        q = MySQLQuery.update(self.table).set('deleted_at', datetime.now()).where(self.table.id == id)
        try:
            self.cursor.execute(q.get_sql())
        except Exception as e:
            raise e
        else:
            return True