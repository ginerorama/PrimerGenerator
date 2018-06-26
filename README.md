# PrimerGenerator v0.2
![alt text](https://github.com/ginerorama/PrimerGenerator/blob/master/Primer.gif)

A simply tool for pick primers from a DNA sequence 

Important note: Several tests have been performed with this program to design 
primers that worked fine for PCR experiments. However this software is still experimental, 
and their results should be taken with cautions. 

<br />
<br />
<p align="center">
<img src="https://github.com/ginerorama/PrimerGenerator/blob/master/pic1.png" width="370" height="590">
<br />
<br />

## Usage
<br />

`python Primergenerator.py

<br /><br />


## Input file
<br />


Primergenerator requiere a fasta or multifasta file containing all the sequence genes that are going to be scanned for primers. 
<br />


## Parameters
<br />
All these parameters appears in the Tkinter GUI of PrimerGenerator
<br /><br />

`primer size:` desired size of primers that Primergenerators have to find.
`max GC percentage:` maximum % GC admited for primers. 
`min GC percentage:` minimun % GC admited for primers (have to be 1 below to max GC value). 

`QPCR checkbox:` if check it, Primergenerators will find primers that renders a band of size
				between the maximum and minimum size set for the amplicon.  

`max size for amplicon:` maximun size of amplicon that should be amplified in the QPCR. 
`min size for amplicon:` minimum size of amplicon that should be amplified in the QPCR. 	
<br /><br />


## Ouput

<br />
Primergenerators generates a txt file as output with all the forwards and reverse primers listed for all
the genes presents in the fasta/multifasta file. 
<br />
<br />
