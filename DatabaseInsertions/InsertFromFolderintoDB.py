import sqlite3
import os
import sys
connection = None
cursor = None

def connect(path):
	global connection, cursor

	connection = sqlite3.connect(path)
	cursor = connection.cursor()
	cursor.execute(' PRAGMA foreign_keys=ON; ')
	connection.commit()
	return

def cyclethru(directory_in_str):
	directory = os.fsencode(directory_in_str)
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".wav"):
			pathname = os.path.join(directory, file)
			finalpath = os.fsdecode(pathname)
			new = filename.replace('.wav', '')
			executestring = "INSERT INTO alphabet VALUES ('{}','','{}')".format(new, finalpath)

			#print(executestring)
			cursor.execute(executestring)
	connection.commit()
	return

def sound(directory_in_str):
	directory = os.fsencode(directory_in_str)
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".wav"):
			pathname = os.path.join(directory, file)
			finalpath = os.fsdecode(pathname)
			new = filename.replace('.wav', '')
			if len(new) == 3:
				if new[2] == '^':
					executestring = "INSERT INTO PairSounds VALUES ('{}','{}','{}','{}')".format(new, new[0:2], new[2], finalpath)
				else:
					executestring = "INSERT INTO PairSounds VALUES ('{}','{}','{}','{}')".format(new, new[0], new[1:3], finalpath)

			else:
				executestring = "INSERT INTO PairSounds VALUES ('{}','{}','{}','{}')".format(new, new[0], new[1], finalpath)


			#print(executestring)

			cursor.execute(executestring)
	connection.commit()
	return

def main():
	global connection, cursor
	try:
		f = open(sys.argv[1])
		f.close()
	except OSError:
		print("Database does not exist.")
		exit()
	path=sys.argv[1]
	connect(path)


	sound(sys.argv[2])
	connection.commit()
	connection.close()
	return

main()
