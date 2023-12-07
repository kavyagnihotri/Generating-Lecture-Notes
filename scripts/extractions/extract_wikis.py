import requests
from bs4 import BeautifulSoup

def all_links(soup):
    tags = soup.find_all('a')
    for tag in tags:
        if tag.get('href') != '':
            print(tag.get_text())

def headings(soup):
    bolds = soup.find_all('b')
    for b in bolds:
        tags = b.find_all('a')
        for tag in tags:
            if tag.get('href') != '':
                print(tag.get_text())

def sub_headings(soup):
    # divs = soup.find_all('div')
    # for div in divs:
        lists = soup.find_all('li')
        for li in lists:
            tags = li.find_all('a')
            for tag in tags:
                if tag.get('href') != '':
                    print(tag.get_text())

def main():
    wiki_url = "https://en.wikipedia.org/wiki/Wikipedia:Contents/Categories"
    response = requests.get(wiki_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    # headings(soup)
    sub_headings(soup)

if __name__ == '__main__':
    main()