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
json_path = './'

## parse all content
def parse_html(html):
	html_file = html_path + html
	json_file = json_path + html.split('.')[0] + '.json'
	_dict = defaultdict(lambda: defaultdict())
	with open(html_file, 'r') as f:
		soup = BeautifulSoup(f)

	location = (soup.find("h2", class_= "geo").contents)[0]
	_dict['location'] = location
	tables = soup.findAll("table")


	for table in tables:
		_dict = parse_table(table, _dict)

	write_json(json_file, _dict)
	return tables


## helper functions
## =========================================================================
def write_json(file_name, data):
	with open(file_name,  "w") as f:
		json.dump(data, f)
	return

def read_json(file_name):
	with open(file_name, "r") as f:
		data = json.loads(f)
	return data

def get_nest_content(data):
	## get the deepest level of content, e.g. <strong>--</strong>

	while 'contents' in dir(data):
		data = data.contents[0] if data.contents else None
	return data

## process individual table
def parse_table(table, _dict):

	trs = table.findAll('tr')
	sub_dict = defaultdict()
	key = None

	try:
		## summary table
		## =========================================================================
		classes = table.attrs["class"]
		key = "_".join(classes)

		for tr in trs:
			## reset value in case there is a empty value
			th = None
			td = None
			try:
				th = str(tr.find('th').contents[0])
				td = str(tr.find('td').contents[0])
			except:
				pass
			sub_dict[th] = td
	except:
		## process other tables that don't contain class
		## =========================================================================

		### headers
		
		columns = []
		headers = trs[0].findAll('th')
		key = str(headers[0].find('a').contents[0])

		for i in headers[1:]:
			val = str(i.contents[0])
			# make meaningful of the column for %
			if val == "%":
				val = columns[-1] + "_" + val
			columns.append(val)


		### contents
		#-------------------
		for tr in trs[1:]:
			td = None
			th = None
			

			td_list = tr.findAll('td')
			try:
				th = str(tr.find('th').contents[0])
				td_vals = [str(get_nest_content(i)) for i in td_list]
				td_dict = dict(zip(columns, td_vals))
				sub_dict[th] = td_dict
			except:
				pass
			
			
			


	# return result of current table
	if key: _dict[key] = sub_dict
	return _dict

	


## get the full list of target html files
def get_all_html_files(path):
	return [f for f in listdir(path) if f.endswith(".html")]

if __name__ == "__main__":
	files = get_all_html_files(html_path)
	for i in files[1:]:
		print("="*20)
		result = parse_html(i)
		print(len(result))