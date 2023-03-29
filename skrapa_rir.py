import os
import pandas
import requests
from bs4 import BeautifulSoup as BS
import selenium
import PyPDF2

for year in range(2004, 2024):
    rapporter_arsvis_URL = f"https://www.riksrevisionen.se/rapporter/arsvis/{year}.html"
    rapporter_arsvis_page = requests.get(rapporter_arsvis_URL)
    rapporter_arsvis_soup = BS(rapporter_arsvis_page.content, "html.parser")

    rapporter_links = rapporter_arsvis_soup.find_all(class_="rir-bordered-link-list")

    if len(rapporter_links) == 2:
        granskningsrapporter_html, revisionsrapporter_html = rapporter_links[0], rapporter_links[1]
    else:
        print(f"Unexpected number of links: {len(rapporter_links)}")

    # Granskningsrapporter
    granskningsrapporter_href = granskningsrapporter_html.find_all("a", href=True)
    granskningsrapporter_href_links = []
    for rapport in granskningsrapporter_href:
        granskningsrapporter_href_links.append(rapport["href"])

    # Samma sak för revisionsrapporter
    revisionsrapporter_href = revisionsrapporter_html.find_all("a", href=True)
    revisionsrapporter_href_links = []
    for rapport in revisionsrapporter_href:
        revisionsrapporter_href_links.append(rapport["href"])


    print(f"""
    År {year}:
    Hittade {len(granskningsrapporter_href_links)} granskningsrapporter och {len(revisionsrapporter_href_links)} revisionsrapporter
    """)


    base_url = "https://www.riksrevisionen.se"

    # Granskningsrapporter
    soups = []
    granskningsrapporter_namn = []
    for granskningsrapporter_href_link in granskningsrapporter_href_links:
        rapport_sida_url = base_url + granskningsrapporter_href_link
        rapport_namn = granskningsrapporter_href_link.strip(".html").split("/")[-1]
        granskningsrapporter_namn.append(rapport_namn)

        page = requests.get(rapport_sida_url)
        tmp_soup = BS(page.content, "html.parser")
        soups.append(tmp_soup)


    for idx, (soup, granskningsrapport_namn) in enumerate(zip(soups, granskningsrapporter_namn)):
        # Leta efter alla href med ordet "download" i, ta endast den som heter "rapport" (finns också bilagor)
        downloadables = soup.select("a[href*=download][href*=pdf]")
        if len(downloadables) == 1:
            relative_pdf_url = downloadables[0]["href"]
        elif len(downloadables) > 1:
            for downloadable in downloadables:
                if "ladda ner" in downloadable.text.lower():
                    relative_pdf_url = downloadable["href"]
                    break
        else:
            print("No downloadable files found ...")

        # Lägg ihop bas-url med url för specifik rapport
        pdf_url = base_url + relative_pdf_url

        # Ladda ner pdf för rapporten
        target_folder = os.path.join("Data", f"{year}", f"Granskningsrapporter {year}")
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        file_name = f"{granskningsrapport_namn}.pdf"
        if len(file_name) > 120:
            file_name = f"Granskningsrapport_tmp_{idx}.pdf"
        file_path = os.path.join(target_folder, file_name)
        if os.path.exists(file_path):
            file_name = f"{pdf_url.strip('.pdf').split('/')[-1]}_XXX.pdf"
            file_path = os.path.join(target_folder, file_name)
        with open(file_path, "wb") as f:
            f.write(requests.get(pdf_url).content)

    
    # Revisionsrapporter
    soups = []
    revisionsrapporter_namn = []
    for revisionsrapporter_href_link in revisionsrapporter_href_links:
        rapport_sida_url = base_url + revisionsrapporter_href_link
        rapport_namn = revisionsrapporter_href_link.strip(".html").split("/")[-1]
        revisionsrapporter_namn.append(rapport_namn)

        page = requests.get(rapport_sida_url)
        tmp_soup = BS(page.content, "html.parser")
        soups.append(tmp_soup)


    for idx, (soup, revisionsrapport_namn) in enumerate(zip(soups, revisionsrapporter_namn)):
    # Leta efter alla href med ordet "download" i, ta endast den som heter "rapport" (finns också bilagor)
        for downloadable in soup.select("a[href*=download][href*=pdf]"):
            if "ladda ner" in downloadable.text.lower():
                relative_pdf_url = downloadable["href"]
                break

        # Lägg ihop bas-url med url för specifik rapport
        pdf_url = base_url + relative_pdf_url

        # Ladda ner pdf för rapporten
        target_folder = os.path.join("Data", f"{year}", f"Revisionsrapporter {year}")
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        file_name = f"{revisionsrapport_namn}.pdf"
        if len(file_name) > 120:
            file_name = f"Revisionsrapport_tmp_{idx}.pdf"
        file_path = os.path.join(target_folder, file_name)

        with open(file_path, "wb") as f:
            f.write(requests.get(pdf_url).content)
        
    