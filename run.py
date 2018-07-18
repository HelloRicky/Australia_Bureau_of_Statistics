"""
Author: Ricky Zheng

Use this script to fetch all tables from the html and store into json files
The html files were scrapped from the Australia Bureau of Statistics, 2016 data set, sample link below:
	http://quickstats.censusdata.abs.gov.au/census_services/getproduct/census/2016/communityprofile/SSC10790?opendocument
	data covered from SSC10001 to SSC14524
"""

from __future__ import print_function
from collections import defaultdict
from bs4 import BeautifulSoup
import json
import time
from os import listdir

## initial

html_path = "./html_files/"
json_path = './json_files/'



"""
## helper functions
=========================================================================
"""

## get the full list of target html files
def get_all_html_files(path):
	return [f for f in listdir(path) if f.endswith(".html")]

## save data into json files
def write_json(file_name, data):
	with open(file_name,  "w") as f:
		json.dump(data, f)
	return

## read json files
def read_json(file_name):
	with open(file_name, "r") as f:
		data = json.loads(f)
	return data

## get the deepest level of content, e.g. <strong>--</strong>
def get_nest_content(data):
	if not data: return None


	try:

		## data might contain UnicodeEncodeError
		while 'contents' in dir(data):
			data = data.contents[0] if data.contents else None
		return str(data)
	except:

		return None
	

"""
## process individual table
=========================================================================
"""

def parse_table(table, _dict):

	trs = table.findAll('tr')
	sub_dict = defaultdict()
	key = None

	table_attrs = table.attrs

	if 'class' in table_attrs:
		## summary table, contains class attributes
		## =========================================================================
		key = "_".join(table_attrs["class"])

		for tr in trs:
			## reset value in case there is a empty value
			th = get_nest_content(tr.find('th'))
			td = get_nest_content(tr.find('td'))
			sub_dict[th] = td
	else:
		## process other tables that don't contain class
		## =========================================================================

		### headers
		#-------------------		
		columns = []
		headers = trs[0].findAll('th')
		key = get_nest_content(headers[0].find('a'))

		for i in headers[1:]:
			val = get_nest_content(i)
			# make meaningful of the column for %
			if val == "%":
				val = columns[-1] + "_" + val
			columns.append(val)


		### contents
		#-------------------
		for tr in trs[1:]:
			td_list = tr.findAll('td')
			
			th = get_nest_content(tr.find('th'))
			td_vals = [get_nest_content(i) for i in td_list]
			td_dict = dict(zip(columns, td_vals))
			sub_dict[th] = td_dict


	# return result of current table
	if key: _dict[key] = sub_dict
	return _dict




""" 
main function
=========================================================================
read html content, parse all tables and save to json
"""
def parse_html(html):
	html_file = html_path + html
	json_file = json_path + html.split('.')[0] + '.json'
	_dict = defaultdict(lambda: defaultdict())

	## read html files
	with open(html_file, 'r') as f:
		soup = BeautifulSoup(f)

	## parse tables
	tables = soup.findAll("table")
	for table in tables:
		_dict = parse_table(table, _dict)

	## addtional information
	location = (soup.find("h2", class_= "geo").contents)[0]
	_dict['GeoInfo'] = {'city': location}

	## save to json files
	write_json(json_file, _dict)

	return tables



if __name__ == "__main__":
	files = get_all_html_files(html_path)
	for i in files:
		print("="*20)
		print('processing:', i, end = '...')
		result = parse_html(i)
		print(len(result), 'tables detected')
