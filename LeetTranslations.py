# -*- coding: utf-8 -*-
# Eli Gatchalian
# May 6, 2016
# CPSC 3400 - P4
# Version 1 - Python3.5.1

# This program reads in a file if extension is of length 2 or 3 except for bat
# and exe. If it is a valid argument, program makes leet translations accordingly:
# 1) Words ending in ed is replaced from ed to d.
# 2) Words ending in er is replaced from er to xor.
# 3) Words with ant, and, or anned is replaced with &.
# 4) Words beginning with f is replaced from f to ph.
# The program makes translations in the above order.
# Translates ed or er if and only if there is a space right after word, nothing else 
# must follow in order to make leet translation.
# Translates f if and only if there is a space right before word, nothing else must
# preceed in order to make leet translation.
# Next, the program replaces the following words:
#     d00d, w00t, sk1llz, h4xx, n0sc0p3, pwn4g3, r0f1
# with the following pattern:
#     10, 20, 35, 55, 80, 110, …
# using a cyclic and numeric generator. These words must only have spaces before and
# after the words to make replacement and is case sensitive.
# Finally, the program writes to n00b.txt with the modified contents.

import itertools
import re
import sys
import string

def leet_translater(pattern,replace,list_of_words):
    translated_list = []
    for word in list_of_words:
        translated_list.append(re.sub(pattern,replace,word))
    return translated_list

def cyclic_generator(pattern,words_of_lists):
    for word in words_of_lists:
        if re.match(pattern,word) != None:
            yield word

def numeric_generator(num):
    adder = 10
    while True:
        yield num
        num += adder
        adder += 5

start_generator = 10
noob = open("n00b.txt","w")
given_file = sys.argv[1]
split_file = given_file.split('.')
extension = split_file[1]

# Accepts extension of length 2 or 3 except bat and exe
if (extension != "bat" or extension != "exe") and len(extension) <= 3 and len(extension) >= 2:
    given_file = open(sys.argv[1],"r")
    print("Writing to n00b.txt...")
else:
    print("Invalid argument. Exiting now.")
    sys.exit()

# Write words in file to lists
original_list = []
for lines in given_file:
    word = lines.split()
    original_list.append(word)
original_list = list(itertools.chain.from_iterable(original_list))

# Words ending in any combination of ed
ed_pattern = re.compile(r'(ed|Ed|eD|ED)$')
# Words ending in any combination of er
er_pattern = re.compile(r'(er|Er|eR|ER)$')
# Words that have ant, and, and anned
ant_and_anned_pattern = re.compile(r""" (ant|Ant|ANt|AnT|aNt|aNT|anT|ANT) |  #Combinations of ant
                                        (and|And|ANd|AnD|aNd|aND|anD|AND) |  #Combinations of and
                                        (anned|ANNED) |                      #All lower or upper case of anned
                                        (Anned|aNned|anNed|annEd|anneD) |    #One uppercase of anned
                                        (ANned|aNNed|anNEd|annED|AnneD) |    #Two uppercase of anned
                                        (ANNed|aNNEd|anNED|AnnED|ANneD) |    #Three uppercase of anned
                                        (ANNEd|aNNED|AnNED|ANnED|ANNeD)      #Four uppercause of anned
                                    """,re.VERBOSE)
# Words that begin with any combination of f
f_pattern = re.compile(r'^(f|F)')

# Make leet translations from ed,er,ant_and_anned, and f
modified_list = leet_translater(ed_pattern,'d',original_list)
modified_list = leet_translater(er_pattern,'xor',modified_list)
modified_list = leet_translater(ant_and_anned_pattern,'&',modified_list)
modified_list = leet_translater(f_pattern,'ph',modified_list)

# Using a cyclic and numeric generator to complete 3a of assignment
leet_pattern = re.compile(r'^(d00d|w00t|sk1llz|h4xx|n0sc0p3|pwn4g3|r0fl)$')
cyc_gen = cyclic_generator(leet_pattern,modified_list)
num_gen = numeric_generator(start_generator)
for leet_word in cyc_gen:
   modified_list[modified_list.index(leet_word)] = next(num_gen)
   
# Writing modified contents to n00b.txt
for word in modified_list:
    noob.write(str(word) + ' ')