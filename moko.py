import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import logging
import os
import hashlib
import time
import random
logger = logging.getLogger()
STORAGE_URL = r'C:\STORAGE'
URL = 'http://www.moko.cc/channels/post/23/{}.html'
BASE_URL = 'http://www.moko.cc'
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Cookie':'JSESSIONID=1AF10F45B63ECA4ED8C5537FA34BBE65; Hm_lvt_8d82e75c6168ba4bc0135a08edae2a2e=1566697643; Hm_lpvt_8d82e75c6168ba4bc0135a08edae2a2e=1566698188; NEWMOKO_USER_LOGINKEY=947f9deb-de75-4d52-8b83-627faa45e535',
}



def get_content(url,headers):
    """
    获取列表页的html。

    """
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        return r.text


def get_individuals(content):
    """
    通过beautifulsoup，获取列表页的每个个体的相关信息
    :return:
    """
    soup = BeautifulSoup(content,'lxml')
    individuals_uls = soup.find_all(name='ul',class_='post small-post')
    individuals = []

    for individuals_ul in individuals_uls:
        # logger.info('individuals_ul',individuals_ul)
        url = BASE_URL + individuals_ul.find(name='a').attrs['href']
        logger.info('url',url)
        name = individuals_ul.find(name='a',class_='nickname').attrs['title']
        logger.info('name',name)
        individuals.append({'url':url,'name':name})
    return individuals



def get_download_links(content):
    links = []

    for p in BeautifulSoup(content,'lxml').find_all(name='p',class_='picBox'):

        link = p.img.attrs['src2']
        links.append(link)
    return links

def download(link,name):

    r = requests.get(link,headers=HEADERS)
    md5 = hashlib.md5()
    md5.update(link.encode('utf-8'))
    file_name = md5.hexdigest()+'.jpg'
    if not os.path.exists(os.path.join(STORAGE_URL,name,file_name)):
        f = open(os.path.join(STORAGE_URL,name,file_name),'wb')

        f.write(r.content)
        f.close()
        print('download succeed')




def create_dir(name):
    if not os.path.exists(os.path.join(r'C:\STORAGE',name)):
        os.makedirs(os.path.join(r'C:\STORAGE',name))



for i in range(1,20):
    START_URL = URL.format(i)

    content = get_content(START_URL,HEADERS)
    if content:
        individuals = get_individuals(content)
        for individual in individuals:

            name = individual['name']
            create_dir(name)
            indi_content = get_content(individual['url'],headers=HEADERS)
            links = get_download_links(indi_content)
            for link in links:
                time.sleep(random.randint(1,6))

                download(link,name)




