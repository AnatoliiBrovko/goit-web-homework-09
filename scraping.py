import requests
from bs4 import BeautifulSoup
import json


def get_qoutes():

    qoutes = []
    for page in range(1,11):
        url = "https://quotes.toscrape.com/page/" + f"{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        for i in range(0, len(quotes)):
            tagsforquote = tags[i].find_all('a', class_='tag')
            taags = []
            for tagforquote in tagsforquote:
                taags.append(tagforquote.text)
            qoutes_dict = {"tags":taags, "author":authors[i].text, "quote":quotes[i].text}
            qoutes.append(qoutes_dict)
    return qoutes


def qoutes_json():

    qoutes = get_qoutes()
    with open('qoutes.json', "w", encoding='windows-1251', errors='replace') as fh:
        json.dump(qoutes, fh)
    print("'qoutes.json' created and written")


def normalize_author_page():

    author_pages = []
    for page in range(1,11):
        url_page = "https://quotes.toscrape.com/page/" + f"{page}/"
        response = requests.get(url_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes_div = soup.find_all('div', class_='quote')
        for div in quotes_div:
            author_page = "https://quotes.toscrape.com/" + div.find('a')['href']
            if author_page not in author_pages:
                author_pages.append(author_page)
    return author_pages


def get_authors():

    authors = []
    author_pages = normalize_author_page()
    for a_page in author_pages:
        response = requests.get(a_page)
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.find('h3', class_="author-title").get_text()
        bday = soup.find('span', class_="author-born-date").get_text()
        location = soup.find('span', class_="author-born-location").get_text()
        description = soup.find('div', class_="author-description").get_text().replace("\n", '').replace("        ", "")
        author_dict = {"fullname": name, "born_date": bday, "born_location": location, "description": description}
        authors.append(author_dict)
    return authors


def authors_json():

    authors = get_authors()
    with open('authors.json', "w", encoding='windows-1251', errors='replace') as fh:
        json.dump(authors, fh)
    print("'authors.json' created and written")


if __name__ == '__main__':
    qoutes_json()
    authors_json()