#!/usr/bin/env python

import codecs
import sys
import os
import json
import csv

data_path = "data"
ROOT = "raw"

# Open database load files for writing:
BILLS = codecs.open(data_path + '/bills.dat', 'w', 'utf-8')
SUBJECTS = codecs.open(data_path + '/bills_subjects.dat', 'w', 'utf-8')

# Traverse the govtrack data directory to collect all bills info:

def parse_bills_in_dir(dir):
    '''
    Parse data.json files contained in a top-level bills directory
    For example: bills-113, bills-112
    '''
    for root, dirs, files in os.walk(os.path.join(ROOT, dir)):
        for filename in files:
            if filename != 'data.json':
                continue
            with codecs.open(os.path.join(root, filename), 'r', 'utf-8') as jsonfile:
                bill = json.load(jsonfile)

                print >> BILLS, u'{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(
                    bill['bill_id'],
                    bill['congress'],
                    bill['bill_type'],
                    bill['number'],
                    bill['status'],
                    bill['status_at'],
                    bill['official_title'],
                    bill['popular_title'] if bill['popular_title'] else '',
                    bill['short_title'] if bill['short_title'] else '')

                if bill['subjects']:
                    for subject in bill['subjects']:
                        print >> SUBJECTS, u'{}|{}'.format(
                            bill['bill_id'],
                            subject)

# ['bills-113', 'bills-112', 'bills-113', ...]
bill_dirs = filter(lambda x: x.startswith('bills'), os.walk(ROOT).next()[1])
for bill_dir in bill_dirs:
    print '***** Parsing bills in %s ...' % (bill_dir)
    parse_bills_in_dir(bill_dir)

BILLS.close()
