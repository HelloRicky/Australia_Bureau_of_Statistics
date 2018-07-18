from os import listdir
import json


json_path = "./test/"

def read_json(file_name):
  with open(file_name) as f:
    data = json.load(f)
  return data

def get_all_files(path, file_type = ''):
  return [f for f in listdir(path) if f.endswith(file_type)]

for i in get_all_files(json_path, file_type = '.json'):
  data = read_json(json_path + i)
  print(i, data['GeoInfo']['city'], int(data['summaryTable_qsPeople']['People']))