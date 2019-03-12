import warnings
warnings.simplefilter("ignore", UserWarning)
from retrying import retry
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import os
import pandas as pd
import re
import sys


@retry(stop_max_attempt_number=10)
def tryin(driver, url):
    try:
        print('等候10秒打开网页....')
        driver.implicitly_wait(5)
        driver.get(url)
    except:
        driver.get(url)


def get_totals(name, institution):
    """" to get pdf_download_links"""
    total = [121,0,0]
    while total[0] > 0:
        print('设置浏览器.....')
        driver = webdriver.PhantomJS(r"D:\anaconda2\Lib\phantomjs\bin\phantomjs.exe")
        user_agent = "Mozilla/5.0WindowsNT6.1WOW64AppleWebKit/535.8KHTML,likeGeckoBeamrise/17.2.0.9Chrome/17.0.939.0Safari/535.8"
        url = 'http://eng.oversea.cnki.net/kns55/brief/result.aspx?txt_1_value1=&txt_1_sel=%E4%B8%BB%E9%A2%98&dbPrefix=SCDB&db_opt=%E4%B8%AD%E5%9B%BD%E5%AD%A6%E6%9C%AF%E6%96%87%E7%8C%AE%E7%BD%91%E7%BB%9C%E5%87%BA%E7%89%88%E6%80%BB%E5%BA%93&db_value=%E4%B8%AD%E5%9B%BD%E6%9C%9F%E5%88%8A%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E5%8D%9A%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E4%BC%98%E7%A7%80%E7%A1%95%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E4%BC%9A%E8%AE%AE%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E5%9B%BD%E9%99%85%E4%BC%9A%E8%AE%AE%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E6%8A%A5%E7%BA%B8%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E5%B9%B4%E9%89%B4%E7%BD%91%E7%BB%9C%E5%87%BA%E7%89%88%E6%80%BB%E5%BA%93&search-action=brief%2Fresult.aspx'
        driver.set_window_size(1920, 1080)

        driver.set_page_load_timeout(10)
        tryin(driver, url)

        print('select框框切换到第一作者....')
        element = driver.find_element_by_xpath(r"//*[@id='1_4']/a")
        element.click()

        print('input name....')
        driver.set_page_load_timeout(10)
        element = driver.find_element_by_xpath(r"//*[@id='au_2_value1']")
        element.send_keys(name)
        element.send_keys(Keys.RETURN)

        # input institution
        if len(institution) > 2:
            driver.set_page_load_timeout(10)
            element = driver.find_element_by_xpath(r"//*[@id='danwei_1_value1']")
            element.send_keys(institution)
            element.send_keys(Keys.RETURN)

        print('click the search button')
        element = driver.find_element_by_xpath(r'//*[@id="btnSearch"]')
        element.click()
        assert "No results found." not in driver.page_source

        print('switch to iframe....')
        flag = False
        driver.switch_to.frame('iframeResult')
        driver.implicitly_wait(8)

        print('show 50 results--->')
        driver.find_element("id", "id_grid_display_num").click()
        driver.find_element("link text", '50').send_keys(Keys.ENTER)
        driver.implicitly_wait(8)

        print('find total....')
        tar = driver.find_element_by_class_name(r'TitleLeftCell')
        global found
        found = re.findall(r'[0-9]{1,3}', tar.text)
        if int(found[0]) == 121:
            total = [121, 0, 0]
        else:
            total = [-1,2,4]
            return found[0]


if __name__ == '__main__':
    # to read name_list
    df = pd.read_excel(r'E:\study-1\first semester\11月\research\danwei.xlsx', encoding='utf-8')
    name_list = df['name']
    danwei_list = df['institution']
    zipped = zip(name_list, danwei_list)

    start = time.time()
    totals = []
    for pack in zipped:
        name = pack[0]
        ins = pack[1]
        target = get_totals(name, ins)
        totals.append(target)
        print('For %s, %s papers are found!' % (name, target))
    end = time.time()

    result = pd.DataFrame()
    result['name'] = name_list
    result['total'] = totals

    print(result)

    file_path = r'E:/Ipython/Machine Learning/research/data/articles.xlsx'
    writer = pd.ExcelWriter(file_path)
    result.to_excel(writer, index=True, encoding='utf-8', sheet_name='result')
    writer.save()
    print("Successfully Saved!")

    print("------> It costs %ss" % end)