import os
from mongoengine import *
path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir("../data")

class Products(DynamicDocument):
	product_id = StringField()
	product_name = DictField()
	product_description = DictField()
	product_attributes = DictField()

stop_words_file = open('stop-word-list.csv','r+')
for line in stop_words_file:
	stop_words = line.split(", ")

if connect('product_info'):
	print "Database Connected"
else:
	print "Connection cannot be established"
print stop_words

'''
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
	words = [i for i in fields[1].split() if i not in stop_words]
	#print "---------------------"
	#print words
	#print "---------------------"
	temp_dict = {}
	for word in words:
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
			fields[2] = fields[2].replace("#","")
			fields[2] = fields[2].replace("\\","-")
			fields[2] = fields[2].lower().strip()
			words = [i for i in fields[2].split() if i not in stop_words]
			#print "---------------------"
			#print words
			#print "---------------------"
			temp_dict = {}
			for word in words:
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
		fields[2] = fields[2].replace("#","")
		fields[2] = fields[2].replace("\\","-")
		fields[2] = fields[2].lower().strip()
		words = [i for i in fields[2].split() if i not in stop_words]
			#print "---------------------"
			#print words
			#print "---------------------"
		temp_dict = {}
		for word in words:
			if word in  temp_dict:
				count = temp_dict[word]
				temp_dict.update({word : count + 1})
			else:
				temp_dict.update({word : 1})
		print temp_dict
		p = Products(product_id = fields[1],product_name = temp_dict,product_description = {} , product_attributes = {})
		p.save()	
'''
f = open('attributes.csv','r+')
for line in f:
	fields = line.split(",")
	try:
		p = Products.objects.get(product_id = fields[0])
		print fields[1]
		if p:
			fields[2] = fields[2].replace(".","")
			fields[2] = fields[2].replace("$","")
			fields[2] = fields[2].replace("\"","")
			fields[2] = fields[2].replace("(","")
			fields[2] = fields[2].replace(")","")
			fields[2] = fields[2].replace("#","")
			fields[2] = fields[2].replace("\\","-")
			fields[2] = fields[2].lower().strip()
			words = [i for i in fields[2].split() if i not in stop_words]
			#print "---------------------"
			#print words
			#print "---------------------"
			temp_dict = {}
			for word in words:
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
		fields[2] = fields[2].replace(".","")
		fields[2] = fields[2].replace("$","")
		fields[2] = fields[2].replace("\"","")
		fields[2] = fields[2].replace("(","")
		fields[2] = fields[2].replace(")","")
		fields[2] = fields[2].replace("#","")
		fields[2] = fields[2].replace("\\","-")
		fields[2] = fields[2].lower().strip()
		words = [i for i in fields[2].split() if i not in stop_words]
			#print "---------------------"
			#print words
			#print "---------------------"
		temp_dict = {}
		for word in words:
			if word in  temp_dict:
				count = temp_dict[word]
				temp_dict.update({word : count + 1})
			else:
				temp_dict.update({word : 1})
		print temp_dict
		p = Products(product_id = fields[0],product_name = {},product_description = {} , product_attributes = temp_dict)
		p.save()
