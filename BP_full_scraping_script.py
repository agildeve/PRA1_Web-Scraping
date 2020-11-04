# Importem les llibreries que utilitzarem:
from bs4 import BeautifulSoup
import numpy as np
import requests
import pandas as pd
from tqdm import tqdm
from datetime import date

# Busquem les urls
# Com a url principal agafem la més general:

url = 'https://www.compraonline.bonpreuesclat.cat/products'

# Obtenim el contingut de la url
page = requests.get(url).text

# Organitzem el format html:
soup = BeautifulSoup(page, 'lxml')

# Ens situem a la secció de la pàgina d'on obtindrem les categories:
llista = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 kcPzHi')

# Creem un diccionari per a les categories més externes on hi posarem el nom de la categoria juntament amb la seva url:
categoria_1 = {}

# Iterem per omplir el diccionari:
for i in tqdm(llista.find_all('li')):
    categoria_1[i.a.text] = 'https://www.compraonline.bonpreuesclat.cat' + i.a['href']

# Creem un diccionari per a les categories següents:
categoria_2 = {}

# Iterem per omplir el diccionari:
for i in tqdm(categoria_1.values()):
    soup = BeautifulSoup(requests.get(i).text, 'lxml')
    match = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 kcPzHi')

    for j in match.find_all('li'):
        categoria_2[j.a.text] = 'https://www.compraonline.bonpreuesclat.cat' + j.a['href']

# Creem un diccionari per a les categories següents:
categoria_3 = {}

# Creem un llistat per emmagatzemar aquelles categories que ja són les últimes:
productes_2 = []

# Iterem per omplir el diccionari i en cas de no trobar més categories, és a dir, que trobi una que és la última, posar-la en la llista 'productes':
for i in tqdm(categoria_2.values()):
    try:
        soup = BeautifulSoup(requests.get(i).text, 'lxml')
        match = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 kcPzHi')

        for j in match.find_all('li'):
            categoria_3[j.a.text] = 'https://www.compraonline.bonpreuesclat.cat' + j.a['href']

    except Exception as e:
        productes_2.append(list(categoria_2.keys())[list(categoria_2.values()).index(i)])

# Creem un diccionari per a les categories següents:
categoria_4 = {}

# Creem un llistat per emmagatzemar aquelles categories que ja són les últimes:
productes_3 = []

# Iterem per omplir el diccionari i en cas de no trobar més categories, és a dir, que trobi una que és la última, posar-la en la llista 'productes':
for i in tqdm(categoria_3.values()):
    try:
        soup = BeautifulSoup(requests.get(i).text, 'lxml')
        match = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 kcPzHi')

        for j in match.find_all('li'):
            categoria_4[j.a.text] = 'https://www.compraonline.bonpreuesclat.cat' + j.a['href']

    except Exception as e:
        productes_3.append(list(categoria_3.keys())[list(categoria_3.values()).index(i)])

# Creem un diccionari per a les categories següents:
categoria_5 = {}

# Creem un llistat per emmagatzemar aquelles categories que ja són les últimes:
productes_4 = []

# Iterem per omplir el diccionari i en cas de no trobar més categories, és a dir, que trobi una que és la última, posar-la en la llista 'productes':
for i in tqdm(categoria_4.values()):
    try:
        soup = BeautifulSoup(requests.get(i).text, 'lxml')
        match = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 kcPzHi')

        for j in match.find_all('li'):
            categoria_5[j.a.text] = 'https://www.compraonline.bonpreuesclat.cat' + j.a['href']

    except Exception as e:
        productes_4.append(list(categoria_4.keys())[list(categoria_4.values()).index(i)])

# Creem un diccionari per a les categories següents:
categoria_6 = {}

# Creem un llistat per emmagatzemar aquelles categories que ja són les últimes:
productes_5 = []

# Iterem per omplir el diccionari i en cas de no trobar més categories, és a dir, que trobi una que és la última, posar-la en la llista 'productes':
for i in tqdm(categoria_5.values()):
    try:
        soup = BeautifulSoup(requests.get(i).text, 'lxml')
        match = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 kcPzHi')

        for j in match.find_all('li'):
            categoria_6[j.a.text] = 'https://www.compraonline.bonpreuesclat.cat' + j.a['href']

    except Exception as e:
        productes_5.append(list(categoria_5.keys())[list(categoria_5.values()).index(i)])

# Finalment, agrupem totes les categories finals:
categories_finals = productes_2 + productes_3 + productes_4 + productes_5

# Les podem veure per pantalla si volem (n'hi ha unes 800):
# categories_finals

# Però el que ens interessa a nosaltres és la url d'aquestes categories, així que les emmagatzemarem aqui:
urls_finals = []

# Obtenim la url de cada categoria final i la emmagatzem a la llista 'urls_finals' que hem creat:
for i in productes_2:
    urls_finals.append(categoria_2[i])

for i in productes_3:
    urls_finals.append(categoria_3[i])

for i in productes_4:
    urls_finals.append(categoria_4[i])

for i in productes_5:
    urls_finals.append(categoria_5[i])

# Mostrem per pantalla el llistat de urls finals que hem obtingut i sobre les quals realitzarem el scraping:
#urls_finals


####################################################################################################################
####################################################################################################################

# Definim el Dataframe bp_dataset, per anar guardant la informació obtinguda a través del scraping:

bp_dataset = pd.DataFrame(
    columns=['Categoria_1', 'Categoria_2', 'Categoria_3', 'Categoria_4', 'Categoria_5', 'Nom', 'Preu', 'Quantitat',
             'Preu unitari', 'Oferta', 'Promocio', 'URL', 'Date'])

# Definim la funció sc_bonpreu que, donada una url, fa scraping a la url i utilitza les categories per classificar la informació dels productes:

def sc_bonpreu(url):
    bp_dataset = pd.DataFrame(
        columns=['Categoria_1', 'Categoria_2', 'Categoria_3', 'Categoria_4', 'Categoria_5', 'Nom', 'Preu', 'Quantitat',
                 'Preu unitari', 'Oferta', 'Promocio', 'URL', 'Date'])

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    # Primer, ens situem a les categories de classificació.
    cat = soup.find('div', class_='bar__Bar-gf1nko-0 EGrQK')
    pos = 0
    lst = ['-', '-', '-', '-', '-']
    dt = date.today()

    for sibling in cat.li.next_siblings:
        lst[pos] = sibling.text
        pos = pos + 1

        prd = soup.find_all('div', wrap='wrap')

    for i in prd:
        enOferta = 'NO'
        preu_2 = 'NULL'
        for z in i.find('div', class_='base__OfferContainer-sc-7vdzdx-32 jrdCrR'):
          #  print(z)
            if (z):
                enOferta = 'SI'
                preu_2 = z.div.next_sibling.text
        try:
            nom = i.div.h3.a.text
            preu = i.div.strong.text
            qntat = i.find('span', display="inline-block").text
            p_uni = i.find('span', class_="text__Text-x7sj8-0 jrIktQ").text

            a2 = i.find('a')
            url_producte = ('https://www.compraonline.bonpreuesclat.cat' + a2['href'])

            add_row = {'Categoria_1': lst[0],
                       'Categoria_2': lst[1],
                       'Categoria_3': lst[2],
                       'Categoria_4': lst[3],
                       'Categoria_5': lst[4],
                       'Nom': nom,
                       'Preu': preu,
                       'Quantitat': qntat,
                       'Preu unitari': p_uni,
                       'Oferta' : enOferta,
                       'Promocio' : preu_2,
                       'URL' : url_producte,
                       'Date' : dt.strftime("%d/%m/%Y")}

            bp_dataset = bp_dataset.append(add_row, ignore_index=True)

        except Exception as e:
            add_row = {'Categoria_1': 'NULL',
                       'Categoria_2': 'NULL',
                       'Categoria_3': 'NULL',
                       'Categoria_4': 'NULL',
                       'Categoria_5': 'NULL',
                       'Nom': 'PRODUCTE NO OBTINGUT',
                       'Preu': 'NULL',
                       'Quantitat': 'NULL',
                       'Preu unitari': 'NULL',
                       'Oferta' : 'NULL',
                       'Promocio': 'NULL',
                       'URL' : 'NULL',
                       'Date' : 'NULL'}

            bp_dataset = bp_dataset.append(add_row, ignore_index=True)

    return bp_dataset


# Finalment, executem la funció per a cada una de les urls obtingudes en el script anterior:
print("Start Scraping...")
for x in tqdm(urls_finals):
    df = sc_bonpreu(x)
    bp_dataset = bp_dataset.append(df, ignore_index=True)


# Abans de guardar, eliminem rows amb al menys quatre 'na'.
#bp_dataset.drop()
print("Scraping done, cleaning...")
bp_dataset = bp_dataset[bp_dataset['Nom'] != 'PRODUCTE NO OBTINGUT']

# Guardem la informació en el dataset:
print("Saving dataset...")
dt = date.today()
name_to_save = dt.strftime("%Y%m%d") + '_BP_dataset.csv'
bp_dataset.to_csv(name_to_save, index=False)

print(dt.strftime("%d/%m/%Y"), ' - Your saved Dataset has ', bp_dataset.shape[0], ' ROWS and ', bp_dataset.shape[1], 'COLUMNS.')
