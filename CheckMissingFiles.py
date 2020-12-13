import pandas as pd
from GetAllReleases import getQueryArray
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    # get list of all queries
    all_queriers = getQueryArray()

    # get list of all files in the output directory
    missing_files = []
    for i in range(len(all_queriers)):
        filepath = str(all_queriers["Ticker"].iloc[i]) + "_" + str(all_queriers["Year"].iloc[i]) + "Q" + \
            str(all_queriers["Quarter"].iloc[i]) +".csv"
        files = [f for f in listdir("..\\articles\\") if isfile(join("..\\articles\\", f))]
        if filepath in files:
            next
        else:
            missing_files.append(filepath)
    
    f = open("..\\articles\\errorLog.txt" , "w")
    for x in missing_files:
        f.write(x+"\n")
    f.close()
        
        

    # compare file names to queries

    # append each file not in the directory to an error list

    # save error list to .txt for further review
