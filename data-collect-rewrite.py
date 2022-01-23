from msilib.schema import RemoveFile
import os
from typing_extensions import runtime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep, time
from lxml import html
import sys


def clean(file) -> None:
    with open(file, "r+", encoding="utf-8") as f:
        content = f.read()
        content_clean1 = content.replace("'", "")
        content_clean2 = content_clean1.replace(
            ", [],", ", ???,").replace("[],", "").replace("[]", "")
        content_clean3 = content_clean2.replace(" ???,  \n", "").replace(
            "\n\n\n\n\n\n", "\n\n---, New Search, Quarry, ---\n\n")

    with open("./cleancsv/clean-" + file.replace("./", "").replace("csv/", ""), "w+", encoding="utf-8") as f:
        f.write(content_clean3)


def fetch_urls(keywords, *args):
    lastTime = None
    for keyword in keywords:
        driver = webdriver.Chrome(options=options)
        keyword = keyword.replace("-", " ")

        for page_nb in range(1, 10):
            driver.get(f"https://www.amazon.com/s?k={keyword}&page={page_nb}")
            sleep(1)

            tree = html.fromstring(driver.page_source)
            for x, product_tree in enumerate(tree.xpath('//div[contains(@data-cel-widget, "search_result_")]')):
                title = product_tree.xpath(
                    './/span[@class="a-size-medium a-color-base a-text-normal"]/text()')
                reviews = product_tree.xpath(
                    './/span[@class="a-size-base"]/text()')
                price = product_tree.xpath(
                    './/span[@class="a-offscreen"]/text()')
                links = list(product_tree.iterlinks())
                try:
                    (_, _, link, _) = links[0]
                except:
                    link = None
                strLink = ("amazon.com/"+link) if not link == None else list()
                listLink = [strLink]
                link = (listLink if len(price) > 0 or len(title) > 0 else [])

                title = str(title[0]).replace(",", "") if len(
                    title) > 0 else str(title).replace(",", "")
                reviews = str(reviews[0]).replace(",", ".") if len(reviews) > 0 else str(
                    reviews).replace(",", ".")
                price = str(price[0]).replace("\xa0", "").replace(",", ".").replace("'", "") if len(price) > 0 else str(
                    price).replace(",", ".").replace("\xa0", "").replace("'", "")
                link = str(link[0]).replace("'", "") if len(
                    link) > 0 else str(link).replace("'", "")

                for word in keyword.split(" "):
                    if title.__contains__(word):
                        info = str((title, reviews, price, link)).replace(
                            "(", "").replace(")", "")
                        with open("./csv/data-{}.csv".format(keyword.replace(" ", "_").replace("-", "_")), "a", encoding="utf-8") as f:
                            f.write(str(info).replace(
                                "(", "").replace(")", "")+"\n")
        with open("./csv/data-{}.csv".format(keyword.replace(" ", "_")), "a", encoding="utf-8") as f:
            f.write("\n\n\n\n\n\n")

        driver.close()
        sleep(1)
        clean("./csv/data-{}.csv".format(keyword.replace(" ", "_")))
        runTime = time() - startTime
        print("Finished collecting \"{}\" data in {} Seconds".format(
            keyword, (runTime.__round__(3)-lastTime if lastTime is not None else runTime.__round__(3)).__round__(3)))
        lastTime = time() - startTime
    runTime = time() - startTime
    sys.exit("Finished in {}".format(runTime.__round__(3)))


args = sys.argv
if len(args) > 1:
    if args[1].__contains__("-k"):
        keywords = args[2::]
    else:
        sys.exit("usage: run.py -k [args]")
else:
    sys.exit("usage: run.py -k [args]")

for keyword in keywords:
    if os.path.isfile("./csv/data-{}.csv".format(keyword.replace(" ", "_").replace("-", "_"))):
        os.remove(
            f"./csv/data-{keyword.replace(' ', '_').replace('-', '_')}.csv")

    with open("./csv/data-{}.csv".format(keyword.replace(" ", "_").replace("-", "_")), "w", encoding="utf-8") as f:
        f.write("name, reviews, price, link\n")

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
print("Start")
startTime = time()
fetch_urls(keywords)
