from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from lxml import html
import smtplib
import codecs
import time
import csv

count = 0
price_list = []

urls = [
    "https://www.amazon.de/dp/B08237CW9N"
]


def check_price(url):
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
    return str(price), item


def send_email(reason, message):
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("derking6263@gmail.com", password)
    s.sendmail("derking6263@gmail.com", "omegagaming189@gmail.com", message)
    s.quit()


def price_decrease_check(price_list):
    if price_list[-1] < price_list[-2]:
        return True, price_list[-1], price_list[-2]
    else:
        return False, None, None


def log(item, price, decrease, bigger):
    try:
        ctime = str(time.strftime('%H:%M'))
        bigger = str(bigger) + "€"
        cprice = str(price) + "€"
        decrease = "-" + str(decrease) + "€"

        log = ctime, item, bigger, cprice, decrease
        fields = ["time", "item", "price", "decrease", "bigger"]
        rows = [[ctime, item, price, decrease, bigger]]

        with open("price-tracker-log.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(rows)

        print(log)
    except Exception as e:
        print("Unable to log data, " + e)


def main(url):
    try:
        global count
        cprice, citem = check_price(url)

        if count > 1:
            flag, smaller, bigger = price_decrease_check(price_list)

            if flag:
                if smaller != None and bigger != None:
                    decrease = float(bigger) - float(smaller)

                    message = "The price of '" + \
                        str(citem) + "' (" + url + ") has decreased by: " + \
                        str(decrease.__round__()) + "€"
                    send_email("Price decrase of " + str(citem), message)

                    log(citem, cprice, decrease, bigger)

        count += 1
    except Exception as e:
        print(e)


while 1:
    for i, url in enumerate(urls):
        i = i+1
        main(url)
        print(f"[{i}]\n\n\n")
    time.sleep(86400/2)
