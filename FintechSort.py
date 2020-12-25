import pandas as pd
import numpy as np

def getBreakdown(identifier):
    counts = {
        "General Fintech":0,
        "Contract (Blockchain)":0,
        "Decision (AI)":0,
        "RegTech":0,
        "WealthTech":0,
        "InsurTech":0,
        "Payments":0,
        "Lending":0
    }

    generalFintech = [
        "fintech",
        "unbank",
        "tech",
        "mobile",
        "digital",
        "innovat",
        "online bank",
        "web bank",
        "internet bank",
        "app",
        "virtual",
        "techfin"
    ]

    contract = [
        "blockchain",
        "distributed ledger",
        "smart contract",
        "authenticat",
        "e-money",
        "emoney",
        "crypto",
        "digital cash",
        "bitcoin",
        "ethereum",
        "token"
    ]

    decision = [
        "artificial intelligence",
        "ai",
        "machine learning",
        "deep learning",
        "automat",
        "big data",
        "analytics"
    ]

    regTech = [
        "regtech",
        "cybersecur",
        "cyber secur",
        "cybercrim"
    ]

    wealthTech = [
        "wealthtech",
        "wealth tech",
        "robo",
        "betterment",
        "wealthfront",
        "digital advi"
    ]

    insurTech = [
        "insurtech",
        "insurance tech",
        "wearabl",
        "genomic",
        "smart car"
    ]

    payments = [
        "qr code",
        "nfc",
        "near field communicat",
        "peer-to-peer pay",
        "peer to peer pay",
        "p2p pay",
        "contactless",
        "paypal",
        "stripe"
    ]

    lending = [
        "peer-to-peer lend",
        "peer to peer lend",
        "p2p lend",
        "marketplace lend",
        "online lend",
        "crowdfund",
        "proptech",
        "prosper",
        "lending club"
    ]

    currFile = pd.read_csv("..//articles//"+identifier+".csv",header=None,index_col=None)
    currFile = currFile.iloc[[0,1],:]

    for i in range(currFile.shape[1]):
        currArticle = currFile.iloc[1,i]
        
        # check for text matching one of the fintech categories
        result_scores = {
        "General Fintech": np.mean([x in currArticle.lower() for x in generalFintech]),
        "Contract (Blockchain)":np.mean([x in currArticle.lower() for x in contract]),
        "Decision (AI)": np.mean([x in currArticle.lower() for x in decision]),
        "RegTech": np.mean([x in currArticle.lower() for x in regTech]),
        "WealthTech": np.mean([x in currArticle.lower() for x in wealthTech]),
        "InsurTech": np.mean([x in currArticle.lower() for x in insurTech]),
        "Payments": np.mean([x in currArticle.lower() for x in payments]),
        "Lending": np.mean([x in currArticle.lower() for x in lending])
        }
        highScore = max(result_scores.values())
        if highScore == 0:
            continue
        for key,val in result_scores.items():
            if val == highScore:
                counts[key] += 1
        
    return(counts)




if __name__ == "__main__":
    master = pd.read_excel("..//instructions//Press Releases - Master.xlsx")
    master = master.loc[master["Assigned"] == 1,:]

    for i in range(master.shape[0]):
        ticker = master["Ticker"].iloc[i]
        year = master["Year"].iloc[i]
        quarter = master["Quarter"].iloc[i]

        file = ticker+"_"+year+"Q"+quarter

        breakdown = getBreakdown(file)

        master.iloc[i,7] = breakdown["General Fintech"]
        master.iloc[i,8] = breakdown["Contract (Blockchain)"]
        master.iloc[i,9] = breakdown["Decision (AI)"]
        master.iloc[i,10]= breakdown["RegTech"]
        master.iloc[i,11]= breakdown["WealthTech"]
        master.iloc[i,12]= breakdown["InsurTech"]
        master.iloc[i,13]= breakdown["Payments"]
        master.iloc[i,14]= breakdown["Lending"]
    
    print(master)

    


