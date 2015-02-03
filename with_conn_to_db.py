#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import MySQLdb
import psycopg2


class conn_to_mysql(object):

    def __init__(self, db='dw', config='db.ini'):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config)
        self.conn_to_mysql = MySQLdb.Connect(
            host=config_parser.get(db, 'host'),
            user=config_parser.get(db, 'user'),
            passwd=config_parser.get(db, 'passwd'),
            db=config_parser.get(db, 'db'),
            port=int(config_parser.get(db, 'port'))
        )
        self.conn_to_mysql.set_character_set('utf8')
        self.conn_to_mysql.ping(True)
        self.cursor_to_mysql = self.conn_to_mysql.cursor()

    def __enter__(self):
        return self.cursor_to_mysql

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_to_mysql.commit()
        self.cursor_to_mysql.close()
        self.conn_to_mysql.close()


class conn_to_pgsql(object):

    def __init__(self, db='www', config='db.ini'):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config)
        conn_to_pgsql = psycopg2.connect(
            "host=%s port=%s dbname=%s user=%s password=%s" % (
                config_parser.get(db, 'host'),
                config_parser.get(db, 'port'),
                config_parser.get(db, 'db'),
                config_parser.get(db, 'user'),
                config_parser.get(db, 'passwd')))
        conn_to_pgsql.set_client_encoding('UTF8')
        cur_server = conn_to_pgsql.cursor()

    def __enter__(self):
        return self.cursor_to_pgsql

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_to_pgsql.commit()
        self.cursor_to_pgsql.close()
        self.conn_to_pgsql.close()
        
if __name__ == "__main__":
#包装了一个上下文管理器，以后可以这么连接数据库了，自动commit 自动关连接 
#先导入：from with_conn_to_db import * ，然后直接使用：
    sql_str = 'select * from www_users limit 10'
    with conn_to_mysql() as db:
        db.execute(sql_str)
        data_set = db.fetchall()
        for i in data_set:
            print i

    sql_str2 = 'select * from piwik_log_visit limit 10'
    #conn_to_mysql db默认值为dw
    with conn_to_mysql(db='piwik') as db: 
        db.execute(sql_str2)
        data_set = db.fetchall()
        for i in data_set:
            print i

#     sql_str3 = 'show tables'
#     #conn_to_pgsql db默认值为www
#     with conn_to_pgsql() as db:
#         db.execute(sql_str3)
#         data_set = db.fetchall()
#         for i in data_set:
#             print i