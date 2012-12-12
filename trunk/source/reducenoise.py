#! /usr/bin/env python
import sys
from Bio import AlignIO


'''
parameters handling
'''

inputf = 'input' # default input file
outputf = 'output' # default output file

hasIn = False
hasOut = False

if len(sys.argv) % 2 == 0:
	print >> sys.stderr, 'ERROR!'
	print >> sys.stderr, 'please use correct command'
	print >> sys.stderr, './reducenoise.py -in inputFile -out outputFile'
	sys.exit(1)
else:
	for i in range(1, (len(sys.argv)-1)):
		if sys.argv[i] == '-in':
			hasIn = True
			inputf = sys.argv[i+1]
		if sys.argv[i] == '-out':
			hasOut = True
			outputf = sys.argv[i+1]

if hasIn:
	print 'input file:', inputf
else:
	print 'using default input file:', inputf

if hasOut:
	print 'output file:', outputf
else:
	print 'using default outputfile:', outputf


#######################################################################################################
# definitions here!!!
#######################################################################################################
def readMSA(inputfile):
	'''
	read MSA file in fasta format
	parameters: input file name
	return: alignment
	'''
	ifile = open(inputfile, 'r')
	alignment = AlignIO.read(ifile, 'fasta')
	ifile.close()
	return alignment
def writeMSA(msa, outputfile):
	'''
	write the provided msa to file
	'''
	ofile = open(outputfile, 'w')
	ofile.write(msa.format('fasta'))
	ofile.close()
#######################################################################################################
# running script here!!!
#######################################################################################################
try:
	alignment = readMSA(inputf)
except IOError:
	print >> sys.stderr, 'ERROR! cannot open inputfile:', inputf
	sys.exit(1)
#######################################################################################################
# testing script here!!!
#######################################################################################################
writeMSA(alignment, outputf)
	
