#!/usr/bin/env python
import argparse
from datetime import datetime
import logging
import re
import csv
from os import listdir, makedirs
from os.path import join, expanduser, normpath
import errno

VERSION = '1.0'
DOWNLOADS_DIR = '~/Downloads'
DOCUMENTS_DIR = '~/Documents/HSBC Statements'

def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def fix(file_in):
    all_rows = []

    # read csv
    with open(file_in, 'r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            all_rows.append(row)
        if len(all_rows) < 2:
            logger.error('No transactions')
            return
        from_date = datetime.strptime(all_rows[1][0], '%d %b %Y').strftime('%Y%m%d')
        to_date = datetime.strptime(all_rows[-1][0], '%d %b %Y').strftime('%Y%m%d')

    # fix for crunch
    for row in reversed(all_rows[1:]):
        if is_number(row[3]):
            method = 'out'
            row[4] = 0.0
        else:
            method = 'in'
            row[3] = 0.0

        if is_number(row[5]):
            balance = float(row[5])
        else:
            row[5] = str(balance)

        if method == 'out':
            balance += float(row[3])
        elif method == 'in':
            balance -= float(row[4])

    # write Crunch-proof csv
    file_out = join(args.output_dir, 'transactions.%s-%s.csv' % (from_date, to_date))
    with open(file_out, 'w') as csv_out:
        writer = csv.writer(csv_out, quoting=csv.QUOTE_NONNUMERIC)
        for row in all_rows:
            writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', help='input directory', action='store', default=normpath(expanduser(DOWNLOADS_DIR)))
    parser.add_argument('--output-dir', help='output directory', action='store', default=normpath(expanduser(DOCUMENTS_DIR)))
    parser.add_argument('-V', '--version', action='version', version='HSBC Statement Fixer for Crunch Accounting %s' % VERSION, help='show version and exit')
    args = parser.parse_args()

    logger = logging.getLogger('fixer_logger')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    pattern = re.compile("Transactions(-[0-9]+)?\.csv")
    files = [ join(args.input_dir, f) for f in listdir(args.input_dir) if pattern.match(f) ]

    if len(files):
        try:
            makedirs(args.output_dir)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
        for file in files:
            fix(file)

        print('Files written to %s: %d' % (args.output_dir, len(files)))
