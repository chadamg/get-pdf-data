from datetime import datetime, date
from tabula import read_pdf
from bs4 import BeautifulSoup
from requests import get
from io import BytesIO

pdf_url = ""

# get html page from url
url = "https://owma.org.uk/salaah-times/"
reqs = get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(reqs.text, "html.parser")

# find pdf links on html page
for link in soup.find_all(
    "a", {"class": "elementor-button-link elementor-button elementor-size-sm"}
):
    pdf_link = link.get("href")

    # save pdf link for current month only
    if int(pdf_link.split("/")[6]) == date.today().month:
        pdf_url += pdf_link

# print pdf name
# print(url.split('/')[7].split('.')[0])

# get binary pdf data from url and store as bytes object
req = get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
f = BytesIO(req.content)

# get table from pdf data
df = read_pdf(f, lattice=True, pages="all")[0]

# get multiple tables
# df = read_pdf(f, lattice=True, pages='all', area=[[114.904045, 42.68114, 581.4778, 248], [114.904045, 290.61353, 581.4778, 442.82587]])
# full table , area=(114.904045, 42.68114, 581.4778, 442.82587)
# left table , area=(114.904045, 42.68114, 581.4778, 248)
# right table , area=(114.904045, 290.61353, 581.4778, 442.82587)

# get todays prayer times from table
# fajr, sunrise, dhuhr, asr, isha, maghrib = df.iloc[
#     date.today().day, [0, 1, 3, 4, 5, 11]
# ]

x = df.iloc[1:, [0, 1, 3, 4, 5, 11]]
x.columns = [
    "Fajr",
    "Sunrise",
    "Dhuhr",
    "Asr",
    "Isha",
    "Maghrib",
]
x.to_json("data.json", orient='records', indent=2)

# fajr = "0"+fajr
# sunrise = "0"+sunrise
# if not dhuhr.split(':')[0]=='12':
#     dhuhr = str(int(dhuhr.split(':')[0])+12)+':'+dhuhr.split(':')[1]
# asr = str(int(asr.split(':')[0])+12)+':'+asr.split(':')[1]
# isha = str(int(isha.split(':')[0])+12)+':'+isha.split(':')[1]
# maghrib = str(int(maghrib.split(':')[0])+12)+':'+maghrib.split(':')[1]
#
# if datetime.now().hour >= int(isha.split(':')[0]) and datetime.now().minute >= int(isha.split(':')[1]):
#     fajr = df.iloc[date.today().day+1, [0]]
#     fajr = "0"+fajr

# print(fajr, sunrise, dhuhr, asr, maghrib, isha)


import re
from datetime import datetime
x = 'https://owma.org.uk/wp-content/uploads/2021/06/Jul2021.pdf'
y = x.split('/')[7]
# date.today().month
months = ['Jan', 'Feb', 'Mar', 'March', 'Apr', 'April', 'May', 'Jun', 'June', 'Jul', 'July', 'Aug', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec']
for month in months:
    if month in y and month in datetime.now().strftime('%B'):
        print(month)


import json
items=soup.select('div[class="masjidnow-container"]')

def format_time(prayer):
    in_time = datetime.strptime(prayer, "%I:%M%p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

for item in items:
    data = json.loads(item['data-masjidnow-masjid'])
    month_data = data['salah_timings']
    today_data = month_data[date.today().day-1]
    fajr = format_time(today_data['salah_timing']['fajr_adhan'])
    sunrise = format_time(today_data['salah_timing']['sunrise_adhan'])
    dhuhr = format_time(today_data['salah_timing']['dhuhr_adhan'])
    asr = format_time(today_data['salah_timing']['asr_adhan'])
    maghrib = format_time(today_data['salah_timing']['maghrib_adhan'])
    isha = format_time(today_data['salah_timing']['isha_adhan'])
    print(fajr, sunrise, dhuhr, asr, maghrib, isha)