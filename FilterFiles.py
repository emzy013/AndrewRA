from GetAllReleases import getQueryArray
from os import listdir
from os.path import isfile, join
import csv
import pandas as pd
import re
import sys

if __name__ == "__main__":

    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    # get list of all queries
    all_queries = getQueryArray()

    for i in range(len(all_queries)):
        filepath = str(all_queries["Ticker"].iloc[i]) + "_" + str(all_queries["Year"].iloc[i]) + "Q" + \
            str(all_queries["Quarter"].iloc[i]) +".csv"
        files = [f for f in listdir("..\\articles\\") if isfile(join("..\\articles\\", f))]

        if filepath in files:
            articleDict = {}
            with open(join("..\\articles\\", filepath), 'r', encoding='UTF-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    headings = row.keys()
                    for heading in headings:
                        r = re.compile(all_queries["Name"].iloc[i])
                        if len(r.findall(row[heading])) > 3:
                            articleDict[heading] = row[heading]
                    break
            if bool(articleDict):
                pd.DataFrame(articleDict, index=[1]).to_csv(join("..\\articles2\\", filepath), index=False)
