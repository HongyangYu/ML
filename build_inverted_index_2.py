# -*- coding: utf-8 -*-
import os
from mongoengine import *

import nltk
nltk.download()
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string
import re

import math
import csv

path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir("../data")



class Products(DynamicDocument):
	product_id = StringField()
	product_name = DictField()
	product_description = DictField()
	product_attributes = DictField()

if connect('product_info'):
	print "Database Connected"
else:
	print "Connection cannot be established"

punctuation = list(string.punctuation)
stop_words = stopwords.words('english') + punctuation

stemmer = SnowballStemmer("english")

p_n_inverted_index = {}
p_d_inverted_index = {}
p_a_inverted_index = {}

p_n_total_length = 0L
p_d_total_length = 0L
p_a_total_length = 0L


try:
	for p_id in range(100001,224429):
		p = Products.objects.get(product_id = str(p_id))
		p_n_total_length = p_n_total_length + len(p.product_name)
		p_d_total_length = p_d_total_length + len(p.product_description)
		p_a_total_length = p_a_total_length + len(p.product_attributes)
	
		for word in p.product_name:
			#print word+" "+str(p.product_name[word])
			if word in p_n_inverted_index:
		        	p_n_inverted_index[str(word)][str(p_id)]= p.product_name[word]
		    	else:
	  			p_n_inverted_index[str(word)] = {str(p_id):p.product_name[word]}
		
		for word in p.product_description:
			#print word+" "+str(p.product_name[word])
			if word in p_d_inverted_index:
		        	p_d_inverted_index[str(word)][str(p_id)]= p.product_description[word]
		    	else:
	  			p_d_inverted_index[str(word)] = {str(p_id):p.product_description[word]}

		for word in p.product_attributes:
			#print word+" "+str(p.product_name[word])
			if word in p_a_inverted_index:
		        	p_a_inverted_index[str(word)][str(p_id)]= p.product_attributes[word]
		    	else:
	  			p_a_inverted_index[str(word)] = {str(p_id):p.product_attributes[word]}

except Exception, e:
	print e
	print "Ignore exception"

#print inverted_index

def remove_non_ascii(text):
	return re.sub(r'[^\x00-\x7F]+',' ', text)

def calculate_tf_idf(inverted_index,words,p_id):
	tf_idf_score = 0
	for word in words:
		if word in inverted_index.keys():
			idf = 1/float(len(inverted_index[word]))
			if p_id in inverted_index[word].keys():
				tf = 1 + math.log(inverted_index[word][p_id])
			else:
				tf = 0
			tf_idf_score = tf_idf_score + tf*idf
	return tf_idf_score

def calculate_okapi(inverted_index,words,p_id,avgdl,N):
	okapi_score = 0
	k1 = 2.0
	b = 0.75
	p = Products.objects.get(product_id = str(p_id))
	D = len(p.product_description)
	for word in words:
		if word in inverted_index.keys():
			idf = math.log(N/float(len(inverted_index[word])))
			if p_id in inverted_index[word].keys():
				tf = 1 + math.log(inverted_index[word][p_id])
			else:
				tf = 0
			okapi_score = okapi_score + idf*((tf*(k1+1))/(tf + k1*(1-b+b*(D/avgdl))))

	return okapi_score

target = open('scores.csv', 'w')
#f =  open('train.csv','r+')

csv_file = open('train.csv','rb')
csv_reader = csv.reader(csv_file)
cnt = 0
for fields in csv_reader:

	if cnt == 0:
		cnt = cnt + 1
		continue
	#fields = line.split(",")
	#print fields
	fields[3] = fields[3].replace(".","")
	fields[3] = fields[3].replace("$","")
	fields[3] = fields[3].replace("\"","")
	fields[3] = fields[3].replace("(","")
	fields[3] = fields[3].replace(")","")
	fields[3] = fields[3].replace("[","")
	fields[3] = fields[3].replace("]","")
	fields[3] = fields[3].replace("'","")
	fields[3] = fields[3].replace("#","")
	fields[3] = fields[3].replace("\\","-")
	fields[3] = fields[3].lower().strip()
	fields[3] = remove_non_ascii(fields[3])
	words = [stemmer.stem(i) for i in fields[3].split() if str(i) not in stop_words]


	p_id = str(fields[1])

	p_n_tf_idf = calculate_tf_idf(p_n_inverted_index,words,p_id)
	p_d_tf_idf = calculate_tf_idf(p_d_inverted_index,words,p_id)
	p_a_tf_idf = calculate_tf_idf(p_a_inverted_index,words,p_id)
	
	s_tf_idf = (3*p_n_tf_idf + 2*p_d_tf_idf + 1*p_a_tf_idf)/6
	

	p_n_avgdl = p_n_total_length/float(124428)
	p_d_avgdl = p_d_total_length/float(124428)
	p_a_avgdl = p_a_total_length/float(124428)

	p_n_okapi = calculate_okapi(p_n_inverted_index,words,p_id,p_n_avgdl,124428)
	p_d_okapi = calculate_okapi(p_d_inverted_index,words,p_id,p_d_avgdl,124428)
	p_a_okapi = calculate_okapi(p_a_inverted_index,words,p_id,p_a_avgdl,124428)

	s_okapi = (3*p_n_okapi + 2*p_d_okapi + 1*p_a_okapi)/6

	w_string = fields[0]+","+str(s_tf_idf)+","+str(s_okapi)+","+fields[4]+"\n"
	target.write(w_string)

		
target.close()
