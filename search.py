import pandas as pd
import numpy as np
import urllib.request
import mysql.connector
import sys


df = pd.read_csv('annotations/winter11_urls.txt', header=None, names=["img_id", "url"], sep="\t")

print("urls loaded...")


def download(img_id, url):

	filename = "{}.jpg".format(img_id)
	file_path = "../dataset/images/{}".format(filename)
	print(file_path, url)

	try:
		with urllib.request.urlopen(url) as response, open(file_path, 'wb') as out_file:
			data = response.read()
			out_file.write(data)
			save_url(url, filename, img_id)
	except mysql.connector.Error as err:
		print("Something went wrong: {}".format(err))
	except:
		print("Unexpected error:", sys.exc_info()[0])


def save_url(url, filename, img_id):
	update_url = "UPDATE annotations SET url = %s, filename = %s WHERE img_id = %s"
	data = (url, filename, img_id)
	cursor.execute(update_url, data)


cnx = mysql.connector.connect(user='root', password='secret',
                              host='127.0.0.1', port='33061',
                              database='imagenet')

cursor = cnx.cursor()

query = ("SELECT img_id, wnid FROM annotations")
cursor.execute(query)

print("database loaded")

i = 0

for (img_id, wnid) in cursor:
	i = i + 1
	print(">>>", i, img_id)
	index = df.loc[ df['img_id'] == img_id]
	download(img_id, index['url'].values[0])

cnx.commit()
cursor.close()
cnx.close()