#!/usr/bin/env python

import codecs
import sys
import os
import json
import csv

# Establish the mapping from person id_lis to person id (some votes in
# JSON are recorded using person id_lis, but we want person id
# instead):
data_path = "data"
raw_path = "raw"
people_id_lis = {}
with open(data_path + '/persons.dat') as personsfile:
    for row in csv.reader(personsfile, delimiter='|'):
        id = row[0]
        id_lis = row[2]
        if id_lis != '':
            people_id_lis[id_lis] = id

# Open database load files for writing:
VOTES = codecs.open(data_path + '/votes.dat', 'w', 'utf-8')
VOTES_RE_BILLS = codecs.open(data_path + '/votes_re_bills.dat', 'w', 'utf-8')
VOTES_RE_AMENDMENTS = codecs.open(data_path + '/votes_re_amendments.dat', 'w', 'utf-8')
VOTES_RE_NOMINATIONS = codecs.open(data_path + '/votes_re_nominations.dat', 'w', 'utf-8')
PERSON_VOTES = codecs.open(data_path + '/person_votes.dat', 'w', 'utf-8')

common_vote_codes = { 'Yea' : '+',
                      'Aye' : '+',
                      'Nay' : '-',
                      'No' : '-',
                      'Present' : 'P',
                      'Not Voting' : '0' }

# Traverse the govtrack data directory to collect all votes info:
# root = 'raw/votes-2013'
# dirs = os.walk(root).next()[1]
# jsonfiles = [ os.path.join(root, dir, 'data.json') for dir in dirs ]

root = 'raw'
# dirs = [..., 'votes-112', votes-2013', ...]
dirs = [x for x in next(os.walk(root))[1] if x.startswith('votes')]
for dir in dirs:
    subdirs = next(os.walk(os.path.join(root, dir)))[1]
    jsonfiles = [os.path.join(root, dir, subdir, 'data.json') for subdir in subdirs]

    # Process each JSON file:
    for jsonfile in jsonfiles:
        print('***** processing ' + jsonfile + ' *****')
        votes = json.load(codecs.open(jsonfile, 'r', 'utf-8'))
        # Use of .get(key, '') below allows us to set the default to ''
        # (which will be interpreted by the database loader as NULL) if
        # the key is missing:
        print('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(
            votes['vote_id'],
            votes['category'],
            votes['chamber'],
            votes['session'],
            votes['date'],
            votes['number'],
            # remove all occurrences of '\n', e.g. votes-2003/s332/data.json
            ''.join(votes.get('question', '').split('\n')),
            ''.join(votes.get('subject', '').split('\n')),
            ''.join(votes.get('type', '').split('\n')), 
            votes['result']), file=VOTES)
        if 'bill' in votes:
            print('{}|{}{}-{}'.format(
                votes['vote_id'],
                votes['bill']['type'],
                votes['bill']['number'],
                votes['bill']['congress']), file=VOTES_RE_BILLS)
        if 'amendment' in votes:
            print('{}|{}amdt{}-{}'.format(
                votes['vote_id'],
                votes['amendment']['type'][0],
                votes['amendment']['number'],
                votes['bill']['congress'] if 'bill' in list(votes.keys()) else '-1')  #e.g. votes-2003/s41/data.json, no "bill" for the amendment
                ,file=VOTES_RE_AMENDMENTS)
        if 'nomination' in votes:
            print('{}|{}|{}'.format(
                votes['vote_id'],
                votes['nomination']['number'].split('-')[0],  # non-integer value, e.g. votes-2009/s6/data.json, line 7
                votes['nomination']['title']), file=VOTES_RE_NOMINATIONS)
        if not (set(votes['votes'].keys()) <= set(common_vote_codes.keys())):
            print('non-standard vote types found')
            print(list(votes['votes'].keys()))
        for code, votes_with_code in votes['votes'].items():
            for vote in votes_with_code:
                if vote == 'VP':  # e.g. votes-2001/s65/data.json line 434
                    continue
                print('{}|{}|{}'.format(
                    votes['vote_id'],
                    people_id_lis[vote['id']] \
                        if vote['id'] in people_id_lis else vote['id'],
                    code), file=PERSON_VOTES)

VOTES.close()
VOTES_RE_BILLS.close()
VOTES_RE_AMENDMENTS.close()
VOTES_RE_NOMINATIONS.close()
PERSON_VOTES.close()
