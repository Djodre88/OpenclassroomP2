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