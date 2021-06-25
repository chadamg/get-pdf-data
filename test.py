from datetime import datetime, date
from tabula import read_pdf
from bs4 import BeautifulSoup
from requests import get
from io import BytesIO

pdf_url = ""

# get html page from url
url = 'https://owma.org.uk/salaah-times/'
reqs = get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(reqs.text, 'html.parser')

# find pdf links on html page
for link in soup.find_all('a', {'class': 'elementor-button-link elementor-button elementor-size-sm'}):
    pdf_link = link.get('href')

    # save pdf link for current month only
    if pdf_link.split('-')[1].split('/')[4] == datetime.now().strftime('%B'):
        pdf_url += pdf_link

# print pdf name
# print(url.split('/')[7].split('.')[0])

# get binary pdf data from url and store as bytes object
req = get(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
f = BytesIO(req.content)

# get table from pdf data
df = read_pdf(f, lattice=True, pages='all')[0]

# get multiple tables
# df = read_pdf(f, lattice=True, pages='all', area=[[114.904045, 42.68114, 581.4778, 248], [114.904045, 290.61353, 581.4778, 442.82587]])
# full table , area=(114.904045, 42.68114, 581.4778, 442.82587)
# left table , area=(114.904045, 42.68114, 581.4778, 248)
# right table , area=(114.904045, 290.61353, 581.4778, 442.82587)

# get todays prayer times from table
fajr, sunrise, dhuhr, asr, isha, maghrib = df.iloc[date.today().day, [
    0, 1, 3, 4, 5, 11]]
print(fajr, sunrise, dhuhr, asr, maghrib, isha)
