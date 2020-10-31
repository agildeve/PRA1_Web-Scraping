# Importem les llibreries que utilitzarem:
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm


# Definim el Dataframe bp_dataset, per anar guardant la informació obtinguda a través del scraping:

bp_dataset = pd.DataFrame(
    columns=['Categoria_1', 'Categoria_2', 'Categoria_3', 'Categoria_4', 'Categoria_5', 'Nom', 'Preu', 'Quantitat',
             'Preu unitari', 'Oferta', 'Promocio', 'URL'])

# Definim la funció sc_bonpreu que, donada una url, fa scraping a la url i utilitza les categories per classificar la informació dels productes:

def sc_bonpreu(url):
    bp_dataset = pd.DataFrame(
        columns=['Categoria_1', 'Categoria_2', 'Categoria_3', 'Categoria_4', 'Categoria_5', 'Nom', 'Preu', 'Quantitat',
                 'Preu unitari', 'Oferta', 'Promocio', 'URL'])

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    # Primer, ens situem a les categories de classificació.
    cat = soup.find('div', class_='bar__Bar-gf1nko-0 EGrQK')
    pos = 0
    lst = ['-', '-', '-', '-', '-']
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
                       'URL' : url_producte}

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
                       'URL' : 'NULL'}

            bp_dataset = bp_dataset.append(add_row, ignore_index=True)

    return bp_dataset


# Finalment, executem la funció per a cada una de les urls obtingudes en el script anterior:
for x in tqdm(urls_finals):
    df = sc_bonpreu(x)
    bp_dataset = bp_dataset.append(df, ignore_index=True)

# Guardem la informació en el dataset:
bp_dataset.to_csv('bp_dataset_v2.csv', index=True)
