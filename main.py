from fastapi import FastAPI
from datetime import datetime, date
from bs4 import BeautifulSoup
from requests import get
import json

app = FastAPI()


@app.get("/")
def get_pdf_data():

    # function that converts HH:MMam/pm to 24hr time HH:MM
    def format_time(prayer):
        in_time = datetime.strptime(prayer, "%I:%M%p")
        out_time = datetime.strftime(in_time, "%H:%M")
        return out_time

    # get html page from url
    url = "https://owma.org.uk/"
    reqs = get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(reqs.text, "html.parser")

    # find div with data on html page
    items = soup.select('div[class="masjidnow-container"]')

    for item in items:
        # get string data of attribute value from div
        div_attribute_value = item["data-masjidnow-masjid"]

        # convert string representation of dict to dict
        data = json.loads(div_attribute_value)

        # access monthly and daily data from dict
        month_data = data["salah_timings"]
        today_data = month_data[date.today().day - 1]

        fajr = format_time(today_data["salah_timing"]["fajr_adhan"])
        sunrise = format_time(today_data["salah_timing"]["sunrise_adhan"])
        dhuhr = format_time(today_data["salah_timing"]["dhuhr_adhan"])
        asr = format_time(today_data["salah_timing"]["asr_adhan"])
        maghrib = format_time(today_data["salah_timing"]["maghrib_adhan"])
        isha = format_time(today_data["salah_timing"]["isha_adhan"])

    # return tomorrow data for fajr if current time is isha
    if datetime.now().hour >= int(isha.split(":")[0]) and datetime.now().minute >= int(
        isha.split(":")[1]
    ):
        tomorrow_data = month_data[date.today().day]
        fajr = format_time(tomorrow_data["salah_timing"]["fajr_adhan"])

    # return yesterday data for isha if current time is past midnight
    if datetime.now().hour <= int(fajr.split(":")[0]) and datetime.now().minute < int(
        fajr.split(":")[1]
    ):
        yesterday_data = month_data[date.today().day - 2]
        isha = format_time(yesterday_data["salah_timing"]["isha_adhan"])

    return {
        "Fajr": fajr,
        "Sunrise": sunrise,
        "Dhuhr": dhuhr,
        "Asr": asr,
        "Maghrib": maghrib,
        "Isha": isha,
    }
