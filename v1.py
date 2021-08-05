from fastapi import FastAPI
from datetime import datetime, date
from tabula import read_pdf
from bs4 import BeautifulSoup
from requests import get
from io import BytesIO

app = FastAPI()


@app.get("/")
def get_pdf_data():

    pdf_url = ""
    months = [
        "Jan",
        "Feb",
        "Mar",
        "March",
        "Apr",
        "April",
        "May",
        "Jun",
        "June",
        "Jul",
        "July",
        "Aug",
        "Sep",
        "Sept",
        "Oct",
        "Nov",
        "Dec",
    ]

    # get html page from url
    url = "https://owma.org.uk/salaah-times/"
    reqs = get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(reqs.text, "html.parser")

    # find pdf links on html page
    for link in soup.find_all(
        "a", {"class": "elementor-button-link elementor-button elementor-size-sm"}
    ):
        pdf_link = link.get("href")
        y = pdf_link.split("/")[7]

        # save pdf link for current month only
        for month in months:
            if month in y and month in datetime.now().strftime("%B"):
                pdf_url += pdf_link

    # get binary pdf data from url and store as bytes object
    req = get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
    f = BytesIO(req.content)

    # get table from pdf data
    df = read_pdf(f, lattice=True, pages="all")[0]

    # get todays prayer times from table
    fajr, sunrise, dhuhr, asr, isha, maghrib = df.iloc[
        date.today().day, [0, 1, 3, 4, 5, 11]
    ]

    # convert time to 24hr time
    fajr = "0" + fajr
    sunrise = "0" + sunrise
    if not dhuhr.split(":")[0] == "12":
        dhuhr = str(int(dhuhr.split(":")[0]) + 12) + ":" + dhuhr.split(":")[1]
    asr = str(int(asr.split(":")[0]) + 12) + ":" + asr.split(":")[1]
    isha = str(int(isha.split(":")[0]) + 12) + ":" + isha.split(":")[1]
    maghrib = str(int(maghrib.split(":")[0]) + 12) + ":" + maghrib.split(":")[1]

    # return tomorrow data for fajr if current time is isha
    if datetime.now().hour >= int(isha.split(":")[0]) and datetime.now().minute >= int(
        isha.split(":")[1]
    ):
        fajr = df.iloc[date.today().day + 1, 0]
        fajr = "0" + fajr

    # return yesterday data for isha if current time is past midnight
    if datetime.now().hour <= int(fajr.split(":")[0]) and datetime.now().minute < int(
        fajr.split(":")[1]
    ):
        isha = df.iloc[date.today().day - 1, 5]
        isha = str(int(isha.split(":")[0]) + 12) + ":" + isha.split(":")[1]

    return {
        "Fajr": fajr,
        "Sunrise": sunrise,
        "Dhuhr": dhuhr,
        "Asr": asr,
        "Maghrib": maghrib,
        "Isha": isha,
    }
