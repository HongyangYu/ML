# -*- coding: utf-8 -*-
import os
from mongoengine import *

import nltk
nltk.download()
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string
import re

path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir("../data")

class Products(DynamicDocument):
	product_id = StringField()
	product_name = DictField()
	product_description = DictField()
	product_attributes = DictField()

'''
stop_words_file = open('stop-word-list.csv','r+')
for line in stop_words_file:
	stop_words = line.split(", ")

'''
if connect('product_info'):
	print "Database Connected"
else:
	print "Connection cannot be established"



punctuation = list(string.punctuation)
stop_words = stopwords.words('english') + punctuation

stemmer = SnowballStemmer("english")

def remove_non_ascii(text):
	return re.sub(r'[^\x00-\x7F]+',' ', text)

f = open('product_descriptions.csv','r+')
for line in f:
	fields = line.split(",")
	#p = Products.objects.get(product_id = fields[0])
	fields[1] = fields[1].replace(".","")
	fields[1] = fields[1].replace("$","")
	fields[1] = fields[1].replace("\"","")
	fields[1] = fields[1].replace("(","")
	fields[1] = fields[1].replace(")","")
	fields[1] = fields[1].replace("#","")
	fields[1] = fields[1].lower().strip()
	fields[1] = remove_non_ascii(fields[1])
	words = [i for i in fields[1].split() if i not in stop_words]
	#print "---------------------"
	#print words
	#print "---------------------"
	temp_dict = {}
	for word in words:
		if not isinstance(word, unicode):
			word = stemmer.stem(word)
		if word in  temp_dict:
			count = temp_dict[word]
			temp_dict.update({word : count + 1})
		else:
			temp_dict.update({word : 1})
	#print temp_dict
	p = Products(product_id = fields[0],product_name = {},product_description = temp_dict, product_attributes = {})
	p.save()
	
	
f =  open('train.csv','r+')


for line in f:
	fields = line.split(",")
	try:
		p = Products.objects.get(product_id = fields[1])
		print fields[1]
		if p:
			fields[2] = fields[2].replace(".","")
			fields[2] = fields[2].replace("$","")
			fields[2] = fields[2].replace("\"","")
			fields[2] = fields[2].replace("(","")
			fields[2] = fields[2].replace(")","")
			fields[2] = fields[2].replace("[","")
			fields[2] = fields[2].replace("]","")
			fields[2] = fields[2].replace("'","")
			fields[2] = fields[2].replace("#","")
			fields[2] = fields[2].replace("\\","-")
			fields[2] = fields[2].lower().strip()
			fields[2] = remove_non_ascii(fields[2])
			words = [i for i in fields[2].split() if str(i) not in stop_words]
			#print "---------------------"
			#print words
			#print "---------------------"
			temp_dict = {}
			print words
			for word in words:
				if not isinstance(word, unicode):
					word = stemmer.stem(word)
				if word in  temp_dict:
					count = temp_dict[word]
					temp_dict.update({word : count + 1})
				else:
					temp_dict.update({word : 1})
			print temp_dict
			pi = p.product_id
			pd = p.product_description
			p.delete()
			p = Products(product_id = pi,product_name = temp_dict,product_description = pd, product_attributes = {})
			p.save()
		
	except Exception, e:
        	print e
		fields[2] = fields[2].replace(".","")
		fields[2] = fields[2].replace("$","")
		fields[2] = fields[2].replace("\"","")
		fields[2] = fields[2].replace("(","")
		fields[2] = fields[2].replace(")","")
		fields[2] = fields[2].replace("[","")
		fields[2] = fields[2].replace("]","")
		fields[2] = fields[2].replace("'","")
		fields[2] = fields[2].replace("#","")
		fields[2] = fields[2].replace("\\","-")
		fields[2] = fields[2].lower().strip()
		fields[2] = remove_non_ascii(fields[2])
		words = [i for i in fields[2].split() if str(i) not in stop_words]
			#print "---------------------"
			#print words
			#print "---------------------"
		temp_dict = {}
		print words
		for word in words:
			if not isinstance(word, unicode):
				word = stemmer.stem(word)
			if word in  temp_dict:
				count = temp_dict[word]
				temp_dict.update({word : count + 1})
			else:
				temp_dict.update({word : 1})
		print temp_dict
		p = Products(product_id = fields[1],product_name = temp_dict,product_description = {} , product_attributes = {})
		p.save()	






f = open('attributes.csv','r+')
for line in f:
	fields = line.split(",")
	try:
		p = Products.objects.get(product_id = fields[0])
		print fields[0]
		if p:
			fields[1] = fields[1].replace("\"","")
			attr_terms = fields[1].split()
			if(len(attr_terms)>0):
				f_term = attr_terms[0]
				print f_term
				if f_term.startswith(('Bullet','bullet')):
					fields[2] = fields[2].replace(".","")
					fields[2] = fields[2].replace("$","")
					fields[2] = fields[2].replace("\"","")
					fields[2] = fields[2].replace("\'","")
					fields[2] = fields[2].replace("(","")
					fields[2] = fields[2].replace(":","")
					fields[2] = fields[2].replace(")","")
					fields[2] = fields[2].replace("#","")
					fields[2] = fields[2].replace("\\","-")
					fields[2] = fields[2].lower().strip()
					fields[2] = remove_non_ascii(fields[2])
					words = [i for i in fields[2].split() if i not in stop_words]
				
					temp_dict = p.product_attributes
					for word in words:
				
						if not isinstance(word, unicode):
							word = stemmer.stem(word)
						if word in  temp_dict:
							count = temp_dict[word]
							temp_dict.update({word : count + 1})
						else:
							temp_dict.update({word : 1})
					print temp_dict
					pi = p.product_id
					pn = p.product_name
					pd = p.product_description
					p.delete()
					p = Products(product_id = pi,product_name = pn,product_description = pd, product_attributes = temp_dict)
					p.save()
		
	except Exception, e:
        	print e
		fields[1] = fields[1].replace("\"","")
		attr_terms = fields[1].split()
		if(len(attr_terms)>0):
			f_term = attr_terms[0]
			print f_term
			if f_term.startswith(('Bullet','bullet')):
				fields[2] = fields[2].replace(".","")
				fields[2] = fields[2].replace("$","")
				fields[2] = fields[2].replace("\"","")
				fields[2] = fields[2].replace("\'","")
				fields[2] = fields[2].replace("(","")
				fields[2] = fields[2].replace(":","")
				fields[2] = fields[2].replace(")","")
				fields[2] = fields[2].replace("#","")
				fields[2] = fields[2].replace("\\","-")
				fields[2] = fields[2].lower().strip()
				fields[2] = remove_non_ascii(fields[2])
				words = [i for i in fields[2].split() if i not in stop_words]
			
				temp_dict = p.product_attributes
				for word in words:
					if not isinstance(word, unicode):
						word = stemmer.stem(word)
					if word in  temp_dict:
						count = temp_dict[word]
						temp_dict.update({word : count + 1})
					else:
						temp_dict.update({word : 1})
				print temp_dict
				p = Products(product_id = fields[0],product_name = {},product_description = {} , product_attributes = temp_dict)
				p.save()

