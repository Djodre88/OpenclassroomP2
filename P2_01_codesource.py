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
img_url_str=site_url + str(img_url)[5:]
datas[9]=img_url_str

reg_title=re.sub(r'[?|:|.|!|*]',"",title.text)

with open(str(reg_title)+"_Book_Information.csv", "a", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerows([header])
    writer.writerows([datas])