#!/usr/bin/env python

from __future__ import print_function

import json

from pprint import pprint




#
# Read JSON from file
#
def load_file (file_name):

  #
  # Read json into python object
  #
  with open(file_name, 'r') as json_file:    
      json_obj = json.load(json_file)

  return json_obj



#
# Write JSON to file
#

def store_file(file_name, json_obj, preserve=False):

  if preserve:
      file_name = file_name + '.new'

  with open(file_name, 'w') as json_file:  
      json.dump(json_obj, json_file, indent=2)






#
# Main program
#

if __name__ == '__main__':

  #
  # 1. Read data from file
  #  
  json_obj = load_file ('data/json_dict.json') 

  print("\n# ORIG raw python dict object read from file: ")
  pprint(json_obj)

  print("\n# ORIG serialized python object: ")
  print(json.dumps(json_obj))



  #
  # 2. Add new key-val pair { FOO: bar } to dict
  #    remove keys 'maps' and 'masks', and merge 
  #    with another dict
  #

  #
  # 2.1 Add key-val pair { FOO: bar } and 
  #     remove keys 'maps' and 'masks'
  #

  #if isinstance(json_obj, dict):
  if type(json_obj) is dict:

    json_obj[u'FOO'] = "bar"
    
    for key in ['maps', 'masks']:
      if key in json_obj.keys():
        del json_obj[key] 


  #
  # 2.2 Merge another dict
  #
  dic = { u'dic2': u'val2', u'dic2a': 'val2a'}
  json_obj.update(dic)



  #
  # 3. Write updated data to file
  #

  store_file ('data/json_dict.json', json_obj, preserve=True) 

  print("\n# NEW raw python dict object: ")
  pprint(json_obj)

  print("\n# NEW serialized python dict object: ")
  print(json.dumps(json_obj))


