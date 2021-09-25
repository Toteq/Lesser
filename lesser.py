#!/usr/bin/env python3

version = 'v1.7'

import docx2txt
from PIL import Image
import os


def felieton(filenamedocx):

	tytuł = ''
	tekst = []#tytuł i tekst
	Linki = []#liniki do grafik
	Podpis = []#podpis i komentarz
	grafika = 0
	zawartość = []

	try:

		for i,line in enumerate(docx2txt.process(filenamedocx,'r').strip().split('\n')):#args.filenamedocx
			if i == 0:
				tytuł += line+'\n'
				continue
			if not line:
				continue
			if grafika and len(line) > 8:
				if line[4] == 's':
					index = line[8:].find('/')
					Linki.append(f'<li><a href="https://{line[8:]}">{line[8:index+8]}</a></li>\n')
					continue
				elif line[4]== ':':
					index = line[7:].find('/')
					Linki.append(f'<li><a href="http://{line[7:]}">{line[7:index+7]}</a></li>\n')
					continue
				elif len(line)>20:
					Linki.append('</ul>\n')#Koniec grafik
					Podpis.append(autor+'\n')#Podpis
					Podpis.append(line[10:])#Komentarz bez początku "Komenatrz:"
					break
			if line == 'Grafika:':
				grafika = 1
				Linki.append('<p>Grafika:</p>\n<ul>\n')
			else:
				if len(line) > 20:
					tekst.append(f'<p>{line}</p>\n')
				else:
					if len(line)>8 and not grafika:
						tekst.append(f'<b>{line}</b>\n')#Akapity
					else:
						autor = line#autor

		#grafiki w tekscie
		Tekst = ''
		index_grafik = []
		tekst = ''.join(tekst)
		długość = len(tekst)
		co_ile = długość//(ile_jest_grafik+1)

		[index_grafik.append(co_ile*x) for x in range(1, ile_jest_grafik+1)]

		for i,litera in enumerate(tekst):
			if i in index_grafik:
				Tekst += '<<<GRAFIKA>>>'+litera
			else:
				Tekst += litera

		zawartość.append(tytuł)
		zawartość.append(''.join(Tekst))
		zawartość.append(''.join(Linki))
		zawartość.append(''.join(Podpis))
		open(filenamedocx[:-5]+'.txt','w').write(''.join(zawartość))
		print('#Plik',filename[:-4]+'txt','poprawnie stworzony')

	except TabError:
		print('#Błąd pliku',filenamedocx,'- możliwe złe rozszerzenie')
		print(TabError)
		return 0


def poezja(filenamedocx):

	tytuł = ''
	tekst = []#tytuł i tekst
	linki = []#liniki do grafik
	podpis = []#podpis i komentarz
	grafika = 0
	enter = 0
	po = False
	zawartość = []

	try:

		for i,line in enumerate(docx2txt.process(filenamedocx,'r').strip().split('\n')):#args.filenamedocx

			if i == 0:
				tytuł += line+'\n'
				tekst.append(f'<br /><br /><p class="ct"><strong>{line}</strong></p><br />\n\n')
				po = True
				continue
			if not line:
				enter += 1
				continue
			if grafika and len(line) > 8:
				if line[4] == 's':
					index = line[8:].find('/')
					linki.append(f'<li><a href="https://{line[8:]}">{line[8:index+8]}</a></li>\n')
					continue
				elif line[4]== ':':
					index = line[7:].find('/')
					linki.append(f'<li><a href="http://{line[7:]}">{line[7:index+7]}</a></li>\n')

				linki.append('</ul>\n')#Koniec grafik
				podpis.append(line[10:])#Komentarz bez początku "Komenatrz:"
				break
			if line == 'Grafika:':
				grafika = 1
				linki.append('</p>\n\n<p>Grafika:</p>\n<ul>\n')
			else:
				if grafika:
					podpis.append(line+'\n')#Podpis
				else:
					if po:
						tekst.append(f'<p class="ct">{line}')
						enter = 0
						po = False
						continue
					if enter > 3:
						tekst.append(f'</p>\n\n<br /><br /><p class="ct"><strong>{line}</strong></p><br />\n\n')
						enter = 0
						po = True
						continue

					else:
						if enter == 3: tekst.append('<br />\n')
						tekst.append(f'<br />\n{line}')
						enter = 0


		zawartość.append(tytuł)
		zawartość.append(''.join(tekst))
		zawartość.append(''.join(linki))
		zawartość.append(''.join(podpis))
		open(filenamedocx[:-5]+'.txt','w').write(''.join(zawartość))
		print('#Plik',filename[:-4]+'txt','poprawnie stworzony')

	except TabError:
		print('#Błąd pliku',filenamedocx,'- możliwe złe rozszerzenie')
		print(TabError)
		return 0


def zdjęcie(filenamezdj):

	img = Image.open(filenamezdj)
	width,height = img.size[0],img.size[1]

	if img.size[0] == 300 or img.size[0] == 280:
		print('\t#Plik',filenamezdj+' ma odpowiednie wymiary')
		return 0

	if img.size[0] < img.size[1]:
		new_width = 280

	if img.size[0] > img.size[1]:
		new_width = 300

	if img.size[0] == img.size[1]:
		new_width = 300

	new_height = int(new_width * height / width)


	resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)

	try:
		if filenamezdj[-3:] == 'jpg' or filenamezdj[-3:] == 'jpeg':
			resized_img.save(filenamezdj)
			print('#Plik',filenamezdj+' poprawnie stworzony')
			return
		else:
			try:
				resized_img.save(filenamezdj[:-3]+'jpg')
			except:
				resized_img.save(filenamezdj)
				print('#Plik',filenamezdj[:-3]+filenamezdj[-3:]+' poprawnie stworzony')
				return
			print('#Plik',filenamezdj[:-3]+'jpg'+' poprawnie stworzony')
			return

	except:
		print('#Błąd pliku',filename)
		return



print(f'######### lesser.py ### {version} #########\n')

jestplik = False
ile_jest_grafik = 0
for filename in os.listdir():

	if (filename[-3:] == 'jpg' or filename[-3:] == 'png' or filename[-4:] == 'jpeg'):
		jestplik = True
		ile_jest_grafik += 1

		if filename[-5].isdigit(): zdjęcie(filename)

if ile_jest_grafik == 0:
	print('#Nie znaleziono grafik')

for filename in os.listdir():

	if filename[-4:] == 'docx':
		if ile_jest_grafik > 1:
			felieton(filename)
		if ile_jest_grafik == 1:
			poezja(filename)
		jestplik = True

if not jestplik:
	print('#Nie znaleziono żadnych plików')


#	#		#		#		#		Jakub "ybuq" Idec		#		#		#		#	#