# PrimerGenerator v0.2
![alt text](https://github.com/ginerorama/PrimerGenerator/blob/master/Primer.gif)

A simply tool for pick primers from a DNA sequence developed in Python using a Tkinter graphical interface

Important note: Several tests have been performed with this program to design 
primers that worked fine for PCR experiments. However this software is still experimental, 
and their results should be taken with cautions. 

<br />
<br />
<p align="center">
<img src="https://github.com/ginerorama/PrimerGenerator/blob/master/pic1.png" width="370" height="590">
<br />
<br />

## Require
	
Tkinter

<br />

## Usage
<br />

`python PrimerGenerator.py`

<br />
PrimerGenerator can be run in UNIX and MAC systems with python 2.7. GUI is optimized for Tkinter in MacOSX, weird aspects for main Tkinter window can be observed in UNIX systems.
<br />


## Input file
<br />


PrimerGenerator requieres a fasta or multifasta file containing all the sequence genes that are going to be scanned for primers. The input file is loaded using the Browse button.
<br /><br />


## Parameters
<br />
All these parameters appears in the Tkinter GUI of PrimerGenerator
<br /><br />

`primer size:` desired size of primers that PrimerGenerators have to find.

`max GC percentage:` maximum % GC admited for primers. 

`min GC percentage:` minimun % GC admited for primers (have to be 1 below to max GC value). 

`QPCR checkbox:` if check it, PrimerGenerators will find a pair of primers that amplify a band of size
				between the maximum and minimum size set for the amplicon.  
				

`max size for amplicon:` maximun size of amplicon that should be amplified in the QPCR. 

`min size for amplicon:` minimum size of amplicon that should be amplified in the QPCR. 	

<br /><br />
*important note: difference between max and min size for amplicon has to be greater than primer size

## Ouput

<br />
PrimergGnerators generates a txt file as output with all the forwards and reverse primers listed for all
the genes presents in the fasta/multifasta file. 
<br />
<br />
An output exemple using the glutamine synhtethase gene (glnA) from the cyanobacterium Synechocystis sp. PCC6803 with a primer size = 30 , max GC percentage = 40 and min GC percentage = 39:
<br />
<br />
<p align="center">
<img src="https://github.com/ginerorama/PrimerGenerator/blob/master/output.png" >

