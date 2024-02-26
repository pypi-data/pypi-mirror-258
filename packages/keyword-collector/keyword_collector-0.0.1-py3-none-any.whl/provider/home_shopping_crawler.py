from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from selenium.webdriver.common.by import By

from datetime import datetime, timedelta

import time
import asyncio
import re

from utils import chrome_util


#categorys = ['생활·주방', '가전·디지털', '화장품·미용', '패션·잡화', '유아·아동', '여행·레저', '식품·건강보험']
categorys = ['생활·주방', '가전·디지털','화장품·미용', '식품·건강']

today = datetime.now()
tomorrow = today + timedelta(days=5)
date = tomorrow.strftime('%Y%m%d')
#date = '20240222'

five_days_ago = today- timedelta(days=1)
old_date = five_days_ago.strftime('%Y%m%d')


keywords =[]
remove = [ "▼가격인하▼전고객", "7일무료체험", "새봄맞이특별패키지","공영 단독 기획!", "작년 봄시즌 생방송 1회만에 종료.",  "방송중 10%앱할인+10%앱적립",  
           "방송패키지", "오직방송에서만", "쇼핑엔티 단독구성]", "백화점 동일상품" ,"전구성 10일 체험" ,"☆", "★", "렌탈", "운전자보험",
           "W쇼핑 단독구성", "홈쇼핑 특별구성", "◇","◆", "●", "방송에서만 추가구성", "무료상담예약", "○", "□", "■", "홈쇼핑 GS단독", "방송에서만 반값세일!",
           "1+1 세트", "시청자 정보", "방송에서만", "GS 단독", "CJ단독", "무료상담 신청", "무료상담신청", "w쇼핑", "단독구성", "방송에서만", "추가구성",
           "1+1세트", "초특가", "12개월분", "12개월", "신규", "반값세일!", "gs 9년만의 단독 패션 브랜드", "상담예약", "1+1", "최신상"]

remove_patterns = [
    r"[\[({◎★☆][^\[({◎★☆\])}]*[\])}◎★☆]", # (,{,[,☆,★,◎가 감싸고 있는 내용 제거
    r'\b\d+(\.\d+)?(kg|g|ml)\b',
    r'\b총?\s*\d+(개|알|박스|팩|미|마리|봉|통|포|구미|인용|주분|주|개월분)\b',
    r'[^a-zA-Z0-9가-힣\s]'
]

for category in categorys:
    try:
        url = f'https://hsmoa.com/?date={date}&site=&cate={category}'

        browser = chrome_util.create_driver()
        browser.get(url)
        time.sleep(1)

        # 상품 제목들 가져오기
        titles = browser.find_elements(By.CLASS_NAME, 'font-15')

        # 각 요소의 텍스트를 가져와서 리스트에 저장
        for title in titles:
            text = title.text

            # 패턴 제거
            for pattern in remove_patterns:
                text = re.sub(pattern, "", text)
            
            # 제거할 문자열이 포함되어 있으면 해당 문자열을 빈 문자열로 대체
            for word in remove:
                text = text.replace(word, "")
            
            text = text.split('+')[0]
            text = text.split('x')[0]
            text = text.split('X')[0]
            text = text.split('×')[0]
            text = text.split('/')[0]

            text = text.strip()

            # 공백 제거 후 빈 문자열이 아닌 경우에만 추가
            # 너무 길면 쓸모 없는 내용이 있을 확률이 높고, SEO에도 악영향을 줘서 2~15자 사이 키워드만
            if text != "" and len(text) < 16 and len(text) > 1:
                keywords.append(text)
                print(f'keyword appened : {text}')

        insert_hs_keywords(connection, date, keywords)
    except Exception as e:
        print(f'Error to crawling : {e}')
        asyncio.run(send_telegrame('telegram token', f'Crawling error for {category} hs keywords : {e}'))
        continue

new_keywords = get_date_hs_keywords(connection, date)
message = ''
for new_keyword in new_keywords:
    message = message + new_keyword + '\n'
    if len(message) > 300:
        asyncio.run(send_telegrame('telegram token', message))
        message=''
asyncio.run(send_telegrame('telegram token', message + f'New home shopping keywords are updated. {date}'))
close_database(connection)
browser.quit()