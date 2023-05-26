from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from urllib.parse import urlparse, unquote

Header = ({'UserAgent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50", 'Accept-Language':"en-US,en;q=0.5"})
title = []
link_list = []
rating = []
price = []
review = []

URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
mainPage = requests.get(URL, headers=Header)
soup = BeautifulSoup(mainPage.content, 'html.parser')
links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
for link in links:
    linkToAppend = "https://www.amazon.in" + link.get('href')
    link_list.append(linkToAppend)
    path = urlparse(linkToAppend).path
    path_components = path.split('/')[1:]
    product_title = ''.join(unquote(path_components[0]))
    product_title = product_title.replace('-', ' ')
    title.append(product_title)
rating_a = soup.find_all("a", attrs={"href":"javascript:void(0)", "role":"button", "class":"a-popover-trigger a-declarative"})
for a in rating_a:
    rating_i = a.find("i",attrs={"class":"a-icon a-icon-star-small a-star-small-4 aok-align-bottom"})
    rating_div = a.find("span", attrs={"class":"a-icon-alt"})
    rating.append(rating_div.text.split(' ')[0])

price_a = soup.find_all("a", attrs={"class":"a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal"})
for a in price_a:
    price_span = a.find("span", attrs={"class":"a-price","data-a-size":"xl","data-a-color":"base"})
    price_tag = price_span.find("span", attrs={"class":"a-offscreen"})
    price_text = price_tag.text.strip()
    price_integer = ''.join(filter(str.isdigit, price_text))
    price.append(price_integer)

review_div = soup.find_all("div", attrs={"class":"a-row a-size-small"})
for a in review_div:
    review_spans = a.find("span", attrs={"class":"a-size-base s-underline-text"})
    review_text = review_spans.text.strip()
    review.append(review_text)


data = pd.DataFrame({'Title':title, 'Rating':rating, 'Link':link_list, 'Price(₹)':price, 'Number of Reviews':review})
data.to_csv('amazon.csv', index=False, encoding='utf-8')