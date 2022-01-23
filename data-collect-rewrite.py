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

    with open("clean-" + file.replace("./", ""), "w+", encoding="utf-8") as f:
        f.write(content_clean3)


def fetch_urls(keywords, *args):
    for keyword in keywords:
        driver = webdriver.Chrome(options=options)
        for page_nb in range(1, 10):
            driver.get(
                "https://www.amazon.com/s?k={}&page={}".format(keyword, page_nb))
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
                (_, _, link, _) = links[0]
                strLink = "amazon.com/" + link
                listLink = [strLink]
                link = (listLink if len(price)
                        > 0 or len(title) > 0 else [])

                title = str(title[0]).replace(",", "") if len(title) > 0 else str(
                    title).replace(",", "")
                reviews = str(reviews[0]).replace(",", ".") if len(
                    reviews) > 0 else str(reviews).replace(",", ".")
                price = str(price[0]).replace("\xa0", "").replace(",", ".").replace("'", "") if len(price) > 0 else str(
                    price).replace(",", ".").replace("\xa0", "").replace("'", "")
                link = str(link[0]).replace("'", "") if len(link) > 0 else str(
                    link).replace("'", "")  # .replace(",", "")

                info = str((title, reviews, price, link)).replace(
                    "(", "").replace(")", "")
                with open("./data-{}.csv".format(keyword), "a", encoding="utf-8") as f:
                    f.write(str(info).replace(
                        "(", "").replace(")", "") + "\n")

        with open("./data-{}.csv".format(keyword), "a", encoding="utf-8") as f:
            f.write("\n\n\n\n\n\n")

        driver.close()
        sleep(1)
        clean("./data-{}.csv".format(keyword))
        runTime = time() - startTime
        print("Finished collecting \"{}\" data in {} Seconds".format(
            keyword, runTime.__round__(4)))
    runTime = time() - startTime
    sys.exit("Finished in {}".format(runTime.__round__(4)))


keywords = sys.argv
if keywords[1] == "-k":
    keywords = keywords[2::]
    for keyword in keywords:
        with open("./data-{}.csv".format(keyword), "w", encoding="utf-8") as f:
            f.write("name, reviews, price, link\n")

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
print("Start")
startTime = time()
fetch_urls(keywords)
