#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import codecs
import datetime
import MySQLdb

dbip = 'localhost'
dbuser = 'root'
dbpass = '1'
dbname = 'tree'
db = MySQLdb.connect(dbip,dbuser,dbpass,dbname)
cursor = db.cursor()
path_lib = []

# sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
# # sys.stdin.encoding = 'UTF-8'
# sys.stdout.encoding = 'UTF-8'
# # sys.stderr.encoding = 'UTF-8'

def transliterate(string):

    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E',
                       u'Є': u'E',
                       u'І': u'I',}

    capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',
                                                          u'Ц': u'Ts',
                                                          u'Ч': u'Ch',
                                                          u'Ш': u'Sh',
                                                          u'Щ': u'Sch',
                                                          u'Ю': u'Yu',
                                                          u'Ї': u'Yi',
                                                          u'Я': u'Ya',}


    lower_case_letters = {u'а': u'a',
                       u'б': u'b',
                       u'в': u'v',
                       u'г': u'g',
                       u'д': u'd',
                       u'е': u'e',
                       u'ё': u'e',
                       u'ж': u'zh',
                       u'з': u'z',
                       u'и': u'i',
                       u'й': u'y',
                       u'к': u'k',
                       u'л': u'l',
                       u'м': u'm',
                       u'н': u'n',
                       u'о': u'o',
                       u'п': u'p',
                       u'р': u'r',
                       u'с': u's',
                       u'т': u't',
                       u'у': u'u',
                       u'ф': u'f',
                       u'х': u'h',
                       u'ц': u'ts',
                       u'ч': u'ch',
                       u'ш': u'sh',
                       u'щ': u'sch',
                       u'ъ': u'',
                       u'ы': u'y',
                       u'ь': u'',
                       u'э': u'e',
                       u'ю': u'yu',
                       u'я': u'ya',
                       u'є': u'e',
                       u'ї': u'yi',
                       u'’': u'',
                       u'\'': u'',
                       u'»': u'',
                       u'«': u'',
                       u'–': u'-',
                       u'і': u'i',}

    capital_and_lower_case_letter_pairs = {}

    for capital_letter, capital_letter_translit in capital_letters_transliterated_to_multiple_letters.iteritems():
        for lowercase_letter, lowercase_letter_translit in lower_case_letters.iteritems():
            capital_and_lower_case_letter_pairs[u"%s%s" % (capital_letter, lowercase_letter)] = u"%s%s" % (capital_letter_translit, lowercase_letter_translit)

    for dictionary in (capital_and_lower_case_letter_pairs, capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.iteritems():
            string = string.replace(cyrillic_string, latin_string)

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.iteritems():
        string = string.replace(cyrillic_string, latin_string.upper())

    return string

def write_to_database(item, iterator):
		
		sql = "INSERT INTO tree.testtree(id, path) VALUES ('%d', '%s')" %(iterator ,item)
		
		try:
				cursor.execute(sql)
				db.commit()
		except:
				db.rollback()
				print "failure write"
		

path = os.path.split(os.path.abspath(__file__))[0]
target_file = path+'/for_ruslan_tree_fcp.SMGO.txt'
if os.path.isfile(target_file):
	print 'file exists'
file = open(target_file, 'r').readlines()
iterator = 1
for line in file:
	write_to_database(line[:-1], iterator)
	iterator+=1
	a = line.split('/')
	dir = ''
	for item in a[1:-1]:
		dir += '/'
		dir += item
	if dir not in path_lib:
		path_lib.append(dir)
for item in path_lib:
	print item
	write_to_database(item, iterator)
	iterator+=1
	# good = transliterate(line[:-1])
	# print good
	
	
		


db.close()




