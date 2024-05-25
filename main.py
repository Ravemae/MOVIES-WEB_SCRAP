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
    
def data_exists(movie_title, date):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM International WHERE movie_name=? AND date=?", (movie_title, date))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0
    
def insert_data(movie_title, date, url_2, desc, download, image):
    if not data_exists(movie_title, date):
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO International (movie_name, date, link, Description, Download_link, img) VALUES(?, ?, ?, ?, ?, ?)", (movie_title, date, url_2, str(desc), download, image))
        conn.commit()
        conn.close()
        return "Data inserted"


url = "https://nkiri.com/category/international/"
n = range(1, 80)
for num in n:
    url = f'{url}page/{num}'
    print(f"Getting data for page {num}")
    if num == 79:
        print("Successfully added into Database!")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for movie in soup.find_all('article'):
        # Movie Name
        movie_title = movie.find('h2', {'class': "blog-entry-title entry-title"})
        if movie_title:
            name = movie_title.text.strip()
        else:
            print("Movie title not found, skipping...")
            continue
        
        # Date
        date = movie.find('div', {'class': 'blog-entry-date clr'})
        if date:
            f_date = date.text.strip()
        else:
            print("Date not found for movie, skipping...")
            continue
        
        # Image
        img = movie.find('img')
        if img:
            image = img.get('src')
        else:
            print("Image not found for movie, skipping...")
            continue
        
        # Link 2
        link = movie.find('a')
        if link:
            url_2 = link.get('href')
        else:
            print("Link not found for movie, skipping...")
            continue
        
        p_response = requests.get(url_2)
        p_soup = BeautifulSoup(p_response.text, 'html.parser') 
        for x in p_soup.find_all('a', {'class': "elementor-button elementor-button-link elementor-size-md"}):
            download = x.get('href')
            if 'html' in download:
                Download_link = download
            if not Download_link:
                print("Download link not found for movie, skipping...")
                continue
        
        for item in p_soup.find_all('div', {'class': 'overview'}):
            'Description'
            desc = item.find('p')
            desc_text = desc.text.strip()  
            print('\n')
            
                    
            create_database()
            insert_data(name, f_date, url_2, desc, Download_link, image)
            print(f"Inserted data for movie: {name}")
            
            
            if num == 79:
                print("Successfully added into Database!")