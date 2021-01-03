from GetAllReleases import getQueryArray
from os import listdir
from os.path import isfile, join
import pandas as pd
import re

if __name__ == "__main__":

    # get list of all queries
    all_queries = getQueryArray()

    results = dict()

    for i in range(len(all_queries)):
        filepath = str(all_queries["Ticker"].iloc[i]) + "_" + str(all_queries["Year"].iloc[i]) + "Q" + \
            str(all_queries["Quarter"].iloc[i]) +".csv"
        files = [f for f in listdir("..\\articles\\") if isfile(join("..\\articles\\", f))]

        flags = [0, 0, 0, 0, 0, 0, 0, 0]

        if filepath in files:
            with open(join("..\\articles\\", filepath), encoding='UTF-8') as f:
                for line in f:
                    #general fintech
                    r = re.compile(r'\bfintech\b|\bunbank[a-z]*|\btech[a-z]*|\bdigital[a-z]*|\binnovat[a-z]*|\bonline bank[a-z]*|\bweb bank[a-z]*|\binternet bank[a-z]*|\bapp\b|\bvirtual[a-z]*|\btechfin\b', flags=re.I)
                    if r.search(line):
                        flags[0] = 1
                    #contract-based tech
                    r = re.compile(r'\bblockchain\b|\bdistributed ledger\b|\bsmart contract\b|\bauthentication\b|\be-money\b|\bcrypto[a-z]*|\bdigital cash\b|\bbitcoin\b|\bethereum\b|\btoken[a-z]*', flags=re.I)
                    if r.search(line):
                        flags[1] = 1
                    #decision-based tech
                    r = re.compile(r'\bartificial intelligence\b|\bmachine learning\b|\bdeep learning\b|\bautomat[a-z]*|\bbig data\b|\banalytics\b', flags=re.I)
                    if r.search(line):
                        flags[2] = 1
                    #regtech
                    r = re.compile(r'\bregtech\b|\bcybersecur[a-z]*|\bcybercrim[a-z]*', flags=re.I)
                    if r.search(line):
                        flags[3] = 1
                    #wealthtech
                    r = re.compile(r'\bwealthtech\b|\bwealth technology\b|\brobo[a-z]*|\bbetterment\b|\bwealthfront\b|\bdigital advi[a-z]*', flags=re.I)
                    if r.search(line):
                        flags[4] = 1
                    #insurtech
                    r = re.compile(r'\binsurtech\b|\binsurance technology\b|\bwearabl[a-z]*|\bgenomic[a-z]*|\bsmart car[a-z]*', flags=re.I)
                    if r.search(line):
                        flags[5] = 1
                    #payments
                    r = re.compile(r'\bQR code\b|\bnear field communication\b|\bNFC\b|\bpeer-to-peer pay[a-z]*|\bP2P pay[a-z]*|\bcontactless\b|\bpaypal\b|\bstripe\b', flags=re.I)
                    if r.search(line):
                        flags[6] = 1
                    #lending
                    r = re.compile(r'\bpeer-to-peer lend[a-z]*|\bP2P lend[a-z]*|\bmarketplace lend[a-z]*|\bonline lend[a-z]*|\bcrowdfund[a-z]*|\bproptech\b|\bprosper\b|\blending club\b', flags=re.I)
                    if r.search(line):
                        flags[7] = 1

        results[filepath] = flags

    filepath = "..\\results.csv"
    pd.DataFrame.from_dict(results, orient='index').to_csv(filepath, index=True)