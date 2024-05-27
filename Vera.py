import sqlite3
import requests
from bs4 import BeautifulSoup

def create_database():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS International (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_name TEXT,
                    date Text,
                    link TEXT,
                    Description TEXT,
                    Download_link TEXT,
                    img TEXT)''')
    conn.commit()
    conn.close()
    
def data_exists(title, date):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM International WHERE movie_name=? AND date=?", (title, date))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0
    
def insert_data(title, date, link, desc, download, image):
    if not data_exists(title, date):
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO International (movie_name, date, link, Description, Download_link, img) VALUES(?, ?, ?, ?, ?, ?)", (title, date, link, str(desc), download, image))
        conn.commit()
        conn.close()
        return "Data inserted"

base_url = "https://nkiri.com/category/international/"
n = range(1, 80)
for num in n:
    url = f'{base_url}page/{num}'
    print(f"Getting data for page {num}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for movie in soup.find_all('article'):
        # Movie Name
        title = movie.find('h2', {'class': "blog-entry-title entry-title"})
        if title:
            name = title.text.strip()
        
        # Date
        date = movie.find('div', {'class': 'blog-entry-date clr'})
        if date:
            f_date = date.text.strip()
        
        # Image
        img = movie.find('img')
        if img:
            image = img.get('src')
        
        # Link 2
        link = movie.find('a')['href']
            
        p_response = requests.get(link)
        p_soup = BeautifulSoup(p_response.text, 'html.parser') 
        for x in p_soup.find_all('a', {'class': "elementor-button elementor-button-link elementor-size-md"}):
            download = x.get('href')
            if 'html' in download:
                Download_link = download
        
        for item in p_soup.find_all('div', {'class': 'overview'}):
            # Description
            desc = item.find('p')
            if desc:
                desc_text = desc.text.strip()
                
                create_database()
                insert_data(name, f_date, link, desc_text, Download_link, image)
                print(f"Inserted data for movie: {name}")
if num == 79:
    print("Successfully added into Database!:)")

            