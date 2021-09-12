#!/usr/bin/env python3

#lesser.py wersja 1.0 - Jakub "ybuq" Idec
import docx2txt
from PIL import Image
import os

#Pobrać od nowa python-docx i popróbować z tymi stylami popróbować z ...paragraph[0].runs

def pisanie(filenamedocx):

	zawartość = []
	grafika = 0

	for i,line in enumerate(docx2txt.process(filenamedocx,'r').strip().split('\n')):#args.filenamedocx
		if i == 0:
			zawartość.append(line+'\n')
			continue
		if not line:
			continue
		if grafika and line.strip():
			if line[4] == 's':
				index = line[8:].find('/')
				zawartość.append(f'<li><a href="https://{line[8:]}">{line[8:index+8]}</a></li>\n')
				continue
			elif line[4]== ':':
				index = line[7:].find('/')
				zawartość.append(f'<li><a href="http://{line[7:]}">{line[7:index+7]}</a></li>\n')
				continue
			else:
				zawartość.append('</ul>\n')
				break
		if line == 'Grafika:':
			grafika = 1
			zawartość.append('<p>Grafika:</p>\n<ul>\n')
		else:
			if len(line) > 20:
				połowa = (len(line)/2)
				zawartość.append(f'<p>{line[0:int(połowa)]}<<<<<<<GRAFIKA>>>>>>>{line[int(połowa):]}</p>\n')
			else:
				zawartość.append(f'<p>{line}</p>\n')

	try:
		open(filenamedocx[:-5]+'.txt','w').write(''.join(zawartość))
	except:
		open(filenamedocx[:-5]+'.txt','w').write(''.join(zawartość))

def zdjęcie(filenamezdj):

	img = Image.open(filenamezdj)
	width,height = img.size[0],img.size[1]

	if img.size[0] < img.size[1]:
		new_width = 280

	if img.size[0] > img.size[1]:
		new_width = 300

	if img.size[0] == 300 or img.size[0] == 280:
		new_width = 300
	new_height = int(new_width * height / width)


	resized_img = img.resize((new_width, new_height), Image.ANTIALIAS) # best down-sizing filter
	if filenamezdj[-3:] == 'jpg' or filenamezdj[-3:] == 'jpeg':
		resized_img.save(filenamezdj[:-3]+filenamezdj[-3:])
	else:
		resized_img.save(filenamezdj[:-3]+'jpg')

#try:
for filename in os.listdir():
	if filename[-4:] == 'docx':
		pisanie(filename)
		print('Plik',filename[:-4]+'.txt','poprawnie stworzony')
	#if filename[-3:] == 'rtf':
		#newname = filename.replace('.rtf', '.docx')
		#output = os.rename(filename, newname)
		#newname = 'Polska Ibiza.docx'
		#pisanie(newname)
	if filename[-3:] == 'jpg' or filename[-3:] == 'png' or filename[-3:] == 'jpeg':
		zdjęcie(filename)
		print('Plik',filename[:-3]+'.jpg','poprawnie stworzony')
#except:
	#print('Błąd')
	#exit()
