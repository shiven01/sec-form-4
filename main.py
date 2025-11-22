import requests
from bs4 import BeautifulSoup

url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=11/01/2023+-+11/01/2024&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the data table (the one with thead and many rows)
tables = soup.find_all('table')
data_table = next((t for t in tables if t.find('thead') and len(t.find_all('tr')) > 10), None)

# Extract headers
headers = [th.text.strip() for th in data_table.find('thead').find_all('th')]

# Extract rows
rows = []
tbody = data_table.find('tbody')
trs = tbody.find_all('tr') if tbody else data_table.find_all('tr')[1:]  # Skip header row if no tbody
for tr in trs:
    rows.append([td.text.strip() for td in tr.find_all('td')])

# Write to TSV file
with open('data.tsv', 'w', encoding='utf-8') as f:
    f.write('\t'.join(headers) + '\n')
    for row in rows:
        f.write('\t'.join(row) + '\n')

print(f"Saved {len(rows)} rows to data.tsv")
