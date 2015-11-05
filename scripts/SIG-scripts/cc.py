# cc.py
# script that scape the chamber of commerce voter guide at https://www.uschamber.com/report/how-they-voted
# generates id using the info on the website and use the id to query the database
# last time validated: Oct 15, 2015
# Owner: Yubo Tian
from bs4 import BeautifulSoup
import nltk
import urllib.request
import psycopg2
import re
from optparse import OptionParser
import sys

MAIN_URL = 'https://www.uschamber.com'

print ("\nhello python script\n")

def get_votes(year):
	# result dictionary
	votes = []

	# get house votes
	# https://www.uschamber.com/how-they-voted-2014-house
	resp = urllib.request.urlopen(MAIN_URL+'/how-they-voted-'+str(year)+'-house')
	html = resp.read()
	soup = BeautifulSoup(html, "lxml")

	raw = soup.get_text()

	s = '1. 113-2-H-RC61 S. 540 - Debt Limit 2. 113-2-H-RC113 H.R. 2641 - RAPID Act 3. 113-2-H-RC182 H.R. 4414 - Expatriate Health Coverage Clarification Act of 2014'

	records = re.findall(r'\.\s?\d+-[12]-H-RC\d+', raw)

	for r in records:
		# process data and add to votes[]
		vote_number = re.search(r'RC\d+',r).group()[2:]
		congress = re.search(r'\d+-[12]-H-RC',r).group()[:-7]
		vote_id_generated = 'h' + str(vote_number) + '-' + str(congress) + '.' + str(year) 

		votes.append({'vote_id_generated' : vote_id_generated, 'vote_title' : r.strip(), 'vote_number' : vote_number})
		#print('vote_id_generated: ' + vote_id_generated)
		print(str(year) + r.strip())


	# get senate votes
	resp = urllib.request.urlopen(MAIN_URL+'/how-they-voted-'+str(year)+'-senate')
	html = resp.read()
	soup = BeautifulSoup(html, "lxml")

	raw = soup.get_text()

	records = re.findall(r'\.\s\d+-\d+-S-RC\d+', raw)

	for r in records:
		# process data and add to votes[]
		vote_number = re.search(r'RC\d+',r).group()[2:]
		congress = re.search(r'\d+-[12]-S-RC',r).group()[:-7]
		vote_id_generated = 's' + str(vote_number) + '-' + str(congress) + '.' + str(year) 

		votes.append({'vote_id_generated' : vote_id_generated, 'vote_title' : r.strip(), 'vote_number' : vote_number})
		#print('vote_id_generated: ' + vote_id_generated)
		print(str(year)  + r.strip())

	return votes


def main(argv):
	
	# parse command line input
	usage = "usage: %prog -o <filename> -y <year1,year2,..,yearN>"
	parser = OptionParser(usage=usage)
	
	parser.add_option("-o", action="store", type="string", dest="output_filename", help="set output filename", default = "output.txt")
	parser.add_option("-y", type="string", dest="years") #default action is store

	(options, args) = parser.parse_args(argv)

	if not options.years or not options.output_filename:
		parser.error("Incorrect number of arguments")

	target_years = options.years.split(',')

	# set up python and psql conenction
	try:
		conn = psycopg2.connect("dbname = 'politics'");
	except:
		print ('Unable to set up connection, exiting')
		return

	with open(options.output_filename, "w") as text_file:
		for year in target_years:
			print('\t\t========= Chamber of Commerce Result of year ' + str(year) +' ========= \n', file=text_file)
			print('\n Processing Chamber of Commerce votes of year ' + str(year))
			
			votes = get_votes(year)
			
			for v in votes:
				# query db
				curs = conn.cursor()
				query = "SELECT id, date, subject FROM votes WHERE id = '" + v['vote_id_generated'] + "';"
				curs.execute(query)
				
				for row in curs:
					print(row, file = text_file)
				print('{'+'\n'.join("'%s' : '%s'" % (key, val) for (key,val) in v.items())+'}' + '\n', file = text_file)

	return
	

if __name__ == "__main__":
	main(sys.argv[1:])

print ("\nbye python script\n")
