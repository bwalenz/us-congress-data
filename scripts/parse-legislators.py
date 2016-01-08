#!/usr/bin/env python

import sys
import codecs
import datetime
import yaml

raw_path = "raw"
data_path = "data"

# Try to use the faster C-based yaml parser:
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Open database load files for writing:
STATES = codecs.open(data_path + '/states.dat', 'w', 'utf-8')
PERSONS = codecs.open(data_path +  '/persons.dat', 'w', 'utf-8')
PERSON_ROLES = codecs.open(data_path + '/person_roles.dat', 'w', 'utf-8')
LEADERSHIP = codecs.open(data_path + '/leadership.dat', 'w', 'utf-8')

states = set()

def print_person(person):
    print('{} {}'.format(person['name']['first'], person['name']['last']))
    # Use of .get(key, '') below allows us to set the default to ''
    # (which will be interpreted by the database loader as NULL) if
    # the key is missing:
    print('{}|{}|{}|{}|{}|{}|{}|{}'.format(
        person['id']['bioguide'],
        person['id']['govtrack'],
        person['id'].get('lis', ''), 
        person['name']['first'],
        person['name'].get('middle', ''),
        person['name']['last'],
        person['bio'].get('birthday', '') if 'bio' in person else '',
        person['bio'].get('gender', '') if 'bio' in person else ''), file=PERSONS)
    for role in person['terms']:
        if role['state'] not in states:
            states.add(role['state'])
        print('{}|{}|{}|{}|{}|{}|{}'.format(
            person['id']['bioguide'],
            role['type'],
            role['start'],
            role['end'],
            role['state'], 
            role.get('district', ''),
            role.get('party', '')), file=PERSON_ROLES)
    for leader in person.get('leadership_roles', []):
                print('{}|{}|{}|{}|{}'.format(
                    person['id']['bioguide'],
            leader['title'],
                        leader['chamber'],
                        leader['start'],
                        leader.get('end', '')), file=LEADERSHIP)

# Process current legislators:
print("*****loading current legislators*****")
persons = yaml.load(open(raw_path + '/legislators-current.yaml', 'r'),
                    Loader=Loader)
for person in persons:
    print_person(person)

# Even if we are interested only in legistrators in the current
# congress (113th), we still need to process some non-current
# leigstrators, like John Kerry, who resigned from the senate before
# the end of his term to become the Secretary of the State.
def is_relevant(person):
    # This filter defines which one of historical legislators still
    # need to be processed.  By default we get everybody.
    return True
    # Uncomment the follow to restrict processing to those who might
    # have served in the 113th congress, with a lenient cut-off of
    # 2012-07-01:
    # return 'terms' in person and \
    #     filter(lambda role: 'end' in role and \
    #            datetime.datetime.strptime(role['end'], '%Y-%m-%d').date() \
    #            >= datetime.date(2012, 7, 1),
    #            person['terms'])

# Process non-current legistrators:
print("***** loading historical legislators *****")
persons = yaml.load(open(raw_path + '/legislators-historical.yaml', 'r'),
                    Loader=Loader)
for person in persons:
    if is_relevant(person):
        print_person(person)

PERSONS.close()
PERSON_ROLES.close()

# Print out the states we found:
for state in sorted(states):
    print('{}'.format(state), file=STATES)
STATES.close()
