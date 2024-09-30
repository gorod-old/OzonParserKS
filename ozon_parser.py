from time import sleep

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from g_gspread import get_sheet_data_by_title
from scroll_webpage import page_down

SPREADSHEET_ID = '1rpJDfy3i4fsNFZjtZxM7guK7ULpA_z9z9pHmNWVDN6I'
SETUP_SHEET_TITLE = 'Настройки'


def get_filter(filter_list):
    filter_str = ''
    for f in filter_list:
        if f == 'Рейтинг продавца':
            filter_str += '&is_high_rating_premium_seller=t'
        elif f == 'Распродажа':
            filter_str += '&is_promo=t'
        elif f == 'Новинки':
            filter_str += '&isnew=t'
    return filter_str


def start():
    setup = get_setup()

    for item in setup:
        get_data(item)


def get_setup():
    setup_data = get_sheet_data_by_title(SPREADSHEET_ID, SETUP_SHEET_TITLE)
    setup = []
    for row in setup_data:
        if row[0] == 'TRUE':
            item = {
                'sheet': row[1],
                'request': row[2],
                'depth': row[3],
                'filter': get_filter([row[4], row[5], row[6]])
            }
            setup.append(item)
    return setup


def append_sheet_data(data):
    pass


def get_data(item):
    sheet_ = item['sheet']
    request_ = item['request']
    depth_ = item['depth']
    filter_ = item['filter']

    driver = uc.Chrome()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    sleep(2)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(request_)
    sleep(2)

    find_input.send_keys(Keys.ENTER)
    sleep(2)

    # current_url = f'{driver.current_url}&sorting=rating'
    current_url = f'{driver.current_url}{filter_}'
    driver.get(url=current_url)
    sleep(10)

    page_down(driver)
    sleep(50)

    product_urls = []
    try:
        links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
        product_urls = list(set([f'{link.get_attribute("href")}' for link in links]))
        print('[+] ссылки на товары собраны')
    except Exception as e:
        print('[!] что-то пошло не так во время сбора ссылок на товары')
        print(str(e))

    print('всего:', len(product_urls))

    driver.close()
    driver.quit()
