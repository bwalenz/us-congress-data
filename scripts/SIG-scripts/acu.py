# acu.py
# script that scape the acu votes on "http://acuratings.conservative.org/acu-federal-legislative-ratings/"
# last time validated: Oct 16, 2015
# Owner: Yubo Tian

from bs4 import BeautifulSoup
import urllib.request
import psycopg2
import re
from optparse import OptionParser
import sys

BASE_URL = "http://acuratings.conservative.org/Vote-Description/"
ERR = -1;

# function that takes in a vote_url, return the formatted vote info
def process_vote(vote_url):
	# variables correlate to this curr vote are named v_variable

	v_resp = urllib.request.urlopen(vote_url)
	v_html = v_resp.read()
	v_soup = BeautifulSoup(v_html, "lxml")

	v_title = v_soup.findAll('h1')[1].text.strip()


	if (len(v_title) <= 1):
		return ERR;

	v_t = v_title.lower().find('roll call');
	if (v_t == -1):
		return ERR;

	vote_number = int(re.search(r'\d+', v_title[v_t:]).group())

	v_description = v_soup.find('h3').text.strip()
	
	v_d = re.search(r'\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\S)*(\W)*\d*(\W)*\d\d\d\d', v_description)
	v_date = date_convert(v_d.group())
	print(v_date + '\t' + v_title)

	return {'vote_date' : v_date, 'vote_number' : vote_number, 'vote_description' : v_description, 'vote_title' : v_title};

def date_convert(date_str):

	day_i = int(re.search(r'\d+', date_str).group());
	if day_i < 10:
		day = '0'+str(day_i)
	else:
		day = str(day_i)

	month = month_convert(date_str[1:4]);
	
	year = date_str[-4:];

	return '-'.join((year,month,day))


def month_convert(month):
	return {
	'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'aug':'08', 'sep':'09', 'oct':'10', 'nov':'11', 'dec':'12',
	}[month.lower()]

def main(argv):
	
	# parse command line input
	usage = "usage: %prog -o <filename> -y <year1,year2,yearN>"
	parser = OptionParser(usage=usage)
	
	parser.add_option("-o", action="store", type="string", dest="output_filename", help="set output filename")
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
			print('\t\t========= ACU Result of year ' + str(year) +' ========= \n', file=text_file)
			print ("\nProcessing ACU votes of year " + str(year) + '......')

			year_url = BASE_URL + "?year1=" + str(year) 
			
			index = 1

			# increment from 1 until vote url is empty
			# alternatively, for each year, go to the url to grab the total # of votes

			while True:
				curr_vote_url = year_url + "&chamber=12&issue=" + str(index) + "&s="


				vote_info = process_vote(curr_vote_url);

				if (vote_info == ERR):
					break

				# use vote_number, vote_date in vote_info to query db, output to file
				curs = conn.cursor()
				query = "SELECT id, date, subject FROM votes WHERE number = " + str(vote_info['vote_number']) + " AND date = '" + vote_info['vote_date']+ "';"
				curs.execute(query)
				for row in curs:
					print(row, file=text_file)
					#print(row)

				#print ("Vote # = " + str(index))	
				#print('{'+'\n'.join("'%s' : '%s'" % (key, val) for (key,val) in vote_info.items())+'}')
				print('{'+'\n'.join("'%s' : '%s'" % (key, val) for (key,val) in vote_info.items())+'}' +'\n', file=text_file)

				index = index + 1


if __name__ == "__main__":
	main(sys.argv[1:])

print ("\nbye python script\n")