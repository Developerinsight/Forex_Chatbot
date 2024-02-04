from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys # 엔
import datetime
from selenium.webdriver.common.by import By

####사용자 지정 필요
PATH = "/home/misys/AI_ws/chatbot" ## 드라이버 경로 
######

# 환율 크롤링: 기간 마음대로 정할 수 있음 1일부터 2000년까지
def exchange(year, month, day):
    path = PATH
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    driver = webdriver.Chrome(path + '/chromedriver.exe', chrome_options=options)


    driver.get('https://spot.wooribank.com/pot/Dream?withyou=CMCOM0186')
    #driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[2]/td/input[2]").click()
    driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[2]/td/input[2]").click()
    time.sleep(1)
    
    # 1년 환율
    #driver.find_element_by_xpath(f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[1]/option[{year-1999}]").click()
    driver.find_element(by=By.XPATH, value=f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[1]/option[{year-1999}]").click()

    # month 선택: 1월부터 1
    #driver.find_element_by_xpath(f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[2]/option[{month}]").click()
    driver.find_element(by=By.XPATH, value=f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[2]/option[{month}]").click()
   
    # day 선택: 1일부터 1
    #driver.find_element_by_xpath(f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[3]/option[{day}]").click()
    driver.find_element(by=By.XPATH, value=f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[3]/option[{day}]").click()

    # 조회 클릭
    #driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/fieldset/div/span/input").click()
    driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/fieldset/div/span/input").click()
    
    # text 가져오기
    time.sleep(1)
    dollar = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/div/div[1]/table/tbody/tr[1]/td[7]").text    
    dollar = dollar.replace(",","")
    dollar = float(dollar)
    
    time.sleep(1)
    yen = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/div/div[1]/table/tbody/tr[2]/td[7]").text
    yen = yen.replace(",","")
    yen = float(yen)    
    
    time.sleep(1)
    euro = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/div/div[1]/table/tbody/tr[3]/td[7]").text
    euro = euro.replace(",","")
    euro = float(euro) 
    
    exchange = {'dollar': dollar, 'yen': yen, 'euro': euro}
    
    return exchange 

    path = PATH
def dollar_index(year, month, day):
    
    import datetime
    today = datetime.date.today()
    target_date = datetime.date(year, month, day)

    d_day = today - target_date 
    d_day = d_day.days

    path = PATH
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    driver = webdriver.Chrome(path + '/chromedriver.exe', chrome_options=options)
    
    
    # 대상 url 이동
    driver.get('https://finance.yahoo.com/quote/DX-Y.NYB/history?period1=1511740800&period2=1669507200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')
    time.sleep(2)
    
    #driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]").click()
    driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]").click()
    time.sleep(2)
               
    lst = []
    cnt = 0
    rng = d_day//20
    for c in range(0,rng+1):
        driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    table = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table")
    
    tbody = table.find_element(by=By.TAG_NAME, value = "tbody")
    rows = tbody.find_elements(by=By.TAG_NAME, value="tr")
    for index, value in enumerate(rows):
        body = value.find_elements(by=By.TAG_NAME, value="td")[5]
        if cnt != d_day:
            try:
                lst.append(float(body.text))
                cnt +=1 
            except:
                cnt +=1
                
        else:
            break
    driver.close()
    
    return str(sum(lst) / len(lst))
# 기사 크롤링
def article():
    path = PATH
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    driver = webdriver.Chrome(path + '/chromedriver.exe', chrome_options=options)
    

    #driver.find_element(by=By.XPATH, value='//<your xpath>')

    # 대상 url 이동
    driver.get('https://kr.investing.com/')
    time.sleep(1)
    
    # 화면 크기 최대화 
    driver.maximize_window()
    
    # 뉴스 창 이동
    time.sleep(1)
    #driver.find_element_by_xpath("/html/body/div[5]/header/div[2]/nav[1]/ul/li[5]/a").click()
    driver.find_element(by=By.XPATH, value="/html/body/div[5]/header/div[2]/nav[1]/ul/li[5]/a").click()

    # 외한 창 이동
    time.sleep(1)
    #driver.find_element_by_xpath("/html/body/div[5]/header/div[2]/nav[2]/ul/li[2]/a").click()
    driver.find_element(by=By.XPATH, value="/html/body/div[5]/header/div[2]/nav[2]/ul/li[2]/a").click()

    article = ''

    for i in range(1,19,1):
        txt = driver.find_element(by=By.XPATH, value=f"/html/body/div[5]/section/div[4]/article[{i}]").text
        article += txt
        article
    driver.close()
    
    return article

#article()

# 구매 결정
def decision(year, month, day):
    path = PATH
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    driver = webdriver.Chrome(path + '/chromedriver.exe', chrome_options=options)
    
    
    # 대상 url 이동
    driver.get('https://finance.yahoo.com/quote/DX-Y.NYB/history?p=DX-Y.NYB')
    time.sleep(2)
    
    #driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]").click()
    driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]").click()
    time.sleep(2)
    
    index_lst = []
    
    for c in range(0,20):
        driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        
    table = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table")

    tbody = table.find_element(by=By.TAG_NAME, value = "tbody")
    rows = tbody.find_elements(by=By.TAG_NAME, value="tr")
    for index, value in enumerate(rows):
        body = value.find_elements(by=By.TAG_NAME, value="td")[5]
        try:
            index_lst.append(float(body.text))
        except:
            pass
            
    index_1 = index_lst[0]
    index_1y = sum(index_lst)/len(index_lst)
    
    driver.close()
    
    path = PATH
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    driver = webdriver.Chrome(path + '/chromedriver.exe', chrome_options=options)

    driver.get('https://spot.wooribank.com/pot/Dream?withyou=CMCOM0186')
    #driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[2]/td/input[2]").click()
    driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[2]/td/input[2]").click()
    
    time.sleep(1)
    
    # 1년 환율
    #driver.find_element_by_xpath(f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[1]/option[{year-1999}]").click()
    driver.find_element(by=By.XPATH, value=f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[1]/option[{year-1999}]").click()
                             
    # month 선택: 1월부터 1
    #driver.find_element_by_xpath(f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[2]/option[{month}]").click()
    driver.find_element(by=By.XPATH, value=f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[2]/option[{month}]").click()

    # day 선택: 1일부터 1
    #driver.find_element_by_xpath(f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[3]/option[{day}]").click()
    driver.find_element(by=By.XPATH, value=f"/html/body/div/div[2]/div[2]/form/fieldset/table/tbody/tr[3]/td/div[1]/select[3]/option[{day}]").click()

    # 조회 클릭
    #driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/fieldset/div/span/input").click()
    driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/fieldset/div/span/input").click()

    # text 가져오기
    time.sleep(1)
    ex_1y = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div[2]/form/div/div[1]/table/tbody/tr[1]/td[7]").text 
    ex_1y = ex_1y.replace(",","")
    ex_1y = float(ex_1y)
    
    # 창 닫기
    driver.close()
    
    path = r"C:\Users\조영민\Desktop\학교수업\chromedriver_win32" # driver 경로 
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    driver = webdriver.Chrome(path + '/chromedriver.exe', chrome_options=options)
    
    # 1일  환율
    driver.get('https://kr.investing.com/')
    time.sleep(3)
    
    driver.maximize_window()
    
    #driver.find_element_by_xpath("/html/body/div[8]/div[2]/i").click()
    time.sleep(1)
    
    #driver.find_element_by_xpath("/html/body/div[5]/aside/div[2]/div[1]/ul/li[3]").click()
    driver.find_element(by=By.XPATH, value="/html/body/div[5]/aside/div[2]/div[1]/ul/li[3]").click()

    ex_1 = driver.find_element(by=By.XPATH, value='/html/body/div[5]/aside/div[2]/div[2]/div[2]/table[3]/tbody/tr[1]/td[3]').text
    ex_1 = ex_1.replace(",","")
    ex_1 = float(ex_1)
    driver.close()
    time.sleep(1)

    if ex_1 < ex_1y and index_1 < index_1y and (index_1/ex_1*100) > (index_1y/ex_1y*100) and ex_1 < (index_1 /(index_1y/ex_1y*100))*100:
        return "Buy it now!"
        
    else:
        return "Wait!"

import re
import os
import nltk
from nltk.corpus import wordnet
from web import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

nltk.download('wordnet')
nltk.download('omw-1.4')

os.system('clear')

def appendix(key,day,month,year):
    if key=='yen':
        print ("=== BOT : Wait a few seconds")
        ex = exchange(year, month, day)
        return str(ex['yen']) + "\n\n=== BOT : Can I help you further?"
    elif key=='dollar':
        print ("=== BOT : Wait a few seconds")
        ex = exchange(year, month, day)
        return str(ex['dollar'])  + "\n\n=== BOT : Can I help you further?"
    elif key=='euro':
        print ("=== BOT : Wait a few seconds")
        ex = exchange(year, month, day)
        return str(ex['euro']) + "\n\n=== BOT : Can I help you further?"
    elif key=='news':
        print ("=== BOT : Wait a few seconds")
        return "\n" + str(article()) + "\n\n=== BOT : Can I help you further?"
    elif key=='dollar index':
        print ("=== BOT : Wait a few seconds")
        idx = dollar_index(year, month, day)
        return str(idx) + "\n\n=== BOT : Can I help you further?"
        
    elif key=='purchase':
        print ("=== BOT : Wait a few seconds")
        dec = decision(year, month, day)
        if dec == "Buy it now!":
            return 'lets buy' + "\n\n=== BOT : Can I help you further?"
        else:
            return 'no, you should not buy' + "\n\n=== BOT : Can I help you further?"
    elif key=='sell':
        print ("=== BOT : Wait a few seconds")
        dec = decision(year, month, day)
        if dec == "Buy it now!":
            return 'no, you should not sell' + "\n\n=== BOT : Can I help you further?"
        else:
            return 'lets sell' + "\n\n=== BOT : Can I help you further?"
    else:
        return ''
    
    
list_words=['hi','exchange rate','yen','dollar','euro','news','dollar index','purchase','sell']

list_exchange_word = ['rate of exchange', 'currency rate']
list_news_word = ['article']
list_index_word = ['dxy', 'udxy']

list_syn={}
for word in list_words:
    synonyms=[]
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # Remove any special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    
    if(len(synonyms) == 0):
        lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', word)
        synonyms.append(lem_name)
    if word == 'exchange rate':
        for lem in list_exchange_word:
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem)
            synonyms.append(lem_name)
    if word == 'dollar index':
        for lem in list_index_word:
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem)
            synonyms.append(lem_name)
    if word == 'news':
        for lem in list_news_word:
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem)
            synonyms.append(lem_name)
    list_syn[word]=set(synonyms)
    
# print (list_syn)
# Building dictionary of Intents & Keywords
keywords={}
keywords_dict={}
# Defining a new key in the keywords dictionary

for word in list_words:
    keywords[word]=[]
    # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
    for synonym in list(list_syn[word]):
        keywords[word].append('.*\\b'+synonym+'\\b.*')
    if len(keywords[word])==0:
        keywords[word].append('.*\\b'+word+'\\b.*')
    
    list_news_word
    
for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))
    
# print (keywords_dict)
# Building a dictionary of responses
responses={
    'hi':'=== BOT : Hello! How can I help you?',
    'exchange rate':'=== BOT : What exchange rate should I tell you?',
    'yen':'=== BOT : The exchange rate of the yen is',
    'dollar':'=== BOT : The exchange rate of the dollar is',
    'euro':'=== BOT : The exchange rate of the euro is',
    'news':'=== BOT : The following is a list of addresses for news.',
    'dollar index':'=== BOT : The dollar index is',
    'purchase':'=== BOT : ',
    'sell':'=== BOT : ',
    'fallback':'=== BOT : I dont quite understand. Could you repeat that?',
}           
print ("=== BOT : Welcome to MyBank. How may I help you?")
# While loop to run the chatbot indefinetely
while (True):  
    # Takes the user input and converts all characters to lowercase
    user_input = input("====== User : ").lower()
    # Defining the Chatbot's exit condition
    if user_input == 'quit': 
        print ("=== BOT : Thank you for visiting.")
        break    
    matched_intent = None
    now = datetime.now()
    default_year=datetime.today().year        # 현재 연도 가져오기
    default_month=datetime.today().month      # 현재 월 가져오기
    default_day=datetime.today().day        # 현재 일 가져오기
    
    default_day=(now - timedelta(days=1)).day
    default_month=(now - timedelta(days=1)).month
    default_year=(now - timedelta(days=1)).year
    
    for intent,pattern in keywords_dict.items():
        # Using the regular expression search function to look for keywords in user input
        if re.search(pattern, user_input): 
            # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
            matched_intent=intent
            
    # The fallback intent is selected by default
    if re.search('.*\\bago\\b.*', user_input) or re.search('.*\\bbefore\\b.*', user_input):
        if re.search('.*\\bday\\b.*', user_input) or re.search('.*\\bdays\\b.*', user_input): 
            numbers = int(re.sub(r'[^0-9]', '', user_input))
            default_day=(now - timedelta(days=numbers)).day
            default_month=(now - timedelta(days=numbers)).month
            default_year=(now - timedelta(days=numbers)).year
        if re.search('.*\\bweek\\b.*', user_input) or re.search('.*\\bweeks\\b.*', user_input): 
            numbers = int(re.sub(r'[^0-9]', '', user_input))
            default_day=(now - timedelta(weeks=numbers)).day
            default_month=(now - timedelta(weeks=numbers)).month
            default_year=(now - timedelta(weeks=numbers)).year
        if re.search('.*\\bmonth\\b.*', user_input) or re.search('.*\\bmonths\\b.*', user_input): 
            numbers = int(re.sub(r'[^0-9]', '', user_input))
            default_day=(now - relativedelta(months=numbers)).day
            default_month=(now - relativedelta(months=numbers)).month
            default_year=(now - relativedelta(months=numbers)).year
        if re.search('.*\\byear\\b.*', user_input) or re.search('.*\\byears\\b.*', user_input): 
            numbers = int(re.sub(r'[^0-9]', '', user_input))
            default_year=(now - relativedelta(years=numbers)).year
    if re.search('.*\\byesterday\\b.*', user_input): 
        numbers = 1
        default_day=(now - timedelta(days=numbers)).day
        default_month=(now - timedelta(days=numbers)).month
        default_year=(now - timedelta(days=numbers)).year
    
    
        
    key='fallback' 
    if matched_intent in responses:
        # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        key = matched_intent
    # The chatbot prints the response that matches the selected intent
    if key!='hi' and key!='fallback' and key!='purchase' and key!='sell' and key!='news' and key!='exchange rate':
        print("=== BOT : In",default_year,"year",default_month,"month",default_day,"day") 
    print (responses[key], appendix(key,default_day,default_month,default_year)) 
