import requests
from bs4 import BeautifulSoup
import csv
import re

header=['product_page_url','universal_product_code(upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
l=len(header)
datas=['']*l

site_url="https://books.toscrape.com/"               
                    
book_url='https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

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
datas[6]=pd.text

#Category
category=soup.findChildren('a')
ct=category[3]
datas[7]=ct.text