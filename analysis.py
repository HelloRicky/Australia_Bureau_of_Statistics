"""
use this script to analysis the downloaded data, mainly for 4 and 41 dataset
Analysis includes:
- people distribution
- people density

"""


from os import listdir
import os.path
import shutil
from collections import defaultdict
import json
import csv


## initial
json_path = "./json_files"
json_04 = "4"
json_41 = "41"
file_source_type = '.json'

output_dict = defaultdict()
error_list = []

"""

helper function
"""
def read_json(file_name):
  with open(file_name) as f:
    data = json.load(f)
  return data

def get_all_files(path, file_type = ''):

  return [f for f in listdir(p) for p in path if f.endswith(file_type)]

## format string value by remove all the non digit charaters
def remove_non_digit(data):
  data = data.replace(',', '')
  data = data.replace('$', '')
  return data

def csv_saver(file_name, data):
  with open(file_name, 'wb') as f:
    writer = csv.writer(f)
    for k, v in data.items():
      writer.writerow([k, v])

if __name__ == "__main__":

  target_04 = os.path.join(json_path, json_04)
  target_41 = os.path.join(json_path, json_41)
  target_path = [target_04, target_41]

  for i in get_all_files(target_path, file_type = file_source_type):
    area_code = i.split(file_source_type)[0]
    try:
      data = read_json(json_path + i)
      #print(i, data['GeoInfo']['city'], int(remove_non_digit(data['summaryTable_qsPeople']['People'])))
      
      city = str(data['GeoInfo']['city'])
      people_count = int(remove_non_digit(data['summaryTable_qsPeople']['People']))
      output_dict[city] = people_count
      output_dict[code] = area_code

      
      
    except:
      error_list.append(i)

  ## save result
  csv_saver('people_count.csv', output_dict)

  print('error count:', len(error_list))


