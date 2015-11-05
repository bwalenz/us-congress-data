# scrape_aflcio.py
# script that scape the aflcio voter guide on "http://www.aflcio.org" from 2009 until last time validated
# last time validated: Oct 15, 2015
# Owner: Yubo Tian

from bs4 import BeautifulSoup
import urllib.request
import psycopg2
import re
from optparse import OptionParser
import sys

BASE_URL = "http://www.aflcio.org"

# function that returns the date and number of a vote, which can be used to identify the vote.id in politics.votes
# input: page url of the aflcio key vote
def get_vote_info(vote_url):
	resp = urllib.request.urlopen(vote_url)
	html = resp.read()
	soup = BeautifulSoup(html, "lxml")

	# Get votes.date
	try: 
		dates = soup.find_all('span', {'class':'votingrecords_keyvotes_date'})
	except AttributeError as e:
		print ('No votingrecords_keyvotes_date found, exiting')
		return 

	date = date_convert(dates[0].text.strip());

	# Get description paragraph, which contains votes.number
	try:
		paragraphs = soup.find_all('p')
		#print ("# of Ps found = %d" % len(paragraphs))
	except AttributeError as e:
		print ('No tables found, exiting')
		return
	
	i = 0;

	# remove empty paragraphs
	for p in paragraphs:
		#print("\n" + " p index : " + str(i) + "\n" + "length : "  + str(len(p.text)) + "\n"+ p.text+ "\n")
		#i = i + 1
		if (len(p.text) <= 1):
			paragraphs.remove(p)


	# pull description from paragraphs, index 1 is an empirical result
	description = paragraphs[1].text;
	
	# get the number after roll call vote

	index = description.lower().find('roll call');

	if (index == -1):
		return {'vote_date' : date, 'vote_description' : description, 'vote_number' : -1}

	vote_number = int(re.search(r'\d+', description[index:]).group())

	return {'vote_date' : date, 'vote_description' : description, 'vote_number' : vote_number};

# function that retrieves the url to each key vote in the given year
def go(year):
	year_url = "http://www.aflcio.org/Legislation-and-Politics/Legislative-Voting-Records?termyear=" + str(year) + "&act=3&location=Senate&memberid="
	resp = urllib.request.urlopen(year_url)
	html = resp.read()
	soup = BeautifulSoup(html, "lxml")

	# get all link to each key votes, call get_date_number() on each of them
	try:
		keyvotes = soup.find('ol')

	except AttributeError as e:
		print ('No tables found, exiting')
		return

	key_votes = [];

	# for each key vote link, call get_date_number
	for li in keyvotes.findAll('li'):
		title = li.text.strip();
		print(str(year) +'\t'+ title);

		vote_url = BASE_URL + li.a['href'];

		vote_info = get_vote_info(vote_url);
		vote_info['vote_title'] = title;
		key_votes.append(vote_info);

	return key_votes;


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

	# option 1: 
	# create a new file for each targer year
	# filename = "out_"+str(year) + ".txt"

	#option 2: dump all data into a single output file	
	with open(options.output_filename, "w") as text_file:
		for year in target_years:
			print ("\nProcessing AFL-CIO votes of year " + str(year) + '......')

			# for each target year, scrape the web page and return a list of the information of thats years key votes
			key_votes_list = go(year);
			print('\t\t========= AFL-CIO Result of year ' + str(year) +' ========= \n', file=text_file)

			for vote in key_votes_list:
				# for each vote in key_votes_list
				curs = conn.cursor()
				query = "SELECT id, date, subject FROM votes WHERE number = " + str(vote['vote_number']) + " AND date = '" + vote['vote_date']+ "';"
				curs.execute(query)
				for row in curs:
					print(row, file=text_file)
				print('{'+'\n'.join("'%s' : '%s'" % (key, val) for (key,val) in vote.items())+'}' + '\n' , file=text_file)
			print('\n',file=text_file)

def date_convert(date_str):
	day_i = int(re.search(r'\d+', date_str[10:12]).group());
	if day_i < 10:
		day = '0'+str(day_i)
	else:
		day = str(day_i)
	month = month_convert(date_str[6:9]);
	year = date_str[-4:];

	return '-'.join((year,month,day))
	
def month_convert(month):
	return {
	'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'aug':'08', 'sep':'09', 'oct':'10', 'nov':'11', 'dec':'12',
	}[month.lower()]


if __name__ == "__main__":
	main(sys.argv[1:])

print ("\nbye python script\n")