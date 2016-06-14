#!/usr/bin/env python3
import ConfigParser
import os
import argparse
from datetime import datetime
from common import valid_date, log_setup, check_task
import logging

class Configuration:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def set_up(self, *import_sections):
        parser = ConfigParser.ConfigParser()
        local_path = os.path.dirname(os.path.abspath(__file__))
        parser.read(os.path.join(local_path, 'config.ini'))
        for section in parser.sections():
            if section in import_sections:
                self.__dict__.update(parser.items(section))



conf = Configuration()

def get_args():
    parser = argparse.ArgumentParser(description="desc", version="version 0.1")
    parser.add_argument('-e', dest='env',choices=['dev1', 'dev2', 'test', 'pdn'],
                        type = str.upper(), help='define env for config to use', required=True)
    return parser.parse_args()


def main():
    package_start_time = datetime.now()
    try:
        arg_val = get_args()
        conf.set_up('GENERAL', arg_val.env)
        log_setup('testlog')
    except Exception:
        logging.error()

class Database:
    def __init__(self, db_name):
        try:
            logging.info('connecting to db...')
            self.cnxn = pyodbc.connect('DRIVER={SQl Server}; Server=' + config.db_server + ';Database=' + db_name
                                       + ';Trusted_Connection=Yes;')
            logging.info('connected to db')
            self.cursor = self.cnxn.cursor()
        except pyodbc.Error as e:
            logging.error('db connection error: {}'.format(e.args[1]))
            raise

    def get_data(self, sql):
        try:
            logging.info('runing get data sql ... : {}'.format(sql))
            self.cursor.execute(sql)
            logging.info('complete')
            return self.cursor.fetchall()
        except pyodbc.DatabaseError as e:
            logging.error('sql error: {}'.format(e.args[1]))
            raise

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        self.cnxn.commit()

    def truncate_table(self, truncate_table):
        try:
            trunc_sql = 'truncate table ' + truncate_table
            self.execute_sql(trunc_sql)
            logging.info(trunc_sql)
        except pyodbc.DatabaseError as e:
            logging.error('sql error: {}'.format(e.args[1]))
            raise


