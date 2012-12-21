#! /usr/bin/env python
import sys
import sqlite3
import os

inputFile = 'input'
outputFile = 'sql.sql'

for i in range(1, len(sys.argv)-1):
	if sys.argv[i] == '-in':
		inputFile = sys.argv[i+1]
	elif sys.argv[i] == '-out':
		outputFile = sys.argv[i+1]

print 'using input file: ', inputFile
print 'using output file: ', outputFile

disData = {}
dataType = ''

try:
	inf = open(inputFile, 'r')

	# read the distance data in input file
	for line in inf:
		if '\t' not in line:
			continue
		if line.startswith('#'):
			break
		line = line.strip()
		data = line.split('\t')
		
		# get file name and data type
		tmpPath = data[0].split('/')
		fileName = tmpPath[len(tmpPath)-1]
		if dataType == '':
			dataType = tmpPath[len(tmpPath)-2]

		# get original distance
		orig_dis = float(data[1])
		# get reduced distance
		reduc_dis = float(data[2])

		disData[fileName] = {}
		disData[fileName]['orig'] = orig_dis
		disData[fileName]['reduc'] = reduc_dis
	inf.close()
		
except Exception as e:
	print >> sys.stderr, e
	print >> sys.stderr, 'Could not open input file!!!'
	sys.exit(1)
	
try:
	isDataCreated = True
	if not os.path.isfile(outputFile):
		isDataCreated = False
	
	# create database cursor
	sql_database=sqlite3.connect(outputFile)
        sql_cursor=sql_database.cursor()

	if isDataCreated == False:
		sql_cursor.execute('''CREATE TABLE Distances (
				type TEXT, 
				MSA_id TEXT, 
				original_distance float, 
				reduced_distance float);''')
	
	for key, value in disData.items():
		insertString = 'INSERT INTO Distances VALUES(\'%s\', \'%s\', %.2f, %.2f);' % (dataType, key, value['orig'], value['reduc'])
		sql_cursor.execute(insertString)
	sql_cursor.close()
	sql_database.commit()	
except Exception as e:
	print >> sys.stderr, e
	print >> sys.stderr, 'Could not execute SQL!!!'
	sys.exit(1)

