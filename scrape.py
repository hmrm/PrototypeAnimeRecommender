from bs4 import BeautifulSoup

html_doc = open("html_doc", "r").read()

soup = BeautifulSoup(html_doc)

for text in soup.find_all('table'):
    print text
    for link in text.find_all('a'):
        print link.get_text()
