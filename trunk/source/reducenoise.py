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
	AlignIO.write(msa, ofile, 'fasta')
	ofile.close()

def isNoise(msa, pos):
	'''
	check if specific column in alignment is noise or not
	return True if yes, False otherwise
	'''
	aa = {}
	for i in range(0, len(msa)):
		if msa[i, pos] not in aa:
			aa[msa[i, pos]] = 1
		else:
			aa[msa[i, pos]] += 1
	
	numOfUniques = 0
	numOfGoodAA = 0
	numOfIndels = 0
	for key, value in aa.items():
		if value == 1:
			numOfUniques += 1
		if value > 2:
			numOfGoodAA += 1
		if key == '-' or key == '.':
			numOfIndels += value

	
	# if more than 50% are indels
	if numOfIndels >= (len(msa) * 1./2):
		return True
	# if more than 50% are unique amino acids
	if numOfUniques >= (len(msa) * 1./2):
		return True
	# if there is no aa that appears more than twice
	if numOfGoodAA == 0:
		return True

	return False
	
def reduceNoise(msa):
	'''
	reduce the noises in MSA
	input: MSA with noises
	output: MSA without noises
	'''
	i = 0
	while i < msa.get_alignment_length():
		while i < msa.get_alignment_length() and isNoise(msa, i):
			msa = msa[:, :i] + msa[:, i+1:]
		i += 1
	
	return msa
	

#######################################################################################################
# running script here!!!
#######################################################################################################
msa = None
try:
	msa = readMSA(inputf)
except IOError:
	print >> sys.stderr, 'ERROR! cannot open inputfile:', inputf
	sys.exit(1)

if msa.get_alignment_length() == 0:
	print >> sys.stderr, 'ERROR! length of the provided MSA is 0'
	sys.exit(1)

print 'length before reducing:', msa.get_alignment_length()
msa = reduceNoise(msa)
print 'length after reducing:', msa.get_alignment_length()
if msa.get_alignment_length() == 0:
	print >> sys.stderr, 'ERROR! the length of the MSA after reducing noise is 0'
	sys.exit(1)

writeMSA(msa, outputf)
#######################################################################################################
# testing script here!!!
#######################################################################################################
#print msa.get_alignment_length()
#msa = reduceNoise(msa)
#print msa.get_alignment_length()
#writeMSA(msa, outputf)

