import os
import requests
import json
import re  # regex
from bs4 import BeautifulSoup as bs


def scrape_report_detail(input_dir, output_dir,  fname):

    partial_report_info = {}

    with open(os.path.join(input_dir, fname), "r", encoding = 'utf-8') as protokol:
        html = bs(protokol, 'html.parser')

        #základní údaje
        main_info = html.find("div", class_ = "dz-zakl-udaje")
        main_info_dict = {}
        for divs in main_info.find_all('div', recursive=False):
            main_info_dict[divs.label.string] = divs.div.string
        partial_report_info['zakladni_udaje'] = main_info_dict

        #spolunavrhovatel
        doctor = html.find("label", attrs={'for': re.compile("Navrhovatel_Jmeno")})
        d = doctor.find_next("div").string
        partial_report_info['spolunavrhovatel'] = d

        #spoluuchazec
        hospital = html.find("label", attrs={'for': re.compile("Navrhovatel_Uchazec")}) 
        h = hospital.find_next("div").string
        partial_report_info['spoluuchazec'] = h

        #Ostatní provozní náklady - skutečnost 2020

        t = html.find("table", class_="ripTable ostatni-naklady")
        data = t.tbody
        headers = ['Typ nákladu', 'Skutečnost']
        r = {}
        for row in data.find_all("tr"):
            tds = row.find_all("td")
            for i, td in enumerate(tds):
                if i == 0:
                    k = td.string.strip()
                elif i== 2:
                    v = td.input['value']
                else:
                    continue
            r[k] = v
        partial_report_info['provozni_naklady'] = r

        #Osobní náklady souhrn (v tis. Kč)

        t2 = html.find_all("table", class_="ripTable ostatni-naklady")[1]
        data2 = t2.tbody
        headers = ['Typ nákladu', 'Skutečnost']
        r2 = {}
        for row in data2.find_all("tr"):
            tds = row.find_all("td")
            for i, td in enumerate(tds):
                if i == 0:
                    k = td.string.strip()
                elif i== 2:
                    v = td.input['value'] 
                else:
                    continue
            r2[k] = v
            
        partial_report_info['osobni_naklady'] = r2
        

        #Finanční zajištění projektu
        table3 = html.find("legend", string = re.compile("Finanční zajištění projektu"))
        t3 = table3.find_next("table")
        data3 = t3.tbody
        headers = ['Typ finančného zajištění', 'Skutečnost']
        r3 = {}
        for row in data3.find_all("tr"):
            tds = row.find_all("td")
            for i, td in enumerate(tds):
                if i == 0:
                    k = td.string.strip()
                elif i== 2:
                    v = td.input['value']
                else:
                    continue
            r3[k] = v
        partial_report_info['financni_zajisteni_projektu'] = r3


        #Osobní náklady - mzdy
        field = html.find("legend", string = re.compile("Osobní náklady - mzdy"))
        f = field.find_previous("fieldset")
        member_field = f.find_all("legend", string = re.compile("člen týmu"))
        members = {}

        num=1
        for member in member_field:
            member_table = member.find_next("table")
            headers = member_table.find_all("th")
            data = member_table.find_all("td")
            salary = member.find_next("input", id = re.compile('MzdaSkutecnost$'))['value']
            member_info = {}
            for i, head in enumerate(headers):
                if headers[i].string is None:
                    pass
                elif data[i].div.string is None:
                    member_info[headers[i].string.strip()] = ""
                else:
                    member_info[headers[i].string.strip()] = data[i].div.string.strip()
            member_info['Mzda_skutečnost'] = salary
            members['clen_' + str(num)] = member_info
            num += 1
        partial_report_info['osobni_naklady_mzdy'] = members
     
        #osobni naklady - dohody
        partime_field = html.find("legend", string = re.compile("Osobní\s+náklady\s+\-\s+dohody"))
        pf = partime_field.find_previous("fieldset")
        partime_member_field = pf.find_all("legend", string = re.compile("dohoda"))
        partime_members = {}

        num=1
        for partime_member in partime_member_field:
            partime_member_table = partime_member.find_next("table")
            headers2 = partime_member_table.find_all("th")
            data2 = partime_member_table.find_all("td")
            salary2 = partime_member.find_next("input", id = re.compile('CastkaSkutecnost$'))['value']
            partime_member_info = {}
            for i, head in enumerate(headers2):
                if headers2[i].string is None:
                    pass
                elif data2[i].div.string is None:
                    partime_member_info[headers2[i].string.strip()] = ""
                else:
                    partime_member_info[headers2[i].string.strip()] = data2[i].div.string.strip()
            partime_member_info['castka_skutečnost'] = salary2
            partime_members['clen_' + str(num)] = partime_member_info
            num += 1
        partial_report_info['osobni_naklady_dohody'] = partime_members
    
    with open(os.path.join(output_dir, os.path.splitext(fname)[0] + '-polozky.json'), "w", encoding='utf-8') as soubor_out:
        json.dump(partial_report_info, soubor_out, indent = 4, ensure_ascii=False)

    return






#temporary variables
dir_path = os.path.dirname(os.path.realpath(__file__))
files_dir = os.path.join(dir_path,'input_html')
json_output_dir = os.path.join(dir_path, 'output_json')
fname = 'DetailDilciZpravy (27).htm'


if __name__ == '__main__':
    scrape_report_detail(files_dir, json_output_dir, fname)

