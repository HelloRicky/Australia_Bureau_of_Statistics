"""
use this script to analysis the downloaded data, mainly for 4 and 41 dataset
Analysis includes:
- people distribution
- people density

"""

from __future__ import print_function
from os import listdir
import os.path
import shutil
from collections import defaultdict
import json
import csv


## initial
analysis_path = "./analysis_result"
json_path = "./json_files"
json_04 = "4"
json_41 = "41"
file_source_type = '.json'

output_dict = defaultdict(lambda:defaultdict())
error_list = []

"""

helper function
"""
def read_json(file_name):
  with open(file_name) as f:
    data = json.load(f)
  return data

def get_all_files(path, file_type = ''):

  return [(f, os.path.join(p,f)) for p in path for f in listdir(p) if f.endswith(file_type)]

## format string value by remove all the non digit charaters
def remove_non_digit(data):
  data = data.replace(',', '')
  data = data.replace('$', '')
  return data


def csv_saver(file_name, data):
  with open(file_name, 'wb') as f:
    writer = csv.writer(f)
    fields = data.values()[0].keys()
    writer.writerow(['city'] + fields)
    for k in data.keys():
      writer.writerow([k] + [data[k][field] for field in fields])


if __name__ == "__main__":

  target_04 = os.path.join(json_path, json_04)
  target_41 = os.path.join(json_path, json_41)
  target_path = [target_04, target_41]

  for (f_name, f_full) in get_all_files(target_path, file_type = file_source_type):

    area_code = f_name.split(file_source_type)[0]
    try:
      data = read_json(f_full)
      #print(i, data['GeoInfo']['city'], int(remove_non_digit(data['summaryTable_qsPeople']['People'])))
      
      city = str(data['GeoInfo']['city'])
      people_count = int(remove_non_digit(data['summaryTable_qsPeople']['People']))
      output_dict[city]['lat'] = float(data['GeoInfo']['lat'])
      output_dict[city]['lon'] = float(data['GeoInfo']['lon'])
      output_dict[city]['people'] = people_count
      output_dict[city]['code'] = data['GeoInfo']['SSC']

      
      
    except:
      error_list.append(f_full)

  ## save result
  csv_out = os.path.join(analysis_path, 'people_count.csv')
  csv_saver(csv_out, output_dict)

  print('error count:', len(error_list))


