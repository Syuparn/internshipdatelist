import re
from time import sleep
import urllib
import pandas as pd
from bs4 import BeautifulSoup


def parse_company_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = [{'company': div.a.text,'url': div.a.attrs['href']}
             for div in soup.div(class_='mp_cassette_title')]
    return pages


def fetch_intern_dates(pageDict):
    interns = []
    try:
        html = urllib.request.urlopen(url=pageDict['url'])
    except urllib.error.HTTPError as e:
        print(e)
        print('this company has no internship pages')
        # empty list
        return interns
    soup = BeautifulSoup(html, 'lxml')
    internDivs = soup.div(class_='ts-p-_internshipList-item-info')

    prefix = 'ts-p-_internshipList-item-info-row-'
    titleClassName = prefix + 'title'
    daysClassName = ' '.join([prefix+'detail-text', prefix+'detail-text_day'])
    dateClassName = ' '.join([prefix+'detail-text', prefix+'detail-text_place'])

    for div in internDivs:
        intern = {'company': pageDict['company'],
                  'title': div.div()[0].text,
                  'days': div.find_all('div', class_=daysClassName)[0].text,
                  'date': div.find_all('div', class_=dateClassName)[0].text}
        interns.append(intern)

    return interns


if __name__ == '__main__':
    htmlName = 'rikunabi.html'

    # read page of my favorite company list (already downloaded to local)
    with open(htmlName, 'r', encoding='utf-8') as f:
        html = f.read()

    # pick up urls of each favorite company
    pages = parse_company_urls(html)
    urlPattern = re.compile(r'\?clk=.*')
    # change each url to that of its internship page
    # '.../?clk=...' to '.../internship/'
    internPages = [{'company': page['company'],
                    'url': urlPattern.sub('internship/', page['url'])} 
                    for page in pages]

    # fetch dates of internships from each internship page
    interns = []
    for internPage in internPages:
        print(f"fetching {internPage['company']}...")
        interns.extend(fetch_intern_dates(internPage))
        # WARNING: DO NOT skip sleeping! (otherwise this causes DOS attack)
        sleep(2)

    df = pd.DataFrame(interns)
    print(df)
    df.to_csv('interndates.csv')
