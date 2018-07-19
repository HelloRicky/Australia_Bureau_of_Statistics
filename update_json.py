from __future__ import print_function
from os import listdir
import os.path
import shutil
from collections import defaultdict
import json
import csv

json_path = "./json_files"
json_04 = "4"
json_41 = "41"
file_source_type = '.json'



def read_csv():
	reader = csv.DictReader(open('lat_lon_au.csv', 'rb'))
	dict_list = []
	for line in reader:
		dict_list.append(line)
	return dict_list

def read_json(file_name):
  with open(file_name) as f:
        data = json.load(f)
  return data

## save data into json files
def write_json(file_name, data, overwrite = True):
	## is file already exist, don't overwrite
	if not overwrite and os.path.isfile(file_name): return
	with open(file_name,  "w") as f:
		json.dump(data, f)
	return

def get_all_files(path, file_type = ''):

  return [(f, os.path.join(p,f)) for p in path for f in listdir(p) if f.endswith(file_type)]





if __name__ == "__main__":
	csv_data = read_csv()
	non_list = []
	error_list= []

	target_04 = os.path.join(json_path, json_04)
	target_41 = os.path.join(json_path, json_41)
	target_path = [target_04, target_41]

	for (f_name, f_full) in get_all_files(target_path, file_type = file_source_type):
		flag = False
		area_code = f_name.split(file_source_type)[0]

		try:
			data = read_json(f_full)
		  #print(i, data['GeoInfo']['city'], int(remove_non_digit(data['summaryTable_qsPeople']['People'])))
		  
			city = str(data['GeoInfo']['city'])
			
			for i in csv_data:
				if city.upper() in i['suburb']:
					data['GeoInfo']['lat'] = i['lat']
					data['GeoInfo']['lon'] = i['lon']
					data['GeoInfo']['SSC'] = area_code
					flag = True
        
			if not flag:
				non_list.append(area_code)

			## WRITE TO JSON
			write_json(f_full, data)

		except:
		  error_list.append(f_full)				

  ## save result
	print('error count:', len(error_list))
	print('non_list count:', len(non_list))




	
