from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from lxml import html
import smtplib
import time
import json
import csv


count = 0
price_list = []

urls = [
    "https://www.amazon.de/dp/B08237CW9N",  # Screen
    "https://www.amazon.com/dp/B08Y8QY5NS"  # Keyboard
]


with open("./config.json", "r") as f:
    data = json.load(f)
    password = data["gmail"]["password"]
    email = data["gmail"]["email"]
    recv = data["options"]["recever"]
    timeout = data["options"]["timeout"]


def check_price(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(
            "C:/Users/Sandbox/Downloads/chromedriver.exe", chrome_options=options)
        driver.get(url)

        tree = html.fromstring(driver.page_source)
        item = tree.xpath(
            '//span[@class="a-size-large product-title-word-break"]/text()')
        price = tree.xpath('//span[@class="a-offscreen"]/text()')
        price = str(price[0]).replace(",", ".").replace("€", "")

        price_list.append(str(price))
        return None, str(price), item
    except Exception as e:
        return e, None, None


def send_email(message):
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(email, password)
        s.sendmail(email, recv, message)
        s.quit()
        return None
    except Exception as e:
        return e


def price_decrease_check(price_list):
    try:
        if price_list[-1] < price_list[-2]:
            return True, price_list[-1], price_list[-2]
        else:
            return False, None, None
    except Exception as e:
        return e, None, None


def log(item, price, decrease, bigger) -> str:
    try:
        ctime = str(time.strftime('%Y-%m-%d'))
        bigger = str(bigger) + "€"
        cprice = str(price) + "€"
        decrease = "-" + str(decrease) + "€"

        log = ctime, item, cprice, decrease, bigger
        fields = ["time", "item", "price", "decrease", "bigger"]
        rows = [[ctime, item, price, decrease, bigger]]

        with open(f"{item}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(rows)

        print(log)
        return None
    except Exception as e:
        return "Unable to log data, " + e


def main(url):
    try:
        global count
        err, cprice, citem = check_price(url)
        if err != None:
            print(err)

        if count > 1:
            flag, smaller, bigger = price_decrease_check(price_list)
            if flag != True and flag != False:
                print(flag)

            if flag:
                if smaller != None and bigger != None:
                    decrease = float(bigger) - float(smaller)

                    message = "The price of '" + \
                        str(citem) + "' (" + url + ") has decreased by: " + \
                        str(decrease.__round__()) + "€"
                    # "Price decrase of " + str(citem)
                    err = send_email(message)
                    if err != None:
                        print(err)

                    err = log(citem, cprice, decrease, bigger)
                    if err != None:
                        print(err)
        count += 1
    except Exception as e:
        return e


while 1:
    h = time.strftime("%h:%m")

    if h == "12:00" or h == "0:00":
        for i, url in enumerate(urls):
            i = i+1
            main(url)
            print(f"[{i}]\n\n\n")
    time.sleep(60*5)
