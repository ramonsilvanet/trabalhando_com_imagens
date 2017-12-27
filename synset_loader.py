
import urllib.request
import mysql.connector
import sys
import os

import requests


base_url = "http://www.image-net.org/api/text/wordnet.synset.getwords?wnid={}"
file_object  = open("imagenet.synset.obtain_synset_list.txt", "r")


def save_synset(synset_id, words):
	add_annotations = ("INSERT INTO synsets "
		"(synset_id, words) "
		"VALUES (%s, %s)")
	data_annotation = (str(synset_id), words)
	cursor.execute(add_annotations, data_annotation)


cnx = mysql.connector.connect(user='root', password='secret',
                              host='127.0.0.1', port='33061',
                              database='imagenet')

cursor = cnx.cursor()

for line in file_object:
	url = base_url.format(line)

	with urllib.request.urlopen(url) as response:
		
		conteudo = response.read().decode("utf-8").rstrip().replace("\n", ", ")

		save_synset(line, conteudo)
		print(">>>" , conteudo)



cnx.commit()
cursor.close()
cnx.close()