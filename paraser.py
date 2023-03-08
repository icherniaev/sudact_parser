import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from time import sleep
from tqdm import tqdm
from selenium.webdriver.common.by import By

#libraries for multithreading
import datetime
import sys
from concurrent.futures import ThreadPoolExecutor, wait
from time import sleep, time


import warnings
warnings.filterwarnings("ignore")
#custom mudules import
from utilities import driver
from utilities import init_page_parser
from utilities import init_clicker
from utilities import inner_parser

df = pd.DataFrame(columns=['case_num', 'judge_name', 'name', 'date', 'articles', 'result'])


def parser(url, k):
    browser = driver() #starts the browser
    url_curr = url #get the current url
    browser.get(url_curr) #open the starting page
    #parase the starting page
    case_name = init_page_parser(browser=browser)
    init_clicker(case_name, browser) #just clicks the first link
    #here we finally get to the inner page and start parsing
    hold = inner_parser(browser=browser, k=k)
    browser.close()
    path = '/Users/ilyachernyaev/Documents/projects/parser/files'
    hold.to_csv(path+'file_%s' %k, index = False)


######### script

'''import threading
from my_paraser import parser
from link_generator import link_generator
import pandas as pd

urls = link_generator()
df = pd.DataFrame(columns=['case_num', 'judge_name', 'name', 'date', 'articles', 'result'])

threads = []

for i in range(10):
    url_curr = urls[i]
    thread = threading.Thread(
        target=parser,
        args=[url_curr, i, df]
    )
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()'''





