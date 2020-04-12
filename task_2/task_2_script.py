import requests as rq
from bs4 import BeautifulSoup
import pandas as pd


list_url = 'https://icobench.com/ieo'
data_with_list = rq.get(list_url)
list_soup = BeautifulSoup(data_with_list.text)

# Expected number of companies
companies = list_soup.findAll('a', {'class': 'name notranslate'})
print('Expected number of companies: ', len(companies))

# Function for processing contacts data
def get_data(t):
    soup = BeautifulSoup(t)
    data = soup.findAll('a', {'class': ['www', 'twitter', 'facebook', 'telegram']})
    res = {}
    for tag in data:
        if isinstance(tag.contents, list) and len(tag.contents) == 1 and \
            isinstance(tag.contents[0], str) and \
            tag.contents[0].strip() in ('Twitter', 'Facebook', 'Telegram', 'WWW'):
            res[tag['class'][0].strip()] = tag['href']
    return res

# A cycle, that downloads the needed information
data = []
cnt = 0
for company_tag in companies:
    company_url = 'https://icobench.com' + company_tag['href']
    t = rq.get(company_url).text
    dct = get_data(t)
    dct['name'] = company_tag.contents[0].strip()
    data.append(dct)
    cnt += 1
    if cnt % 10 == 0:
        print(f'{cnt} companies have been processed')
print(f'All {cnt} companies have been processed')

# Transform data to a pandas dataframe
columns = ('name', 'www', 'facebook', 'telegram', 'twitter')
df = pd.DataFrame(data, columns=columns).fillna('').rename(columns={'www': 'website'})

# Output the results in a csv-file, if you want to
df.to_csv('companies.csv', sep=';')