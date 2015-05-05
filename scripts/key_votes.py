from BeautifulSoup import BeautifulSoup
import urllib2, json, re, string

KEY_BILLS_JSON = 'data/key_bills.json'
KEY_VOTES_JSON = 'data/key_votes.json'
KEY_BILLS_DAT = 'data/key_bills.dat'
KEY_VOTES_DAT = 'data/key_votes.dat'

URLS = ["http://politics.nytimes.com/congress/votes/113/major/house",
	"http://politics.nytimes.com/congress/votes/113/major/senate",
	"http://projects.washingtonpost.com/congress/113/house/1/key-votes",
	"http://projects.washingtonpost.com/congress/113/house/2/key-votes/",
	"http://projects.washingtonpost.com/congress/113/senate/1/key-votes",
	"http://projects.washingtonpost.com/congress/113/senate/2/key-votes/"
	]

'''
IMPORTANT - nytimes returns BILLS, washpost returns VOTES
'''

def nytimes_scraper(soup, chamber, congress):
	elements = soup.findAll('table', 'nytint-feed-items')
	# vote_dates = [str(e.find('td', 'nytint-feed-items-date').find('span').text) for e in elements]
	# print vote_dates
	# vote_names = [str(e.find('h6', 'billHeader').text) for e in elements if e.find('h6', 'billHeader')]
	# print vote_names
	# assert(len(vote_dates) == len(vote_names))

	vote_names, vote_dates = [], []
	for e in elements:
		name = e.find('h6', 'billHeader')
		if name:
			vote_names.append(str(name.text))
			vote_dates.append(str(e.find('td', 'nytint-feed-items-date').find('span').text))

	votes = [nytimes_format(v, congress) for v in vote_names]
	return votes

def nytimes_parse_vote(vote_name):
	'''
	Extract type and number
	Vote is in format 'H.R.3350'
	'''
	vtype = ''.join(ch.lower() for ch in vote_name if ch in string.letters)
	vnumber = re.search('\d+', vote_name).group()
	# return {
	# 	'type': vtype,
	# 	'number': vnumber
	# }
	return vtype, vnumber

def nytimes_format(vote, congress):
	vote_type, vote_number = nytimes_parse_vote(vote) 
	return "{0}{1}-{2}".format(vote_type, vote_number, congress)

def washpost_scraper(soup, chamber, congress):
	"""
	Returns the vote numbers (corresponds to vote_id in the database

	Assumes that vote number is contained in a <span class='lt-gray'> element
	in the format (Vote 123) and that all such elements contain vote numbers
	"""

	elements = soup.findAll('div', 'vote-list')
	vote_numbers = [re.search('\d+', str(e.find('span', 'lt-gray').text)).group() for e in elements]
	vote_dates = [str(e.find('h5').text) for e in elements]
	assert(len(vote_numbers) == len(vote_dates))

	votes = [washpost_format(vote_numbers[i], chamber, congress, vote_dates[i].split(',')[-1].strip()) for i in range(len(vote_numbers))]
	return votes

def washpost_format(vote_num, chamber, congress, year):
	"""
	vote_num is a number denoting the vote number
	
	For example, [Vote] 251 in the 113-th Congress, Session 1 is 
	District of Columbia Pain-Capable Unborn Child Protection Act

	Return in format h251-113.2013
	"""

	return "{0}{1}-{2}.{3}".format(chamber, vote_num, congress, year)

def write_to_json(filename, data):
	'''
	Write output to JSON file
	# ================================================== 
	# Output json file will be in format:
	# {
	#	'house': {
	#		'www.washpost.com': ['vote1', 'vote2', 'vote3'],
	#		'www.nytimes.com': ['vote4', 'vote5'],
	#	}
	#	'senate': {...}
	# }
	# ==================================================
	'''
	with open(filename, 'w') as out:
		json.dump(data, out, check_circular=True, indent=4, encoding='utf-8')

def write_to_dat(filename, data):
	'''
	Values are separated by vertical pipes |
	to be loaded into a Postgres database
	'''
	with open(filename, 'w') as out:
		for chamber in data:
			for url in data[chamber]:
				for item in data[chamber][url]:
					out.write('|'.join([item, url]))
					out.write('\n')

if __name__ == '__main__':
	bills = {
		's': {},
		'h': {} 
	}
	
	votes = {
		's': {},
		'h': {}
	}


	for url in URLS:
		print '***** Getting votes from ' + url

		doc = urllib2.urlopen(url)
		soup = BeautifulSoup(doc)

		assert('house' in url or 'senate' in url)
		chamber = 'h' if 'house' in url else 's'
		congress = re.findall('\d+', url)[0]

		if "nytimes" in url:
			result = nytimes_scraper(soup, chamber, congress)
			# bills
			bills[chamber][url] = result
		elif "washingtonpost" in url:
			result = washpost_scraper(soup, chamber, congress)
			# votes
			votes[chamber][url] = result

	write_to_dat(KEY_BILLS_DAT, bills)
	write_to_dat(KEY_VOTES_DAT, votes)
	# write_to_json(KEY_BILLS_JSON, bills)
	# write_to_json(KEY_VOTES_JSON, votes)
