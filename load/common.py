#!/usr/bin/env python3
from datetime import datetime
import argparse
import logging
import subprocess
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '_'))
from load import Configuration

conf = Configuration()

def valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return date_str
    except ValueError:
        msg = 'Not a valid date: {0}'.format(date_str)
        raise argparse.ArgumentTypeError(msg)

def log_setup(log_name):
    log_file_name = log_name + '-' + str(datetime.today().strftime("%Y%m%d%H%M%S")) + '.log'
    logging.basicConfig(format = '%(asctime)s %(levelname)s %(threadNames :%(message)s',
                        filename=os.path.join(conf.log_path, log_file_name),
                        level=logging.DEBUG,
                        filemode='w')
    logging.info('starting package')
    logging.info('parameters:')
    for key, val in conf.__dict__.items():
        logging.info('    {0}: {1}'.format(key.ljust(25), val))


