from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm

def driver():
    '''
    Set the browser settings
    Returns browser instance
    '''
    driver = Chrome('/Users/ilyachernyaev/Documents/projects/chromedriver')
    driver.implicitly_wait(30)
    return driver

def init_page_parser(browser):
    '''
    Checks whether the current page has loaded
    Repeats the procedure for 30 seconds
    If it has => get the HTML and returns the first case name
    '''
    for i in range(60):
        try:
            soup_gen = BeautifulSoup(browser.page_source, 'html')
            list_of_cases = soup_gen.find('ul', class_='resultsList').find_all('li')
            case_test = list_of_cases[0].find('div', class_='bgs-result')
            break
        except:
            sleep(1)
    soup_gen = BeautifulSoup(browser.page_source, 'html')
    list_of_cases = soup_gen.find('ul', class_='resultsList').find_all('li')
    #when we get the working html of the initial page
    case_name = list_of_cases[0].find('div', class_='bgs-result') \
        .find('a', class_='resultHeader openCardLink') \
        .text
    return case_name


def init_clicker(case_name, browser):
    '''
    Takes the name of the first case and browser
    Tries to click the link for the first case for 30 seconds
    '''
    for i in range(30):
        try:
            to_click = browser.find_element(By.LINK_TEXT, case_name)
            to_click.click()
            break
        except:
            sleep(1)

def inner_parser(browser, k, num_pages=10):
    '''
    For a given number of pages parses the page and steps to the next one.
    Does so with a delay of 7 seconds (to avoid captcha)
    '''
    #creates dataframe for further use
    inner_df = pd.DataFrame(columns=['case_num', 'judge_name', 'name', 'date', 'articles', 'result'])

    for i in tqdm(range(num_pages)):
        button = browser.find_element(By.XPATH, '//*[@id="cardContainer"]/div[1]/div/div/span[3]/span')

        soup_loc = BeautifulSoup(browser.page_source, 'html')
        table = soup_loc.find_all('td', class_='one-table-value')
        judge_name = soup_loc.find_all('li', class_='group-box group-box-open fieldGroup')[1].find('a', class_='paramLink one-value').text
        case_num = soup_loc.find('span', class_='one-value').text

        #parse the second table
        name = table[0].text
        date = table[1].text
        articles = table[2].text
        result = table[3].text

        #add the elements to the dataframe
        df_temp = pd.DataFrame({'case_num': case_num,
                                        'judge_name': judge_name,
                                        'name': name,
                                        'date': date,
                                        'articles': articles,
                                        'result': result
                                       }, index=[0])
        inner_df = inner_df.append(df_temp)
        #clicks the button to next page
        button.click()
        #sleeps for 30 seconds
        sleep(7)
    return inner_df

def link_generator():
    # generate the necessary urls from a given one
    nums = [i for i in range(0, 10790, 10)]
    urls = []

    for i in nums:
        urls.append(f'https://bsr.sudrf.ru/bigs/portal.html#%7B%22start%22:{i},%22rows%22:50,%22uid%22:%22da729f26-1175-45d1-991b-7f2057359c7d%22,%22type%22:%22MULTIQUERY%22,%22multiqueryRequest%22:%7B%22queryRequests%22:%5B%7B%22type%22:%22Q%22,%22request%22:%22%7B%5C%22mode%5C%22:%5C%22EXTENDED%5C%22,%5C%22typeRequests%5C%22:%5B%7B%5C%22fieldRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22case_doc_subject_rf%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%5C%22,%5C%22fieldName%5C%22:%5C%22case_doc_subject_rf_cat%5C%22%7D,%7B%5C%22name%5C%22:%5C%22case_document_category_article_cat%5C%22,%5C%22operator%5C%22:%5C%22SEW%5C%22,%5C%22query%5C%22:%5C%22%D0%A1%D1%82%D0%B0%D1%82%D1%8C%D1%8F%20158%20%D0%A7%D0%B0%D1%81%D1%82%D1%8C%201%5C%22,%5C%22fieldName%5C%22:%5C%22case_document_category_article_cat%5C%22%7D%5D,%5C%22mode%5C%22:%5C%22AND%5C%22,%5C%22name%5C%22:%5C%22common%5C%22,%5C%22typesMode%5C%22:%5C%22AND%5C%22%7D%5D%7D%22,%22operator%22:%22AND%22,%22queryRequestRole%22:%22CATEGORIES%22%7D%5D%7D,%22sorts%22:%5B%7B%22field%22:%22score%22,%22order%22:%22desc%22%7D%5D,%22simpleSearchFieldsBundle%22:%22default%22,%22noOrpho%22:false,%22groupLimit%22:3,%22woBoost%22:false,%22facet%22:%7B%22field%22:%5B%22type%22%5D%7D,%22facetLimit%22:21,%22additionalFields%22:%5B%22court_document_documentype1%22,%22court_case_entry_date%22,%22court_case_result_date%22,%22court_subject_rf%22,%22court_name_court%22,%22court_document_law_article%22,%22court_case_result%22,%22case_user_document_type%22,%22case_user_doc_entry_date%22,%22case_user_doc_result_date%22,%22case_doc_subject_rf%22,%22case_user_doc_court%22,%22case_doc_instance%22,%22case_document_category_article%22,%22case_user_doc_result%22,%22case_user_entry_date%22,%22m_case_user_type%22,%22m_case_user_sub_type%22,%22ora_main_law_article%22%5D,%22hlFragSize%22:1000%7D')
    
    return urls




