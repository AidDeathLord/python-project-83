from bs4 import BeautifulSoup


def parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1').string
    if not h1:
        h1 = ''

    title = soup.title
    if not title:
        title = ''
    else:
        title = title.string

    content = soup.find('meta', attrs={'name': "description"})['content']
    if not content:
        content = ''
    return str(h1), str(title), str(content)
