"""
Extracting the list of members of Congress who have appeared most often on Sunday news shows
and dump to the database on a weekly basis. 
	@Author Charles Xu		Octorber 6, 2015
Schema: 
	persons(id, id_govtrack, id_lis, first_name, middle_name, last_name, birthday, gender)

>> ISSUE <<
unable to retrieve data in 2011 and 2012

"""


from pyvirtualdisplay import Display
from selenium import webdriver
import psycopg2

NICKNAME_DICT = {'Charlie': 'Charles',}
STATE_ABBR= {'Alabama' : 'AL',
		'Alaska' : 'AK',
		'Arizona' : 'AZ',
		'Arkansas' : 'AR',
		'California' : 'CA',
		'Colorado' : 'CO',
		'Connecticut' : 'CT',
		'Delaware' : 'DE',
		'Florida' : 'FL',
		'Georgia' : 'GA',
		'Hawaii' : 'HI',
		'Idaho' : 'ID',
		'Illinois' : 'IL',
		'Indiana' : 'IN',
		'Iowa' : 'IA',
		'Kansas' : 'KS',
		'Kentucky' : 'KY',
		'Louisiana' : 'LA',
		'Maine' : 'ME',
		'Maryland' : 'MD',
		'Massachusetts' : 'MA',
		'Michigan' : 'MI',
		'Minnesota' : 'MN',
		'Mississippi' : 'MS',
		'Missouri' : 'MO',
		'Montana' : 'MT',
		'Nebraska' : 'NE',
		'Nevada' : 'NV',
		'New Hampshire' : 'NH',
		'New Jersey' : 'NJ',
		'New Mexico' : 'NM',
		'New York' : 'NY',
		'North Carolina' : 'NC',
		'North Dakota' : 'ND',
		'Ohio' : 'OH',
		'Oklahoma' : 'OK',
		'Oregon' : 'OR',
		'Pennsylvania' : 'PA',
		'Rhode Island' : 'RI',
		'South Carolina' : 'SC',
		'South Dakota' : 'SD',
		'Tennessee' : 'TN',
		'Texas' : 'TX',
		'Utah' : 'UT',
		'Vermont' : 'VT',
		'Virginia' : 'VA',
		'Washington' : 'WA',
		'West Virginia' : 'WV',
		'Wisconsin' : 'WI',
		'Wyoming' : 'WY',
		'Md' : 'MD',
		'Ga' : 'GA', }

# Connect to Database
conn_string = "dbname='politics'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
# Create new table to store the frequency of coverage of each person
cursor.execute("CREATE TABLE media_coverage(id character(10) NOT NULL, freq integer NOT NULL, year integer NOT NULL)")


display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()
driver.get('http://media.cq.com/facetime/')

table = driver.find_element_by_id('tabularData2013Sub')
for element in driver.find_element_by_class_name("btnGroupToggle").find_elements_by_tag_name('a'):
	# Data collecting
	element.click()
	year = element.text
	if year == '2011' or year == '2012':  continue; 
	for e in table.find_elements_by_xpath("./div"):
		year = e.get_attribute("data-year")
		name_preprocessed = e.find_element_by_class_name("col1").text
		if(not name_preprocessed): continue
		count = e.find_element_by_class_name("col2")
		if(count is not None): count = count.text
		else: continue
		name_arr = name_preprocessed.split(' ')
		first_name = name_arr[1]
		if(first_name in NICKNAME_DICT.keys()): 
			first_name = NICKNAME_DICT[first_name]
		last_name = name_arr[len(name_arr)-2]
		last_name = last_name[0:len(last_name)-1]
		ind = last_name.find('\'')
		if(ind != -1): 
			print('>>>OOPS:'+last_name)
			continue
		print(year + " " + first_name + " " + last_name + " " + count)
		# Write to DB
		cursor.execute("SELECT id FROM persons WHERE first_name = '" + first_name + "'" + "AND last_name = '"+ last_name +"'")
		records = cursor.fetchall()
		if(len(records) == 0): continue
		id_final = records[0][0]
		if(len(records) > 1): #possible duplicates
			abbr = None
			state = name_arr[-1]
			state = state[2:-1]
			for k in STATE_ABBR.keys():
				if(state in k): 
					abbr = STATE_ABBR[k]
					break
			if(abbr is None): print('>>>OPPS: NOT IN DICT'); continue
			for r in records:
				id_tmp = r[0]
				cursor.execute("SELECT person_id FROM person_roles WHERE person_id = '" + id_tmp + "'" + "AND state = '"+ abbr +"'")
				result = cursor.fetchall()
				if(len(result) == 1): 
					id_final = result[0][0]
					break
		cursor.execute("INSERT INTO media_coverage(id, freq, year) VALUES ('"+id_final+"','"+count+"','"+year+"')")

conn.commit()
conn.close()
driver.close()
display.stop()
