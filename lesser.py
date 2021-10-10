#!/usr/bin/env python3

version = 'v2.2'

import docx2txt#https://pypi.org/project/docx2txt/
from PIL import Image#https://pypi.org/project/image/
import os


def felieton(filenamedocx):

	tytuł = ''
	tekst = []#tytuł i tekst
	Linki = []#liniki do grafik
	Podpis = []#podpis i komentarz
	autor = 'Czytelnik SGI Lesser'#Autor domyślny gdy nie ma podpisu
	grafika = 0
	zawartość = []

	try:

		for i,line in enumerate(docx2txt.process(filenamedocx,'r').strip().split('\n')):
			if i == 0:
				tytuł += line+'\n'#Na początku wydzielam tytuł
				continue
			if not line:
				continue
			if grafika and len(line) > 8:#Tworzenie linków gdy line nie jest podpisem
				if line[4] == 's':#https
					index = line[8:].find('/')
					Linki.append(f'<li><a href="https://{line[8:]}">{line[8:index+8]}</a></li>\n')
					continue
				elif line[4]== ':':#http
					index = line[7:].find('/')
					Linki.append(f'<li><a href="http://{line[7:]}">{line[7:index+7]}</a></li>\n')
					continue
				elif len(line)>20:#Kiedy trafimy na Komentarz(samo "Komentarz:" ma 10 znaków - mogą być problemy przy krótszych komentarzach)
					Linki.append('</ul>\n')#Koniec listy
					Podpis.append(autor+'\n')#Podpis
					Podpis.append(line[10:])#Komentarz bez "Komenatrz:"
					break
			if line == 'Grafika:':#Start grafika
				grafika = 1
				Linki.append('<p>Grafika:</p>\n<ul>\n')
			else:
				if len(line) > 20:#Treść artykułu
					tekst.append(f'<p>{line}</p>\n')
				else:
					if len(line) > 8 and len(line) < 20 and not grafika:#Podpis w Tekstach Czytelnika i nie tylko...
						tekst.append(f'<b>{line}</b>\n')#Akapity
					else:
						autor = line#Podpis autora


		#Rozmieszczenie grafik w tekscie
		################################

		#Indexy akapitów
		indeksy_akapitów = []#Na jakim indeksie zaczynają się akapity
		długość = 0#Długość tekstu
		licznik_akapitów = 0#Ile jest akapitów
		która_grafika = 0#Przed którą grafiką jest określona liczba akapitów
		for x in range(len(tekst)):
			długość += len(tekst[x])#Długość tekstu w akapicie "x"
			indeksy_akapitów.append(długość)#Dodanie do listy indeksów

		#Odległość od siebie jako średnia
		Tekst = ''#Końcowy tekst
		index_grafik = []#Lista przechowująca indexy gdzie powinny znajdować sie grafiki
		tekst = ''.join(tekst)#Złączenie listy treści artykułu na string
		długość = len(tekst)#Długość artykułu
		co_ile = długość//(ile_jest_grafik)#Co ile grafika

		[index_grafik.append(co_ile*x) for x in range(1, ile_jest_grafik)]#Tworzenie listy która przechowuje kolejne indeksy grafik

		#Uwzględnienie wysokości grafik
		for i in range( len(wysokość_obrazów)-1):
			if wysokość_obrazów[i] > 300:#Przesunięcie obrazu o "przesunięcie" gdy wysokość jest większa od 300px
				przesunięcie = round((abs(300 - wysokość_obrazów[i]) / 21)*86)
				if wysokość_obrazów[i] > 400: index_grafik[0] -= przesunięcie#Gdy obraz jest wyższy niż 400px to przesuń też pierwszy obraz
				index_grafik[i+1] += przesunięcie

		#Uwzględnienie odstępów akapitów
		for x in range(len(tekst)):
			if x in indeksy_akapitów:
				licznik_akapitów += 1
			if x in index_grafik:
				index_grafik[która_grafika] -= 86*licznik_akapitów#86 znaków ma najdłuższy wiersz
				licznik_akapitów = 0
				która_grafika += 1

		for i,litera in enumerate(tekst):#index, litera
			if i in index_grafik:#Jeżeli index litery jest taki sam jak index grafiki
				Tekst += '<<<GRAFIKA>>>'+litera
			else:
				Tekst += litera

		zawartość.append(tytuł)
		zawartość.append(''.join(Tekst))
		zawartość.append(''.join(Linki))
		zawartość.append(''.join(Podpis))
		open(filenamedocx[:-5]+'.txt','w').write(''.join(zawartość))
		print('#Plik',filenamedocx[:-4]+'txt','poprawnie stworzony')

	except TabError:
		print('#Błąd pliku',filenamedocx,'- możliwe złe rozszerzenie')
		print(TabError)
		return 0


def poezja(filenamedocx):

	Tytuł = ''
	Tekst = []#tytuł i tekst
	Linki = []#liniki do grafik
	Podpis = []#podpis i komentarz
	grafika = 0
	enter = 0
	po = False#Gdy jest "po" akapicie wersów
	zawartość = []

	try:

		for i,line in enumerate(docx2txt.process(filenamedocx,'r').strip().split('\n')):#args.filenamedocx

			if i == 0:#Wykonuje sie tylko raz
				Tytuł += line+'\n'
				Tekst.append(f'<br /><br /><p class="ct"><strong>{line}</strong></p><br />\n\n')#Tytuł wiersza
				po = True
				continue
			if not line:#Gdy jest enter
				enter += 1
				continue
			if grafika and len(line) > 8:#Grafiki
				if line[4] == 's':#https
					index = line[8:].find('/')
					Linki.append(f'<li><a href="https://{line[8:]}">{line[8:index+8]}</a></li>\n')
					continue
				elif line[4]== ':':#http
					index = line[7:].find('/')
					Linki.append(f'<li><a href="http://{line[7:]}">{line[7:index+7]}</a></li>\n')

				Linki.append('</ul>\n')#Koniec grafik
				Podpis.append(line[10:])#Komentarz bez początku "Komenatrz:"
				break
			if line == 'Grafika:':#Grafika start
				grafika = 1
				Linki.append('</p>\n\n<p>Grafika:</p>\n<ul>\n')
			else:
				if grafika:#Podpis
					try:
						Podpis.append(line+'\n')#Podpis
					except:
						Podpis.append('Czytelnik SGI Lesser\n')
				else:
					if po:#Gdy jest po tytule wiersza
						Tekst.append(f'<p class="ct">{line}')#Akapit wersów
						enter = 0
						po = False#Akapit wersów stop
						continue
					if enter > 3:#Gdy są 4 entery to jest odstęp między wierszami(dla bezpieczeńtwa większe od 3)
						Tekst.append(f'</p>\n\n<br /><br /><p class="ct"><strong>{line}</strong></p><br />\n\n')#Tytuł wiersza
						enter = 0
						po = True#Akapit wersów start
						continue

					else:
						if enter == 3: Tekst.append('<br />\n')#Gdy wyliczono 3 entery to jest odstęp
						Tekst.append(f'<br />\n{line}')#Wersy
						enter = 0#Brak enterów


		zawartość.append(Tytuł)
		zawartość.append(''.join(Tekst))
		zawartość.append(''.join(Linki))
		zawartość.append(''.join(Podpis))
		open(filenamedocx[:-5]+'.txt','w').write(''.join(zawartość))
		print('#Plik',filenamedocx[:-4]+'txt','poprawnie stworzony')

	except TabError:
		print('#Błąd pliku',filenamedocx,'- możliwe złe rozszerzenie')#Spotkany błąd z rozszerzeniem ".rtf"
		print(TabError)
		return 0


def zdjęcie(filenameimg):#Tworzenie obrazu z odpowiednimi wymiarami

	img = Image.open(filenameimg)#Objekt obrazu
	szerokość,wysokość = img.size[0],img.size[1]#szerokość, wysokość

	if img.size[0] == 300 or img.size[0] == 280:#Gdy obraz ma odpowiednie wymiary
		print('\t#Plik',filenameimg+' ma odpowiednie wymiary')
		wysokość_obrazów[int(filenameimg[-5])-1] = img.size[1]
		return 0

	if szerokość < wysokość:#Gdy wysokość jest większa od szerokości
		nowa_szerokość = 280

	if szerokość > wysokość:#Gdy wysokość jest większa od szerokości
		nowa_szerokość = 300

	if szerokość == wysokość:#Gdy wysokość i szerokość są równe
		nowa_szerokość = 300

	nowa_wysokość = int(nowa_szerokość * wysokość / szerokość)#Nowa wysokość z proporcji


	nowy_img = img.resize((nowa_szerokość, nowa_wysokość), Image.ANTIALIAS)#Nowy obraz
	wysokość_obrazów[int(filenameimg[-5])-1] = nowa_wysokość#Dodanie wysokości

	try:
		if filenameimg[-3:] == 'jpg' or filenameimg[-3:] == 'jpeg':#Gdy stary obraz jest rozszerzenia jpg, jpeg
			nowy_img.save(filenameimg)
			print('#Plik',filenameimg+' poprawnie stworzony')
			return
		else:
			try:
				nowy_img.save(filenameimg[:-3]+'jpg')#Próba zapisania jako jpg
			except:
				nowy_img.save(filenameimg)#Nadpisanie istniejącego
				print('#Plik',filenameimg[:-3]+filenameimg[-3:]+' poprawnie stworzony')
				return
			print('#Plik',filenameimg[:-3]+'jpg'+' poprawnie stworzony')
			return

	except:
		print('#Błąd pliku',filenameimg)
		return



print(f'######### lesser.py ### {version} #########\n')

jestplik = False#Czy wykryto pliki
ile_jest_grafik = 0#Liczba grafik
wysokość_obrazów = {}#Słownik {"numer_obrazu":wysokość}
for filename in os.listdir():#Przeszukiwanie nazw plików obrazów i docx

	if (filename[-3:] == 'jpg' or filename[-3:] == 'png' or filename[-4:] == 'jpeg'):#Wykryto obraz
		jestplik = True
		ile_jest_grafik += 1

		if filename[-5].isdigit(): zdjęcie(filename)#Zmiana obrazu gdy nie jest głównym

	if filename[-4:] == 'docx': filenamedocx = filename

if ile_jest_grafik > 1:
	felieton(filenamedocx)
	jestplik = True
if ile_jest_grafik == 1:#Poezje mają tylko jedno zdjęcie
	poezja(filenamedocx)
	jestplik = True


if ile_jest_grafik == 0:
	print('#Nie znaleziono odpowiednich plików - grafik')
	exit()

if not jestplik:
	print('#Nie znaleziono żadnych plików')
	exit()