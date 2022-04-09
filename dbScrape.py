import sqlite3
from sqlite3 import Error
from mainScrape import Listing

test_listing = [
    ("Developer", "REDspace", "Remote", "2022-03-09", "https://www.google.ca", False, False),
    ("Assistant", "Curry's", "North Sydney, NS", "2022-04-02", "https://www.google.ca", False, False),
]

conn = None
try:
    conn = sqlite3.connect('favourites.db')
except Error as e:
    print(e)
    
    
cursor = conn.cursor()
conn.execute("create table if not exists favourites(title, company, location, date, link, keyworded, featured)")

def add_listing(title,company,location,date,link,keyworded,featured):
    listing = (title,company,location,date,link,int(keyworded),int(featured))
    conn.execute("insert into favourites(title, company, location, date, link, keyworded, featured)"
                 + " values (?, ?, ?, ?, ?, ?, ?)", listing)
    conn.commit()


def remove_listing(title,company,location,date,link,keyworded,featured):
    listing = (title,company,location,date,link,int(keyworded),int(featured))
    conn.execute("delete from favourites where title=? and company=? and location=? and date=?"
                 + " and link=? and keyworded=? and featured=?", listing)
    conn.commit()
    

def fetch_listings():
    arr_favs = []
    cursor.execute("select * from favourites")
    rows = cursor.fetchall()
    
    for row in rows:
        arr_favs.append(Listing(row[0],row[1],row[2],row[3],row[4],bool(row[5]),bool(row[6])))
        
    return arr_favs


def close_db():
    conn.close()
    
    
"""
conn.execute("delete from favourites")

conn.executemany("insert into favourites(title, company, location, date, link, keyworded, featured)"
                 + " values (?, ?, ?, ?, ?, ?, ?)", test_listing)

cursor.execute("select * from favourites")
rows = cursor.fetchall()
print(type(rows))

for row in rows:
    arr_favs.append(Listing(row[0],row[1],row[2],row[3],row[4],bool(row[5]),bool(row[6])))
    
"""
