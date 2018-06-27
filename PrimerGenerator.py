#!/usr/bin/python
# primergenerator v0.2 
#MIT License
#
#Copyright (c) 2018 Joaquin Giner Lamia
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.




##########################################################################
#
#                   Import  Modules
#
##########################################################################
from __future__ import division


import Tkinter, tkFileDialog, Tkconstants                  
#except ImportError:
#    try tkinter, tkFileDialog, Tkconstants       
#        except ImportError:
#        	print("PrimerGenerator can not acces to Tkinter module")



#import Tkinter, tkFileDialog, Tkconstants 
from tkFileDialog import *
from ttk import *
import tkMessageBox
import subprocess
import os
from Tkinter import *
from tkFileDialog import askopenfilename
import datetime   #module for date and hour
hour = datetime.datetime.now()






##########################################################################
#
#                   Initzialize main Tkinter window
#
##########################################################################


master = Tkinter.Tk() #Declaring of main window
master.geometry("370x590")
master.title("PrimerGenerator")





##########################################################################
#
#                   Utility functions
#
##########################################################################



def Openfunc(): 
	# Open file with fasta sequences.
	global openpath
	global status_check
	openpath= askopenfilename()
	pathlabel.config(text=openpath.split("/")[-1])
	status_check += 1
	return status_check

def Savefunc():
	global savepath
	savepath = asksaveasfile(mode='w', defaultextension=".txt")
	return savepath

def ProceedButtonCommand(mainframe, master): #Command to attach to proceed button
    mainframe.destroy()
    DrawSecondScreen(master) #This line is what lets the command tied to the button call up the second screen

def QuitButtonCommand(master):
    master.destroy()





def run_test(status_check):
	if status_check > 0:
		f = open(openpath,"r")
		for line in f:
			if line[0] == ">":
 				return Run(openpath)
			else:
				return 	tkMessageBox.showinfo("ERROR:","Required a input Fasta file")

	else:
		return 	tkMessageBox.showinfo("ERROR:","Required a input Fasta file")

def Run(openpath):
	
	#savepath = Savefunc()
	
	f = open(openpath,"r")
	
	# get all the variables
	
	try:
		var_qpcr2 = var_qpcr.get()
		size =int(myvar.get())
		gc_top_raw = myvar2.get()
		gc_down_raw = myvar3.get()
		gc_top = float(gc_top_raw)+0.1
		gc_down= float(gc_down_raw)+0.1
		dist_max = int(myvar4.get())
		dist_min = int(myvar5.get())
	except:
		return tkMessageBox.showinfo("ERROR:","some paramaters are empty")	


		# check variables are grater that 0
	if gc_top_raw == 0 or gc_down_raw == 0 or  size == 0:
		return tkMessageBox.showinfo("ERROR:","parameters must be greater than zero")

	if gc_top_raw <= gc_down_raw :
		return tkMessageBox.showinfo("ERROR:","max GC must to be greater than min GC")
		


  	#this module is to write three first line of output text including seq name in fasta format
	output = asksaveasfile(mode='w', defaultextension=".txt")
	output.write("\n"+ "** PrimerGenerator v0.2 date: "+str(hour)+"\n")
	output.write("Parameters:  "+"\n")
	output.write("Primers length: "+str(size)+"\n")
	output.write("Percentage of GC range: "+str(gc_top_raw)+" - "+str(gc_down_raw))

	#Parser Fasta file, extract all sequence and names in a dictionary
	sequences = {}
	for line in f:
		if line.startswith('>'):
			name = line[1:].rstrip('\n')
			sequences[name] = ''
		else:
			sequences[name] = sequences[name] + line.rstrip('\n')


	# iterative loop for every fasta sequence to get potential primers
	for name,seq in sequences.items(): #items() extract values from a dictionary
		name_seq = str(name)
		seq_seq = str(seq) 				
		seq = seq_seq.upper()
		length_seq = len(seq)
		Forward_primer_count=0
		Reverse_primer_count=0
		output.write("\n\n\n"+"-- Primers generated for "+str(name)+" sequence\n\n")
		count_primers = 0
		if var_qpcr2 == 0:   # Normal PCR
			for i in range(len(seq)):
				primer = seq[i:i+int(size)]
				end_iteration = len(seq)/2 # Forward primers are going to be find only in the first 3/4 length of the sequences
				no_c = primer.count("C")
				no_g = primer.count("G")
				length = len(primer)
				#print primer
				#print size
				#print no_c,no_g
				gc = (no_c + no_g)*100.0/float(length)
				if gc >= float(gc_down) and gc < float(gc_top) and length == int(size) and i <= end_iteration:
					Forward_primer_count= Forward_primer_count + 1	
					output.write("\n"+"Forward primer:  5' "+primer + " 3'   forward primer position is: "+str(i))
		

				if gc >= float(gc_down) and gc < float(gc_top) and length == int(size) and i >= (len(seq)*1/2):  
					if count_primers == 0:
						output.write("\n\n\n")
					comp_primer = primer[::-1]       # genera el reverse strand del primer
					basecomplement = {'A':'T', 'C':'G','G':'C','T':'A','N':'N'}
					letters = list(comp_primer) # convertimos el primer en un list para operar en el con el diccionario
					base_comp = ''  
					for base in letters:
						base_comp = base_comp + basecomplement[base]			
						reverse_primer = ''.join(base_comp)
					Reverse_primer_count= Reverse_primer_count+1
					output.write("\n"+"Reverse primer:  5' "+ reverse_primer+ " 3'  Reverse primer position is: "+str(i))
					count_primers =+ 1

		if var_qpcr2 == 1: # Analysis for QPCR	
			if dist_max == 0 or dist_min == 0:
				return tkMessageBox.showinfo("ERROR:","size parameter must be greater than zero")

			if dist_max <= dist_min :
				return tkMessageBox.showinfo("ERROR:","max size must to be greater than min size")	
				
			for i in range(len(seq)):
				primer = seq[i:i+int(size)]
				end_iteration = len(seq)
				no_c = primer.count("C")
				no_g = primer.count("G")
				length = len(primer)
			
				gc = int((no_c + no_g)*100.0/length)
				if gc >= int(gc_down) and gc < int(gc_top) and length == int(size) and i <= end_iteration:	
					
					rev_region = seq[i+int(dist_min):i+int(dist_max)]
					for j in range(len(rev_region)):
						rev_primer = rev_region[j:j+int(size)]
						no_c = int(rev_primer.count("C"))
						no_g = int(rev_primer.count("G"))
						length = len(rev_primer)
						gc = int((no_c + no_g)*100.0/length)									
						if gc >= int(gc_down) and gc < int(gc_top) and length == int(size):
							print gc, gc_down, gc_top
							pos_f = int(i)+int(size)
							pos_rf = int(i)+int(dist_min)+int(j)
							pos_rr = pos_rf+int(size)
							amp_size = int(pos_rr) - int(i)
							Forward_primer_count= Forward_primer_count + 1	
							output.write("\n"+"Forward primer:  5' "+primer + " 3' start/end forward primer position: "+str(i)+"-"+str(pos_f))
			
							comp_primer = rev_primer[::-1]
							basecomplement = {'A':'T','C':'G','G':'C','T':'A','N':'N'}
							letters = list(comp_primer) # convertimos el primer en un list para operar en el con el diccionario
							base_comp = []
							for base in letters:
								base_comp.append(basecomplement[base])			
							reverse_primer = "".join(base_comp)						
							print reverse_primer
							Reverse_primer_count= Reverse_primer_count+1
							output.write("\n"+"Reverse primer:  5' "+ reverse_primer+ " 3' start/end forward primer position: "+str(pos_rf)+"-"+str(pos_rr)+
							"\nAmplicon size: "+str(amp_size)+"\n")		

		
			output.write("\n")
			output.write("\n"+"sequence used for primer generation "+str(name)+" has:  "+str(length_seq)+" bp\n")
			output.write(str(Forward_primer_count)+" forward primers were found\n")
			output.write(str(Reverse_primer_count)+" Reverse primers were found\n") 				


	


	tkMessageBox.showinfo("PrimerGenerator:","analysis is done!!")



def DrawFirstScreen(master):
	var = StringVar()
	
 	mainframe = Frame(master) #This is a way to semi-cheat when drawing new screens, destroying a frame below master frame clears everything from the screen without having to redraw the window, giving the illusion of one seamless transition
	
	Load_input = Button(mainframe, text="Browse", command= lambda: Openfunc())
	ProceedButton = Button(mainframe, text="Run", command=lambda: run_test(status_check)) #Lambda just allows you to pass variables with the command
	QuitButton = Button(mainframe, text = "Quit", command=lambda: QuitButtonCommand(master))
	
	


	mainframe.pack()  
	Load_input.pack()
	ProceedButton.pack(side=LEFT)	
	QuitButton.pack()
 	 





##########################################################################
#
#                   Global  variables
#
##########################################################################

myvar = IntVar()
myvar2 = IntVar()
myvar3 = IntVar()
myvar4 = IntVar()
myvar5 = IntVar()
var_qpcr = IntVar()
status_check = 0	






##########################################################################
#
#                   Tkinter  Labels
#
##########################################################################


dir_path = os.path.dirname(os.path.realpath(__file__))
imagen1=PhotoImage(file=dir_path+"/Primer.gif") 
label1 = Label(master, image=imagen1).pack() 


description1= Label(master, text="Primer size (nt)", anchor="nw").pack()
text_entry = Entry(master, textvariable=myvar)
text_entry.pack()

description2= Label(master, text="max GC percentage").pack()
text_entry2 = Entry(master, textvariable=myvar2)
text_entry2.pack()

description3= Label(master, text="min GC percentage").pack()
text_entry3 = Entry(master, textvariable=myvar3)
text_entry3.pack()

QPCR = Checkbutton(master, text="QPCR primer ?", variable= var_qpcr, onvalue = 1, offvalue = 0)
QPCR.pack() 


description4= Label(master, text="max size for amplicon").pack()
text_entry4 = Entry(master, textvariable=myvar4)
text_entry4.pack()

description5= Label(master, text="min size for amplicon").pack()
text_entry5 = Entry(master, textvariable=myvar5)
text_entry5.pack()


pathlabel = Label(master, text="\nInput file\n", fg="blue", anchor= CENTER)
pathlabel.pack()


DrawFirstScreen(master) 
description5 = (Label(master, text="\nPrimerGenerator v0.2\ndesigned by Joaquin Giner Lamia. 2018.", fg="royal blue",font=(None, 10), height=40, width=40) ).pack()



master.mainloop() 
