###This was the first attempt at scraping the website https://nwccu.org/member-institutions/directory/
###This attempt tried to use BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc/
###This attempt didn't work. BeautifulSoup doesn't work well with data that comes from Javascript, which the aforementioned URL does
import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to scrape data
def scrape_colleges():
    url = "https://nwccu.org/member-institutions/directory/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    colleges = soup.find_all("a", class_="show-more")

    data = []
    for college in colleges:
        name = college.text.strip()
        data.append(name)
    
    return data

# Function to store data in a SQLite database
def store_data(data):
    conn = sqlite3.connect('colleges.db')
    c = conn.cursor()

    # Create table (if not exists)
    c.execute('''CREATE TABLE IF NOT EXISTS colleges (name TEXT)''')

    # Insert data and display each name
    for name in data:
        print(f"Inserting: {name}")
        c.execute("INSERT INTO colleges (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()

# Function to display all stored data
def display_stored_data():
    conn = sqlite3.connect('colleges.db')
    c = conn.cursor()

    # Query all data
    c.execute("SELECT * FROM colleges")
    rows = c.fetchall()

    # Display each row
    print("\nStored College Data:")
    for row in rows:
        print(row[0])

    conn.close()

# Main script
if __name__ == "__main__":
    college_data = scrape_colleges()
    store_data(college_data)
    display_stored_data()
    input("Press Enter to exit...")  # This line keeps the window open
