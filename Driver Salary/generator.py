import datetime
import os
import shutil
from base64 import b64decode

import requests
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

current_date = datetime.date.today()

start_date = datetime.date(current_date.year, 5, 1)
end_date = datetime.date(current_date.year + 1, 4, 30)

if current_date.month < 4:
    start_date = start_date.replace(year=start_date.year - 1)
    end_date = end_date.replace(year=end_date.year - 1)

print(start_date, end_date)


def open_browser():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=540,960")
    driver = webdriver.Chrome(options=options)
    return driver


browser = open_browser()


def save_pdf(url, filepath):
    browser.get(url)
    png = browser.execute("screenshot", {'--dpr': 100})['value']
    png = b64decode(png.encode("ascii"))
    try:
        with open(filepath, "wb") as f:
            f.write(png)
    except OSError:
        return False
    finally:
        del png
    return True


shutil.rmtree('generated')
os.mkdir('generated')

while start_date <= end_date:
    date = start_date + relativedelta(days=-1)
    data = {
        'amount': 10000,
        'employee_name': 'Dhaval Mehta',
        'driver_name': 'Ishit Shah',
        'vehicle_no': '22BH4296A',
        'month': date.strftime('%B'),
        'date': date.strftime('%d %b %Y'),
    }
    url = requests.get(f'http://127.0.0.1:9999/', params=data).url
    filepath = f"generated/Driver Salary Slip {date.strftime('%d-%m-%Y')}.png"
    save_pdf(url, filepath)
    start_date += relativedelta(months=1)
    break
