from bs4 import BeautifulSoup
import sys

html_doc = sys.stdin.read()

soup = BeautifulSoup(html_doc)

for text in soup.find_all('table'):
    for link in text.find_all('a'):
        print link.get_text()
