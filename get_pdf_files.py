import warnings
warnings.simplefilter("ignore", UserWarning)

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import os
import pandas as pd
import sys

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def get_links(name, institution):
    """" to get pdf_download_links"""
    # 设置浏览器
    driver = webdriver.PhantomJS(r"D:\anaconda2\Lib\phantomjs\bin\phantomjs.exe")
    user_agent = "Mozilla/5.0WindowsNT6.1WOW64AppleWebKit/535.8KHTML,likeGeckoBeamrise/17.2.0.9Chrome/17.0.939.0Safari/535.8"
    url = 'http://eng.oversea.cnki.net/kns55/brief/result.aspx?txt_1_value1=&txt_1_sel=%E4%B8%BB%E9%A2%98&dbPrefix=SCDB&db_opt=%E4%B8%AD%E5%9B%BD%E5%AD%A6%E6%9C%AF%E6%96%87%E7%8C%AE%E7%BD%91%E7%BB%9C%E5%87%BA%E7%89%88%E6%80%BB%E5%BA%93&db_value=%E4%B8%AD%E5%9B%BD%E6%9C%9F%E5%88%8A%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E5%8D%9A%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E4%BC%98%E7%A7%80%E7%A1%95%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E4%BC%9A%E8%AE%AE%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E5%9B%BD%E9%99%85%E4%BC%9A%E8%AE%AE%E8%AE%BA%E6%96%87%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E6%8A%A5%E7%BA%B8%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93%2C%E4%B8%AD%E5%9B%BD%E5%B9%B4%E9%89%B4%E7%BD%91%E7%BB%9C%E5%87%BA%E7%89%88%E6%80%BB%E5%BA%93&search-action=brief%2Fresult.aspx'
    driver.set_window_size(1920, 1080)

    # 等候10秒打开网页
    driver.implicitly_wait(10)
    driver.get(url)

    # select框框切换到第一作者
    element = driver.find_element_by_xpath(r"//*[@id='1_4']/a")
    element.click()

    # input name
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

    # click the search button
    element = driver.find_element_by_xpath(r'//*[@id="btnSearch"]')
    element.click()
    assert "No results found." not in driver.page_source

    # switch to iframe
    flag = False
    driver.switch_to.frame('iframeResult')
    driver.implicitly_wait(8)

    # show 50 results
    driver.find_element("id", "id_grid_display_num").click()
    driver.find_element("link text", '50').send_keys(Keys.ENTER)
    driver.implicitly_wait(8)

    # sorted by cites
    sort = driver.find_element_by_xpath(r'//*[@id="Form1"]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/span[4]/a')
    sort.send_keys(Keys.ENTER)

    # to fix the page
    driver.set_page_load_timeout(10)
    # html = driver.page_source

    # get all links
    link_list = []
    for link in driver.find_elements_by_tag_name("a"):
        link_list.append(link.get_attribute("href"))

    # get download_list
    links = []
    for link in link_list:
        if 'download.aspx?filename' in str(link):
            links.append(link)
    driver.close()

    return links


def download_files(url, path):
    """to download pdf files"""
    headers = {'User-Agent': "Mozilla/5.0WindowsNT6.1WOW64AppleWebKit/535.8KHTML,likeGeckoBeamrise/17.2.0.9Chrome/17.0.939.0Safari/535.8"}
    r = requests.get(url, timeout=50, stream=True, headers = headers)
    with open(path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1):
            fd.write(chunk)
    # to get file size
    size = file_size(path)
    while 'bytes' in size:
        print('Download error. Retry!')
        time.sleep(20)
        download_files(url, path)
        if 'bytes' not in size:
            break
    print("[hint!]--> Successful Downloaded!")

if __name__ == '__main__':
    # to read name_list
    df = pd.read_excel(r'E:\study-1\first semester\11月\research\danwei.xlsx', encoding='utf-8')
    name_list = df['name']
    danwei_list = df['institution']
    zipped = zip(name_list, danwei_list)

    start = time.time()
    paper_count = []
    for pack in zipped:
        name = pack[0]
        ins = pack[1]
        link_list = get_links(name, ins)
        while len(link_list) == 20:
            print('retry')
            link_list = get_links(name, ins)
            if len(link_list) != 20:
                break
        print('For %s, %s links are found!' % (name, len(link_list)))
        paper_count.append((name, len(link_list)))
        time.sleep(10)

        for num in range(len(link_list)):
            path = 'F:/down' + '/' + name
            if os.path.exists(path) == 0:
                os.makedirs(path)
            if len([name for name in os.listdir(path)]) != len(link_list):
                file_name = path + '/' + str(num) + '.pdf'
                link = link_list[num]
                if os.path.exists(file_name) == 0:
                    download_files(link, file_name)
                    time.sleep(3)
    end = time.time()

    print('It takes %s' % str(end))
    print(paper_count)