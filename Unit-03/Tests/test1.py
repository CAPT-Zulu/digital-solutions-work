import json
import sqlite3

connection = sqlite3.connect("database.db")
cursor1 = connection.cursor()

JOSN_CONFIG_FILE_PATH = "xxx.json"
CONFIG_PROPERTIES={}

try:
	with open(JOSN_CONFIG_FILE_PATH, encoding="utf8") as data_file:
		CONFIG_PROPERTIES=json.load(data_file)
except IOError as e:
	print(e)
	print("Error: can not open the file")

cont = CONFIG_PROPERTIES
#print(CONFIG_PROPERTIES['countries'][1])
#print(cont)
for item,value in cont.items() :
	print(item,"-->",value)
	cursor1.execute('INSERT INTO file VALUES (?,?)',(item,value,))
connection.commit()
connection.close()