import os
import requests
import json
import re  # regex
from bs4 import BeautifulSoup as bs

def get_project_list():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files_dir = os.path.join(dir_path,'input_html')
    json_output_dir = os.path.join(dir_path, 'output_json')

    for root, d_names, f_names in os.walk(files_dir):
        for list_fname in f_names:
            if list_fname.endswith('.html') and 'Projekt' in list_fname:    
                with open(os.path.join(root, list_fname), "r", encoding = 'utf-8') as protokol:
                    html = bs(protokol, 'html.parser')

                    header = html.find_all("table")[0]
                    data = html.find_all("table")[1]

                    hlavicka_list = []
                    head_names = []
                    for rows in header.find_all("tr"):
                        # řádky hlavičky
                        if head_names == []:
                            col_head = rows.find_all("th")
                            for i in col_head:
                                try:
                                    print('-->', i['data-title'])
                                    head_names.append(i['data-title'].strip())
                                except KeyError:
                                    print('-->')
                                    pass
                            head_names.append('Detail')
                            head_names.append('Zpráva')

                    for rows in data.find_all("tr"):
                        # řádky tabulky
                        pom_dict = {}
                        cols = rows.find_all("td")
                        for i, col in enumerate(cols):
                            if head_names[i] == 'Detail':
                                links = col.div.find_all('a')
                                pom_dict[head_names[i]] = links[0]['href']
                                pom_dict[head_names[8]] = links[1]['href']

                            elif col.string is None:
                                pom_dict[head_names[i]] = ''

                            else:
                                pom_dict[head_names[i]] = col.string.strip()

                        hlavicka_list.append(pom_dict)

                    with open(os.path.join(json_output_dir, os.path.splitext(list_fname)[0] + '-polozky.json'), "w", encoding='utf-8') as soubor_out:
                        json.dump(hlavicka_list, soubor_out, indent = 4, ensure_ascii=False)

    return


if __name__ == '__main__':
    get_project_list()

