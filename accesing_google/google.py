import requests # it is used for making http request like fetching a website 
from bs4 import BeautifulSoup  #it is for parsing and extracting data from html or xml websites
import pandas as pd




url="https://books.toscrape.com/"
result = requests.get(url)


#to make sure that the we accesed the website we are going to run the status code 200 which means ok 


print (result.status_code)

src = result.content # we store the whole content here 

soup=BeautifulSoup(src,'html.parser') #allows us to extract a specific type of information 


book = soup.find_all("article")
books=[]
for find_book in  book:
    title=find_book.h3.a["title"]
    price=find_book.find("p",class_="price_color").text
    rating_p_tag=find_book.p
    rating_classes=rating_p_tag["class"][1]
    all_books={
        "title":title,
        "price" :price,
        "rating_classes":rating_classes

    }
    books.append(all_books)

print(books[1])

df = pd.DataFrame(books)

# Convert to DataFrame and save
df = pd.DataFrame(books)


df = pd.DataFrame(books)

# Just save as CSV - no extra library needed!
df.to_csv('books.csv', index=False)

print(f"✓ Saved {len(df)} books to books.csv!")
