import glob,os
import numpy as np
import pylab as plt
from argparse import ArgumentParser

parser = ArgumentParser(description='Statistics on loop abego types and their sequences ')
parser.add_argument('-data', type=str, help='data file')
parser.add_argument('-connection', type=str, help='type of loop connection')
parser.add_argument('-abego', type=str, help='abego of interest')
parser.add_argument('-restrict_length', type=int, help='only focus on loop lengths equal to that of the loop of interest')
parser.add_argument('-compress', action='store_true', help='merge abego types with abego edges equivalent to the abego for the adjoining secondary structure element' )
args = parser.parse_args()

# Execute as:
#python read_stats_HH.py -data abego_seq_stats_PDB_HH-EH-HE.out -abego xxx -connection HH

datafile = args.data
target_abego = args.abego
target_connection = args.connection
abego_compression = args.compress
restrict_length = args.restrict_length

dic={'HH':{}, 'EH':{}, 'HE':{}, 'EE':{}}
dic_seq={}

# initialize positional dictionary for aa
aa_list = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
aa_list.sort()

seq_pos=[]
if target_abego is not None:
	for i in range(len(target_abego)+2):
		dic_aa={}
		for aa in aa_list:
			dic_aa[aa]=0.0
		seq_pos.append( dic_aa )
elif restrict_length is not None:
        for i in range(restrict_length+2):
                dic_aa={}
                for aa in aa_list:
                        dic_aa[aa]=0.0
                seq_pos.append( dic_aa )

# Read data
for line in open(datafile):
		if line[:4]== '/lab':
			conn = line.split()[1]
			abego = line.split()[-1]
			seq = line.split()[-2]
#			seq_cap = line.split()[-3]
		
			check = abego_compression
			# for abego compression
			#--------------------------
			while check:
				check=False
				if conn[0] =='H' and abego[0] =='A' and len(abego)>1:
					abego=abego[1:]
					check=True
				if conn[1] =='H' and abego[-1] =='A'and len(abego)>1:
					abego=abego[:-1]
					check=True
				if conn[0] =='E' and abego[0] =='B'and len(abego)>1:
					abego=abego[1:]
					check=True
				if conn[1] =='E' and abego[-1] =='B'and len(abego)>1:
					abego=abego[:-1]
					check=True
			#--------------------------
			dic[conn].setdefault(abego,0)
			if restrict_length is not None:
				if len(abego)==restrict_length: # in case only interested in a given length
					dic[conn][abego]+=1
			else:
					dic[conn][abego]+=1

			#---------------------------------
			# Check sequences for target abego
			#---------------------------------
        	        if abego==target_abego and conn==target_connection:	
				#print line
				# Fill whole sequence in dictionary
	                        if seq in dic_seq.keys():
					dic_seq[seq]+=1
	                        else:
					dic_seq[seq]=1

				# Get aa for each position separately
				#print seq
	                        for i in range(len(abego)+2):
					#print i, seq[i]
					seq_pos[i][seq[i]]+=1
					#print seq_pos


# Print and plot summarized data
if target_abego is not None:
	top=30
elif restrict_length is not None:
	top = 100     

if target_abego is not None:
	print 'Frequency of aa sequences'
	print '--------------------------------------'
	print 'Ranking Sequence #found #found/max'
	top=30
#	plt.figure()
	keys = dic_seq.keys()
	keys.sort(lambda x,y : -cmp(dic_seq[x],dic_seq[y]))
	max_freq = dic_seq[keys[0]]
	c=0
	for rank,key in enumerate(keys[:top]):
		freq = dic_seq[key]
#		plt.bar(0.5+c-0.25,freq)
		print rank+1, key, freq, float(freq)/max_freq
		c+=1

#	plt.xticks(np.arange(0.5, c+0.5, 1))
#	plt.gca().set_xticklabels(keys[:c],rotation='vertical')
#	plt.axis([0,c,0,max_freq])

#---------------------------------------
# Matrix of Frequencies
#---------------------------------------
#	npos = len(target_abego)+2
#	posfreq = np.zeros((npos,20))
#print seq_pos

#	for pos in range(npos):
 #       	for j,aa in enumerate(aa_list):
  #              	posfreq[pos,j] = seq_pos[pos][aa]


#	import matplotlib.colors as colors

#	dim1, dim2 = posfreq.shape
#print posfreq
#	plt.figure()
#	plt.pcolor(posfreq,cmap=plt.jet())
#	plt.xticks(np.arange(0.5, dim2+0.5, 1))
#	plt.yticks(np.arange(0.5, dim1+0.5, 1))
#	plt.gca().set_xticklabels(aa_list)

#	ylabel = [ '%s' %(conn[0]) ]
#	for i in range( len(target_abego) ):
#		ylabel.append( '%i.%s' %(i,target_abego[i]) )
#	ylabel.append( '%s' %(conn[1]) )

#	plt.gca().set_yticklabels(ylabel)
#	plt.colorbar()

#	plt.show() 


