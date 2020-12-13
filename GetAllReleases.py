from typing import final
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
from pandas.tseries.offsets import YearBegin
from Factiva import getFactivaSearchResults
import time

def getQueryArray():
    # get queries from excel file to iterate through
    queries = []
    pdQueries = pd.read_excel("..\\instructions\\Press Releases - Master.xlsx")
    pdQueries = pdQueries.loc[:,["Ticker","Year","Quarter","Query"]]
    pdQueries.dropna(inplace=True)
    return(pdQueries)

def saveArticles(query, ticker, year, quarter):
    # get excel data from factiva
    print("########### Getting Atricles From Browser ###########")
    results = getFactivaSearchResults(search_text = query)

    # save file to designated path
    filepath = "..\\articles\\" + ticker + "_" + year + "Q" + quarter + ".csv"
    results.to_csv(filepath, index=False)
    print("Saving: ", ticker + "_" + year + "Q" + quarter, sep="")
    print("#####################################################")
    return(None)

if __name__ == "__main__":
    # load in a list of queries
    queries = getQueryArray()
    attempts = 0
    complete = False

    errorList = []
    # changing this will change the starting point in the queries array
    index = np.min(np.where((queries["Ticker"]=="TD").values & (queries["Year"] == 2007).values))
    i = index
    # iterate through all the queries
    while i < len(queries):
        complete = False
        ticker = str(queries.iloc[i,0])
        year = str(queries.iloc[i,1])
        quarter = str(queries.iloc[i,2])
        query = str(queries.iloc[i,3])
        try:
            print("Attempt:", attempts)
            saveArticles(query,ticker,year,quarter)
        except Exception as err:
            attempts += 1
            print("ERROR: ", ticker + "_" + year + "Q" + quarter, sep="")
            print(err)
            
        else:
            complete = True
            time.sleep(1.5)
        finally:
            if (attempts>=4):
                i+=1
                attempts = 0
                errorList.append(ticker + "_" + year + "Q" + quarter)
            elif(complete):
                i+=1
                attempts = 0
    
    # write a document for the items that couldn't be saved
    f = open("..\\articles\\errorLog.txt" , "w")
    for x in errorList:
        f.write(x+"\n")
    f.close()
    
