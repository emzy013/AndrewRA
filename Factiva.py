import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select


##################################### CONSTANTS ######################################
URL = "https://guides.lib.uwo.ca/az.php?q=factiva"                                   #
USER = "USERNAME"                                                                    #
PASS = "PASSWORD"                                                                   #
USER_XPATH = "/html/body/center[2]/div/form/p[1]/input"                              #
PASS_XPATH = "/html/body/center[2]/div/form/p[3]/input"                              #
LOGIN_XPATH = "/html/body/center[2]/div/form/p[4]/input"                             #
SEARCH_TEXT_XPATH = "/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/div[2]/div/div[1]/textarea"
UWO_XPATH = "/html/body/div[4]/div[5]/section[2]/div/div[1]/div[4]/div/div[1]/a"     #
SEARCH_XPATH = "/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[3]/div[2]/ul/li/div/span"
RESULTS_XPATH = "/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[3]/div/div[1]/div/div[2]/table/tbody"
ARTICLE_XPATH = "/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div"
DROPDOWN_XPATH = "//*[@id=\"isrd\"]"                                                 #
DUPLICATES_XPATH = ""                                                                #
######################################################################################

def getFactivaSearchResults(search_text):

    articleDict = dict()

    # start browser
    options = Options()
    options.add_argument("--headless")
    print("Opening Browser...")
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(URL)
        factiva = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,UWO_XPATH)))
        factiva.click()

        # wait for new tab and switch to new tab
        WebDriverWait(driver,5).until(EC.number_of_windows_to_be(2))
        time.sleep(2)
        allHandles = driver.window_handles
        driver.switch_to.window(allHandles[len(allHandles)-1])        

        # get user and password field and input info
        try:
            userField = driver.find_element_by_xpath(USER_XPATH)
            passField = driver.find_element_by_xpath(PASS_XPATH)
            userField.send_keys(USER)
            passField.send_keys(PASS)

            # click the login button
            loginField = driver.find_elements_by_xpath(LOGIN_XPATH)[0]
            loginField.click()
        except:
            print("No UWO login needed")

        # enter search text
        textBox = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH , SEARCH_TEXT_XPATH)))
        textBox.send_keys(search_text)
        
        # turn off duplicates
        dropdown = Select(driver.find_element_by_xpath(DROPDOWN_XPATH))
        dropdown.select_by_value("None")
        
        # click the search button
        searchButton = driver.find_elements_by_xpath(SEARCH_XPATH)[0]
        searchButton.click()

        # wait for search results to load and return html
        searchResults = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,RESULTS_XPATH)))
        searchItems = searchResults.find_elements_by_class_name("headline")

        
        for i in range(len(searchItems)):
            try:
                time.sleep(1)
                item = searchItems[i].find_elements_by_class_name("enHeadline")[0]
                item.click()
                article = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,ARTICLE_XPATH)))
                children = article.find_elements_by_xpath(".//*")
                articleList = [x.text for x in children]
                articleList = [x for x in articleList if not x == ""]
                articleTitle = articleList[0]
                del articleList[0]
                articleString= "\n".join(articleList)
                articleDict[articleTitle] = articleString
            except:
                print("Non-responsive article. Continuing...")
            
            # for debugging purposes
            # print(articleTitle, "\n" , articleString)
            # print("\n########################################\n")

        # for debugging purposes
        # print(articleDict)
        # unique = set(i for i in docList)
        # print(unique)
        # print(len(unique))
        # print(len(docList))
        print("Closing browser...")
        allHandles = driver.window_handles
        for i in range(len(allHandles)):
            driver.switch_to.window(allHandles[i])
            driver.close()
        driver.quit()

    except Exception as e:
        driver.quit()
        print("Error: " ,e)
        raise Exception("Website Error.")

    
    return(pd.DataFrame(articleDict,index=[1]))

if __name__ == "__main__":
    results = getFactivaSearchResults("rst=sfprn AND la=en AND date from 16/04/2009 to 01/07/2009 AND tech* AND co=JPM")
    print(results)