from os import listdir
import shutil
from collections import defaultdict
import json


json_path = "./json_files/41/"

def read_json(file_name):
  with open(file_name) as f:
    data = json.load(f)
  return data

def get_all_files(path, file_type = ''):
  return [f for f in listdir(path) if f.endswith(file_type)]

"""
helper function
remove all the non digit charaters
"""
def remove_non_digit(data):
  data = data.replace(',', '')
  data = data.replace('$', '')
  return data

result = defaultdict()
error_list = []

for i in get_all_files(json_path, file_type = '.json'):
  try:
    data = read_json(json_path + i)
    #print(i, data['GeoInfo']['city'], int(remove_non_digit(data['summaryTable_qsPeople']['People'])))
    
    city = str(data['GeoInfo']['city'])
    people_count = int(remove_non_digit(data['summaryTable_qsPeople']['People']))
    result[city] = people_count
    
  except:
    error_list.append(i)


print(len(error_list))

