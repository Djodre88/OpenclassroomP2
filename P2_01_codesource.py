import requests
from bs4 import BeautifulSoup
import csv
import re

header=['product_page_url','universal_product_code(upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
l=len(header)
datas=['']*l

site_url="https://books.toscrape.com/"                    
                    
                   
book_url='https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'