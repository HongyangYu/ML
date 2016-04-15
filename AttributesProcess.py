# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 13:33:28 2016
@author: Hongyang
"""

import json
class Attributes:
    def getAttributesList(self, filename, dic):
        _file = file(filename, 'r') 
        for line in _file:
            if line == "\n":
                continue
            words = line.split(",")
            words[1] = words[1].strip('"')
            words[2] = words[2].strip('"\n')
            if words[1] in dic:
                dic[words[1]].append((words[0],words[2]))
            else:
                product_list = [(words[0],words[2])]
                dic[words[1]] = product_list
        return dic  
        

print("Start")      
attr = Attributes()
dic = {} # name: (product_id,value)
dic = attr.getAttributesList("attributes.csv", dic)

with open('data.json', 'w') as fp:
    json.dump(dic, fp)
print("END")

