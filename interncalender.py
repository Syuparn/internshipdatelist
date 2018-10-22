import re
import sys
from time import sleep
import urllib
import pandas as pd
from bs4 import BeautifulSoup

#TODO; なんかzipかみ合ってない気がする(deadlineが１記事に１つしかないから？)

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

    # list of internship divs
    internDivs = soup.div(class_='ts-p-_internshipList-item-info')
    prefix = 'ts-p-_internshipList-item-info-row-'
    titleClassName = prefix + 'title'
    daysClassName = ' '.join([prefix+'detail-text', prefix+'detail-text_day'])
    dateClassName = ' '.join([prefix+'detail-text', prefix+'detail-text_place'])

    # list of deadline divs
    deadlineDivs = soup.div(class_='ts-p-_internshipList-item-entry js-p-entryItem-empty')
    deadlineClassName = 'ts-p-_internshipList-item-entry-deadline'

    for iDiv, dDiv in zip(internDivs, deadlineDivs):
        intern = {'company': pageDict['company'],
                  'title': iDiv.div()[0].text,
                  'days': iDiv.find_all('div', class_=daysClassName)[0].text,
                  'date': iDiv.find_all('div', class_=dateClassName)[0].text}
        intern['deadline'] = re.sub(
            'エントリー締切：', '', dDiv.find_all('div', class_=deadlineClassName)[0].text)
        interns.append(intern)

    return interns


def to_internship_url(companyUrl, urlPattern=re.compile(r'\?clk=.*')):
    # change url of each company page to that of its internship page
    # '.../?clk=...' to '.../internship/'
    internshipUrl = urlPattern.sub('internship/', companyUrl)
    # return full-path url
    return 'https://job.rikunabi.com' + internshipUrl


if __name__ == '__main__':
    htmlName = sys.argv[1] if len(sys.argv) > 1 else 'rikunabi.html'

    # read page of my favorite company list (already downloaded to local)
    with open(htmlName, 'r', encoding='utf-8') as f:
        html = f.read()

    # pick up urls of each favorite company
    pages = parse_company_urls(html)
    internPages = [{'company': page['company'],
                    'url': to_internship_url(page['url'])} 
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
