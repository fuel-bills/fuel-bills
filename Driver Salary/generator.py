import datetime
import os
import shutil
import uuid

import img2pdf

import requests
from PIL import Image
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


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def merge_3_images(path1, path2, path3, output_path):
    # Load the images
    image1 = Image.open(path1)
    image2 = Image.open(path2)
    image3 = Image.open(path3)

    # Get the width and height of each image
    width1, height1 = image1.size
    width2, height2 = image2.size
    width3, height3 = image3.size

    # Get the total width and height of the merged image
    total_width = width1 + width2 + width3
    total_height = max(height1, height2, height3)

    # Create a new image
    new_image = Image.new("RGB", (total_width, total_height))

    # Paste the images onto the new image
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (width1, 0))
    new_image.paste(image3, (width1 + width2, 0))

    # Save the new image
    new_image.save(output_path)


def open_browser():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=540,960")
    driver = webdriver.Chrome(options=options)
    return driver


browser = open_browser()


def save_pdf(url, filepath):
    browser.get(url)
    browser.save_screenshot(filepath)


os.mkdir('generated')

images = []

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
    images.append(filepath)

split = split_list(images, wanted_parts=4)
merged_images = []

for images in split:
    path = f"generated/{uuid.uuid4()}.png"
    merge_3_images(images[0],images[1],images[2], path)
    merged_images.append(path)

pdf_file = img2pdf.convert(merged_images)

# Save the PDF file to the desired location
with open('output.pdf', 'wb') as f:
    f.write(pdf_file)

shutil.rmtree('generated')
