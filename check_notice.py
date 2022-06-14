import os
import re
import pandas as pd
import pickle
import collections
from collections import defaultdict
import numpy as np
import math
from ast import literal_eval
from time import gmtime, strftime
import re
import time
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import requests
import json

# Scrapping
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

options = Options()
ua = UserAgent()
userAgent = ua.chrome
print(userAgent)

options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument(f"user-agent={userAgent}")


# Error Handling
import socket
import urllib3
import urllib.request
from urllib.request import urlopen
from urllib.parse import quote_plus
from urllib.request import urlretrieve
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
import warnings
warnings.filterwarnings('ignore')

import requests
import json

if __name__ == '__main__':
	while True:
		tit_lst = check_notice()
		new_idx = new_notice(tit_lst)

		if new_idx != None:
			status_code = send_message(new_idx)
		else:
			continue


def check_notice():
    seoultech_notice_url = 'https://www.seoultech.ac.kr/service/info/matters/'

    res = requests.get(seoultech_notice_url)
    time.sleep(3)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    tit_lst = [tit.text.strip() for tit in soup.find_all('td', {'class':'tit dn2'})]
    with open('tit_lst.pkl', 'wb') as f:
        pickle.dump(tit_lst, f)

    return tit_lst


def new_notice(tit_lst):
    with open('tit_lst.pkl', 'rb') as f:
        tit_lst_prev = pickle.load(f)

    if tit_lst_prev != tit_lst:
        return [tit_lst.index(n) for m, n in zip(tit_lst_prev, tit_lst) if n != m][0]
    else:
        return None


def send_message(idx):
    new_notice_tit = soup.find_all("tr", {'class':'body_tr'})[idx].a.text.strip()
    new_notice_url = 'https://www.seoultech.ac.kr/service/info/matters/' + \
                                soup.find_all("tr", {'class':'body_tr'})[idx].a['href']

    with open("kakao_token.json","r") as fp:
        tokens = json.load(fp)

    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

    # kapi.kakao.com/v2/api/talk/memo/default/send

    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }

    data={
        "template_object": json.dumps({
            "object_type": "text",
            "text": "새로운 공지사항이 등록되었습니다.\n\n[" + new_notice_tit + "]\n\n" + new_notice_url,
            "link": {
                "web_url" : new_notice_url,
                "mobile_web_url" : new_notice_url
            },
            "button_title" : "공지사항 보러가기"
        })
    }

    response = requests.post(url, headers=headers, data=data)
    return(response.status_code)