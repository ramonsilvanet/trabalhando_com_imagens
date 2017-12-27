import urllib.request
import mysql.connector
import sys

url = "http://farm4.static.flickr.com/3175/2737866473_7958dc8760.jpg"
file_name = "00001.jpg"

cnx = mysql.connector.connect(user='root', password='secret',
                              host='127.0.0.1', port='33061',
                              database='imagenet')

cursor = cnx.cursor()


def save_images_url(img_id, url, filename):
    add_annotations = ("UPDATE annotations "
               " SET url = %s, filename = %s "
               "WHERE img_id = %s")
    data_annotation = (str(img_id), url, filename)
    cursor.execute(add_annotations, data_annotation)


file_object  = open("annotations/spring10_urls.txt", "r")

i = 0

for line in file_object:
	i = i + 1
	img = line.split("\t")
	url = img[1].rstrip()
	img_id = img[0]

	file_name = "{}.jpg".format(img_id) 
	file_path = "../dataset/imagenet/{}".format(file_name)

	print(i, file_path)

	try:
		with urllib.request.urlopen(url) as response, open(file_path, 'wb') as out_file:
			data = response.read()
			out_file.write(data)
			save_images_url(img_id, url, file_name)

			if( i % 100 == 0) :
				print("-------------------------------------------------------")
				print("Commitando")
				cnx.commit()

	except urllib.error.URLError:
		print("Falha no download")
	except:
		print("Unexpected error:", sys.exc_info()[0])


cnx.commit()

cursor.close()
cnx.close()