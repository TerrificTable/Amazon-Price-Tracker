import numpy as np
import os

data = []
price = []
reviews = []


for file in os.listdir("./cleancsv/"):
    with open("./cleancsv/{}".format(file), "r", encoding="utf-8") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if i > 0:
                line = line.split(", ")
                data.append(line)
                try:
                    if line[2] != "???" and line[2] != "Quarry" and not line[2].__contains__("amazon.com"):
                        price.append(line[2])
                    if line[1] != "New Search" and not line[1].__contains__("amazon.com"):
                        reviews.append(
                            line[1] if not line[1] == "[]" and line[1] != "???" else "0")
                except:
                    pass

        newPrice = []
        newReviews = []
        for p in price:
            p = p.split(".")
            newPrice.append(
                int(p[0].replace("$", "") if not p[0] == "\n" else 0))
        for r in reviews:
            newReviews.append(int(r.replace(".", "").replace("$", "")))

        avgprice = np.mean(newPrice)
        avgrev = np.mean(newReviews)
        print("Average Price of \"{}\": ".format(
            file.replace("clean-data-", "")
                .replace("_", " ")
                .replace(".csv", "")
        ) + str(avgprice.round(2)))

        print("Average Reviews of \"{}\": ".format(
            file.replace("clean-data-", "")
            .replace("_", " ")
            .replace(".csv", "")
        ) + str(avgrev.round(1)) + "\n")
