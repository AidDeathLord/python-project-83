from bs4 import BeautifulSoup


def parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    content = soup.find('meta', attrs={'name': "description"})
    content = content['content'] if content else ''
    return str(h1), str(title), str(content)
