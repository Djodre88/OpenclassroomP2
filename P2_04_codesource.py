import requests
from bs4 import BeautifulSoup
import csv
import re
import os

path=os.path.dirname(__file__)

site_url="https://books.toscrape.com/"

req=requests.get(site_url)
soup=BeautifulSoup(req.content, "html.parser")

# création d'une table avec en-tête
header=['product_page_url','universal_product_code(upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
l=len(header)
datas=['']*l

# Recherche catégories
categories_list=soup.findAll("ul", attrs={'nav nav-list'})

for cl in categories_list:
    categories=cl.findAll("a")
    categories=categories[1:]
    nb_categories=len(categories)
    ctgr=1

    for category in categories:
        category_url=site_url+str(category.get("href"))
        category_base_url=category_url[:-10]
        catalogue_url=site_url+"catalogue/"
        req=requests.get(category_url)
        soup = BeautifulSoup(req.content, "html.parser")
        category_name=soup.find("h1").text

        print("==================================")
        print("* * * "+category_name+" * * *\n")
        print("Catégorie n°"+ str(ctgr) +" / "+str(nb_categories))
        ctgr+=1

        #Ecriture des en-têtes
        with open(str(category_name)+"_Books_Information.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";") 
            writer.writerows([header])

        #Lecture du nombre de page
        results=soup.find('li',attrs={'next'})

        if results==None:
            nb_pages=1
        else:
            pages=soup.find('li', attrs={'current'})
            nb_pages_str=str(pages.text)
            position=nb_pages_str.find("P")
            nb_pages=int(nb_pages_str[position+10:])

        for page in range (1,nb_pages+1):
            if nb_pages==1:
                url_page=category_base_url
            else:
                url_page=category_base_url + "page-" + str(page) +".html"

            print("URL : ", url_page)
            print("PAGE", str(page) + " / " + str(nb_pages)+"\n")

            req=requests.get(url_page)
            soup = BeautifulSoup(req.content, "html.parser")
            articles=soup.find_all("h3")
            
            for article in articles:
                books=article.find_all("a")
                                 
                for book in books:
                    book_link=book.get("href")
                    book_url=catalogue_url+str(book_link)[9:]
                    req = requests.get(book_url)
                    soup = BeautifulSoup(req.content, "html.parser")

                    #Product_page_url
                    datas[0]=book_url

                    #universal_product_code (upc)
                    upc=soup.tr.td
                    datas[1]=upc.text

                    #Title
                    title=soup.h1
                    datas[2]=title.text

                    #prices
                    tables=soup.findChildren('table')
                    my_table = tables[0]
                    rows = my_table.findChildren(['tr'])
                    t=['']*len(rows)

                    i=0
                    for row in rows:  
                        cells = row.find('td')
                        t[i]=cells.text
                        i=i+1

                    datas[3]=t[3]
                    datas[4]=t[2]
                    datas[5]=t[6]

                    #product_description
                    product_description=soup.findChildren('p')
                    pd=product_description[3]
                    reg_pd=re.sub('[^A-Za-z0-9,.!? ]+', " ",pd.text)
                    datas[6]=reg_pd

                    #Category
                    category=soup.findChildren('a')
                    ct=category[3]
                    datas[7]=ct.text

                    #Review Rating
                    rating=soup.find_all('p')
                    star=rating[2].get("class")
                    star_rating=star[1]

                    if star_rating=='One':
                        ratings="'1"+ " / 5'"
                    elif star_rating=='Two':
                        ratings="'2 "+ "/5'"
                    elif star_rating=='Three':
                        ratings="'3"+ "/ 5'"
                    elif star_rating=='Four':
                        ratings="'4"+ "/ 5'"
                    else:
                        ratings="'5"+ "/ 5'"

                    datas[8]=ratings

                    #Image URL
                    img_url=soup.find('img').get("src")
                    img_url_str=site_url + str(img_url)[6:]
                    """print("image url",img_url_str)"""
                    datas[9]=img_url_str
                    
                    with open(str(category_name)+"_Books_Information.csv", "a", newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=";")
                        writer.writerows([datas])

                    #Téléchargement du fichier image#
                    response=requests.get(img_url_str)
                    raw_reg_title=re.sub('[^A-Za-z0-9!# ]+', " ",title.text)
                    reg_title=raw_reg_title[:64]
                    if response.status_code == 200:
                        with open(str(reg_title)+".jpg","wb") as f:
                            f.write(response.content)
