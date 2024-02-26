from selenium.webdriver.common.by import By

from model.keyword_model import Keyword
from utils import chrome_util
from enum import Enum

import time

class Category(Enum):
    패션의류 = ('패션의류', 1)
    패션잡화 = ('패션잡화', 2)
    화장품미용 = ('화장품/미용', 3)
    디지털가전 = ('디지털/가전', 4)
    가구인테리어 = ('가구/인테리어', 5)
    출산육아 = ('출산/육아', 6)
    식품 = ('식품', 7)
    스포츠레저 = ('스포츠/레저', 8)
    생활건강 = ('생활/건강', 9)
    여가생활편의 = ('여가/생활편의', 10)
    면세점 = ('면세점', 11)
    도서 = ('도서', 12)

class Device(Enum):
    전체 = '//*[@id="18_device_0"]'
    PC = '//*[@id="18_device_1"]'
    모바일 = '//*[@id="18_device_2"]'

class Gender(Enum):
    전체 = '//*[@id="19_gender_0"]'
    여성 = '//*[@id="19_gender_1"]'
    남성 = '//*[@id="19_gender_2"]'

class Age(Enum):
    전체 = '//*[@id="20_age_0"]'
    십대 = '//*[@id="20_age_1"]'
    이십대 = '//*[@id="20_age_2"]'
    삼십대 = '//*[@id="20_age_3"]'
    사십대 = '//*[@id="20_age_4"]'
    오십대 = '//*[@id="20_age_5"]'
    육십대_이상 = '//*[@id="20_age_6"]'

url = 'https://datalab.naver.com/shoppingInsight/sCategory.naver'

class KeywordNaverDataLab:
    def __init__(self, categorys=Category, device=Device.전체, gender=Gender.전체, age = Age.전체):
        self.categorys = categorys
        self.device = device
        self.gender = gender
        self.age = age

    def set_categorys(self, categorys):
        self.categorys = categorys

    def set_device(self, device):
        self.device = device

    def set_gender(self, gender):
        self.gender = gender

    def set_age(self, age):
        self.age = age

    def get_keywords(self, categorys = None, device = None, gender = None, age = None):
        if categorys is not None:
            self.categorys = categorys

        if device is not None:
            self.device = device

        if gender is not None:
            self.gender = gender

        if age is not None:
            self.age = age

        driver = chrome_util.create_driver()
        driver.get(url)
        time.sleep(1)

        driver.find_element(By.XPATH, self.device.value).click()
        driver.find_element(By.XPATH, self.gender.value).click()
        driver.find_element(By.XPATH, self.age.value).click()

        for category in self.categorys:
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click()

            category_name = category.value[0]
            driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[{category.value[1]}]/a').click()
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a').click()

            keywords = []
            # 25페이지 / 페이지당 20개 / 초 500개
            for i in range(0,25): 
            #for i in range(0,13): # 13 * 20 = 260개 추출
                for j in range(1,21): # 한 페이지 20개 키워드 저장
                    path = f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{j}]/a'
                    result = driver.find_element(By.XPATH, path).text
                    result = result.split('\n')

                    keywords.append(Keyword(result[1], category_name))
                    time.sleep(0.1)
                driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]').click()
                time.sleep(0.1)

        driver.quit()

        for keyword in keywords:
            print(keyword)

        return keywords

    def get_all_keywords(self):
        keywords = self.get_keywords(Category, Device.전체, Gender.전체, Age.전체)

        return keywords
