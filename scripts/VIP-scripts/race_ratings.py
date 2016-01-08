"""
Extracting the race rating of both the Senate and House, which is 
	a spectrum that analyzes the vulnerability (the chances of the 
	seat switching parties) of the Senate/House races up this cycle
@Author Charles Xu		Octorber 21, 2015

"""

from pyvirtualdisplay import Display
from selenium import webdriver
import psycopg2
import pprint


# Connect to Database
conn_string = "dbname='politics'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
# Create new table to store the frequency of coverage of each person
cursor.execute("CREATE TABLE senate_race_ratings_2016(id CHARACTER(10) NOT NULL, dem_rep CHARACTER(3), vulnerability VARCHAR(10) NOT NULL)")


## Initialize display and webdriver to load the web page
display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()


## 2016 SENATE RACE RATINGS
driver.get('http://cookpolitical.com/senate/charts/race-ratings')
expanded_ratings = driver.find_element_by_id('expanded_ratings')
parties =  expanded_ratings.find_elements_by_tag_name('h3')
tables = expanded_ratings.find_elements_by_tag_name('table')
for i in range(0, len(parties)):
	if parties[i].text.split(' ')[0] == 'Democrats': 
		dem_rep = 'Dem'
	else: dem_rep = 'Rep'
	print(i)
	for person in tables[i].find_elements_by_xpath("./tbody/tr[@class='data']/td"):
		vul = None
		for col in tables[i].find_elements_by_xpath("./tbody/tr/th"):
			if(col.get_attribute("class") == person.get_attribute("class")):
				vul = col.text
				break
		for name in person.find_elements_by_tag_name('a'):
			n = name.text.split(' ')
			last_name = n[0]
			state = n[1][1:-1]
			if len(last_name) == 2: 
				last_name = n[1][1:-1] # to address CA (Boxer) etc
				state = n[0]
			cursor.execute("SELECT id FROM persons WHERE last_name = '"+ last_name +"'")
			records = cursor.fetchall()
			id_final = records[0][0]
			if(len(records) > 1): 
				for r in records:
					id_tmp = r[0]
					cursor.execute("SELECT person_id FROM person_roles WHERE person_id = '" + id_tmp + "'" + "AND state = '"+ state +"'")
					result = cursor.fetchall()
					if(len(result) == 1): 
						id_final = result[0][0]
						break
			cursor.execute("INSERT INTO senate_race_ratings_2016 VALUES ('"+records[0][0]+"','"+dem_rep+"','"+vul+"')")


## 2016 HOUSE RACE RATINGS
driver.get('http://cookpolitical.com/house/charts/race-ratings')
cursor.execute("CREATE TABLE house_race_ratings_2016(id CHARACTER(10) NOT NULL, leaning VARCHAR(20) NOT NULL)")
table = driver.find_element_by_xpath(".//div[@class='races']/div/table/tbody")
middle1Visited = False;
for category in table.find_elements_by_xpath("./tr[@class='head']/th[not(@class='vertical-border')]"):
	cat = category.text
	for people in table.find_elements_by_xpath("./tr[not(@class)]/td[@data-rating]"):
		if(category.get_attribute("class") in people.get_attribute("class")):
			# Probabaly needs to be refactored
			# It is ugly because the header of "Democratic Toss Up" and "Republican Toss Up" has 
			# the same css class "toss-up", so it is hard from person to refer back to header 
			if(middle1Visited and ("middle-1" in people.get_attribute("class"))):
				continue
			for person in people.find_elements_by_xpath("./div[@class='races']/p"):
				person_info = person.text.split(' ')
				last_name = person_info[1]
				print(last_name)
				if(last_name == 'OPEN'): continue
				state = person_info[0][0:2]
				cursor.execute("SELECT id FROM persons WHERE last_name = '"+ last_name +"'")
				records = cursor.fetchall()
				id_final = records[0][0]
				if(len(records) > 1): 
					for r in records:
						id_tmp = r[0]
						cursor.execute("SELECT person_id FROM person_roles WHERE person_id = '" + id_tmp + "'" + "AND state = '"+ state +"'")
						result = cursor.fetchall()
						if(len(result) == 1): 
							id_final = result[0][0]
							break
				cursor.execute("INSERT INTO house_race_ratings_2016(id, leaning) VALUES ('"+id_final+"','"+cat+"')")
			if((not middle1Visited) and ("middle-1" in people.get_attribute("class"))):
				middle1Visited = True
				break
			if(middle1Visited and ("middle-2" in people.get_attribute("class"))): 
				break	
## Wraps up
conn.commit()
conn.close()
driver.close()
display.stop()
