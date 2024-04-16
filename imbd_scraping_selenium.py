from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import csv


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


def get_csselectors(selector):
    contents = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , selector)))
    return contents

def get_site(link):
    driver.get(link)

def get_oneelementcss(selector):
    content =WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR  , selector)))
    return content
def get_one_element_xpath(xpath):
    content = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , xpath)))
    return content
def get_back():
    driver.back()

def get_multi_element_xpath(xpath):
    contents = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH , xpath)))
    return contents

def get_multi_elements_classname(xpath):
    contents = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME , xpath)))
    return contents

def put_down():
    driver.execute_script("window.scrollBy(0, 1000);")

def write_to_csv(movie_info):
    fieldnames = ["Movie Name", "Movie Category", "Movie General Rate", "Year", "Score", "Age Limit", "User Name", "Comment Title", "Comment"]
    with open("imbd.csv" , "a" , newline="" ,encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile , fieldnames=fieldnames)
        writer.writerow(movie_info)


get_site("https://www.imdb.com/chart/top/")

scroll_count =0
for i in range(150,200):

    try:
        #enter  general movie page
        content = get_csselectors("h3.ipc-title__text")
        content[i].click()
        time.sleep(2)

        title = get_oneelementcss("span.hero__primary-text").text
        category = get_oneelementcss("span.ipc-chip__text").text

        rate = get_one_element_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[1]/a/span/div/div[2]/div[1]/span[1]').text
        year = get_one_element_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a').text

        score =get_one_element_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[1]/a/span/span[1]').text

        limit_age = get_one_element_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a').text
        time.sleep(2)
        put_down()
        
        time.sleep(2)

    except Exception as e:
        print(e)
    try:
        #enter review page
        review_site = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH , '/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[8]/div[1]/div/a')))
        deneme = review_site.text
        first_line =deneme.splitlines()[0]
        print(first_line)
        if(first_line !="User reviews"):
            get_back()
            time.sleep(2)
            continue
        review_link = review_site.get_attribute("href")
        print(review_link)
        get_site(review_link)
        time.sleep(4)
    except Exception as e:
        print(e)
        continue
    #select without spoiler box
    spoiler = get_one_element_xpath('/html/body/div[2]/div/div[2]/div[3]/div[1]/section/div[2]/div[1]/form/div/div[1]/label/span[1]')
    spoiler.click()
    time.sleep(4)
    try:
        user_name = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR ,"span.display-name-link")))
        comment_title = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR ,"a.title")))
        user_comment =WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR ,"div.text.show-more__control")))

        for j in range(len(user_name)):
            movie_info = {
                "Movie Name" : title,
                "Movie Category" : category ,
                "Movie General Rate" : rate ,
                "Year" : year,
                "Score" : score,
                "Age Limit" : limit_age,
                "User Name" :user_name[j].text,
                "Comment Title" : comment_title[j].text,
                "Comment" : user_comment[j].text
            }
            write_to_csv(movie_info)

    except Exception as e:
        print(e)
    
    scroll_count += 1
    if scroll_count ==5:
        put_down()
        put_down()
        scroll_count =0
    
        
    get_back()
    get_back()
    get_back()


