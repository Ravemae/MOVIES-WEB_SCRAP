import requests
from bs4 import BeautifulSoup
url ='https://www.awafim.tv/browse?q=&type=series&genre%5B%5D=Crime&genre%5B%5D=Drama&country%5B%5D=GBR&country%5B%5D=USA'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
for data in soup.find_all('article',{'class': 'titles-one'}):
    head = data.find('h3', {'class': 'to-h3'})
    print(head.text.strip())
    date = data.find('div', {'class': 'toi-year'})
    print(date.text.strip())
    season = data.find('div',{'class': 'toi-run'})
    print(season.text.strip())
    link = data.find('a')['href']
    print(link)
    country = data.find('div', {'class': 'toi-countries'})
    print(country.find('i')['class'][0])
    image = data.find('img',{'class': 'to-thumb'})
    print(image.get('src'))
    rating = data.find('span', {'class':'stars-list'})
    print(rating.get('title'))
    
import requests
from bs4 import BeautifulSoup
import os
import sqlite3
url ='https://www.awafim.tv/browse?q=&type=series&genre%5B%5D=Crime&genre%5B%5D=Drama&country%5B%5D=GBR&country%5B%5D=USA'
def init_database():
   
        connection = sqlite3.connect('movies.db')
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS action_and_drama(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_title text,
        date text,
        season text,              
        link text,
        country text,
        image text,
        rating
                                                                         
)""")
        connection.commit()
        connection.close()

def add_data(title, date,season, link, country, image, rating):
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO action_and_drama (
                   movie_title,
                   date,
                   season,
                   link,
                   country,
                    image,
                    rating) VALUES (?, ?, ? ,? ,? ,? ,? )"""
                   , (title, date,season, link, country, image, rating))
    connection.commit()
    connection.close()

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
for data in soup.find_all('article',{'class': 'titles-one'}):
    head = data.find('h3', {'class': 'to-h3'})
    f_head = head.text.strip()
    date = data.find('div', {'class': 'toi-year'})
    f_date = date.text.strip()
    season = data.find('div',{'class': 'toi-run'})
    f_season =season.text.strip()
    link = data.find('a')['href']
    
    country = data.find('div', {'class': 'toi-countries'})
    f_country = country.find('i')['class'][0]
    image = data.find('img',{'class': 'to-thumb'})
    f_image = image.get('src')
    rating = data.find('span', {'class':'stars-list'})
    f_rating = rating.get('title')
    init_database()
    add_data = (f_head, f_date, f_season, link, f_country, f_image,f_rating)