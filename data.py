import sys
import numpy as np
import os

data = []
price = []
reviews = []


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


def work(lines, name=None):
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
        name.replace("CLEANED-data-", "")
            .replace("_", " ")
            .replace(".csv", "")
    ) + str(avgprice.round(2)))

    # print("Average Reviews of \"{}\": ".format(
    #     name.replace("CLEANED-data-", "")
    #     .replace("_", " ")
    #     .replace(".csv", "")
    # ) + str(avgrev.round(1)) + "\n")


def dir():
    for file in os.listdir("./csv/"):
        clean("./csv/" + file)

    for file in os.listdir("./cleancsv/"):
        lines_seen = set()  # holds lines already seen
        outfile = open("./cleancsv/CLEANED" +
                       file.replace("clean", "").replace("CLEANED", ""), "w")
        for line in open("./cleancsv/" + file, "r"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        os.remove("./cleancsv/" + file)

    for file in os.listdir("./cleancsv/"):
        with open("./cleancsv/{}".format(file), "r", encoding="utf-8") as f:
            lines = f.readlines()
            work(lines, file)
    sys.exit("Finished")


if __name__ == "__main__":
    print("Started")
    # arg()
    dir()
