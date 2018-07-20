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
analysis_path="./analysis_result"
json_root = "./json_files"
json_dirs = ['41']
file_type = '.json'



error_list = []

"""
helper function
"""
def read_json(file_name):
  with open(file_name) as f:
    data = json.load(f)
  return data

def get_all_files(path, file_type = ''):

  return [os.path.join(p,f) for p in path for f in listdir(p) if f.endswith(file_type)]

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

def people_count(data, _dict):
  
  city = str(data['GeoInfo']['city'])
  people_count = int(remove_non_digit(data['summaryTable_qsPeople']['People']))
  _dict[city]['lat'] = float(data['GeoInfo']['lat'])
  _dict[city]['lon'] = float(data['GeoInfo']['lon'])
  _dict[city]['people'] = people_count
  _dict[city]['code'] = data['GeoInfo']['SSC']
  return _dict

def ancestry_count(data, _dict):
  
  city = str(data['GeoInfo']['city'])
  ancestry = data['Ancestry, top responses']
  max_k = None
  max_v = 0
  for k, v in ancestry.items():
    val = int(remove_non_digit(v[city]))
    if val > max_v:
      max_v = val
      max_k = k
  
  _dict[city]['lat'] = float(data['GeoInfo']['lat'])
  _dict[city]['lon'] = float(data['GeoInfo']['lon'])
  _dict[city]['top_ancestry'] = max_k
  _dict[city]['ancestry_num'] = max_v
  _dict[city]['code'] = data['GeoInfo']['SSC']
  return _dict


if __name__ == "__main__":

  output_dict = defaultdict(lambda:defaultdict())

  file_paths = [os.path.join(json_root, d) for d in json_dirs]

  for f in get_all_files(file_paths, file_type = file_type):

    try:
      data = read_json(f)
      
      #output_dict = people_count(data, output_dict)
      output_dict = ancestry_count(data, output_dict)
      
    except:
      error_list.append(f)

  ## save result
  
  #csv_out = os.path.join(analysis_path, 'people_count.csv')
  csv_out = os.path.join(analysis_path, 'ancestry_count.csv')

  csv_saver(csv_out, output_dict)
  print("Completed!")
  if error_list: print('error count:', len(error_list))


