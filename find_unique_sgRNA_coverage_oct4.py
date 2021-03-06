#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:43:45 2018

@author: xies
"""

import numpy as np
import matplotlib.pylab as plt
from Bio import SeqIO, SeqRecord
from itertools import count, izip, product

# Load ChIP peaks
filename = '/data/crispri_hamming/oct4/oct4_chip_flanking.fa'
peaks = [rec for rec in SeqIO.parse(filename,'fasta')]
Npeaks = len(peaks)

# Merge ChIP peaks that are within 75bp

#guide_window = 75
#
#df = seqrec2df(peaks)
#chromosomes = np.unique(df['chromosome'])
#unique_peaks = pd.DataFrame()
#for c in chromosomes:
#    this_chrom = df[ df['chromosome'] == c]
#    
#    if len(this_chrom) > 1: # skip if there's only one
#        
#        intervals = zip(this_chrom['start'],this_chrom['end'])
#        # Build the index of pairs
#        II = xrange(len(intervals))
#        index = list(product(II,II))
#        
#        D = np.zeros((len(II),len(II)),dtype=bool)
#        	# Iterate through pairs of intervals using itertools
#        for i, intervPair in izip(count(), product(intervals,intervals)):
#        		ind = index[i]
#        		# Only check one side of diagonal
#        		if ind[0] > ind[1]:
#        			D[ind[0],ind[1]] = overlap(intervPair[0],intervPair[1]) > 20
#	df.loc[df.chromosome == c, 'unique'] = ~np.any(D,axis=0)
##    for (i,I) in enumerate(intervals):
##        j = intervals[j]
##        while 
            
        
    
# Load sgRNA seqs
filename = '/data/crispri_hamming/oct4/sgRNA_unique.fasta'
guides = [rec for rec in SeqIO.parse(filename,'fasta')]
Nguides = len(guides)
# Fix the sequence name
for g in guides:
    g.name = get_peak_name(g.description)

# Load closest hamming distance
filename = '/data/crispri_hamming/oct4/big_distance_matrix.csv'
D = np.loadtxt(filename,delimiter=',')

# Go through all peaks and find the 'most unique' guide
guide_names = [g.name for g in guides]
max_distances = np.ones(Npeaks)*-1
for (i,p) in enumerate(peaks):
    # Find all sgRNA belonging to this peak
    indices = [j for j,n in enumerate(guide_names) if n == p.name]
    if len(indices) > 0:
        max_distances[i] = D[indices,0].max()
    
# Plot the inverse distribution of whether a ChIP peak would have a sgRNA "unique" enough
bins = range(int(max_distances.max())+2)
outs = plt.hist(max_distances[max_distances >= 0],bins=bins,
                cumulative=True,normed=True,align='left')
N = outs[0];
plt.bar(bins[:-1],1-N);
plt.xlabel('Minimum mismatches to other sgRNAs requred');
plt.ylabel('Fraction of ChIP peaks with valid sgRNA')
np.savetxt('/data/crispri_hamming/oct4/peak_coverage.csv',N)

def seqrec2df(peaks):
    # Parse the nameing convention of the ChIP peaks into a machine-readable dataframe
    import pandas as pd
    
    temp_list = []
    for rec in peaks:
        chrom = get_peak_chromosome(rec.name)
        I = get_peak_location(rec.name)
        temp_list.append([rec.name,rec.seq,chrom,I[0],I[1],True])
    
    return pd.DataFrame(data = temp_list,
                        columns = ['name','sequence','chromosome','start','end','unique'])
    
def get_peak_chromosome(name):
    return name.split(':')[0]

def get_peak_location(name):
    start = name.split(':')[1]
    end = start.split('-')[1]
    start = start.split('-')[0]
    return int(start), int(end)

def get_peak_name(desc):
    return desc.split(' ')[1]

