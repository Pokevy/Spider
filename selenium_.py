import random
import time
import pymysql
import requests
import selenium.common
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd


class Pok:

    def __init__(self):
        self.room = []
        self.area = []
        self._type = []
        self.floor = []
        self.stype = []
        self.address = []
        self.money = []
        self.link = []
        self.options = webdriver.EdgeOptions()  # 实例化浏览器选项类
        self.options.add_experimental_option("detach", True)  # 设置浏览器不关闭
        self.driver = webdriver.Edge(options=self.options)  # 实例化浏览器驱动

    def get_url(self, url):
        url_list = []
        self.driver.get(url)  # 访问网页
        WebDriverWait(self.driver, 600).until(lambda x: x.find_element(By.XPATH, '//*[@id="list-content"]'))  # 等待全局元素
        urls = self.driver.find_elements(By.XPATH, '//*[@id="list-content"]/div/div[1]/h3/a')  # 获取当前页面所有元素
        for i in urls:
            url_list.append(i.get_attribute("href"))
        return url_list

    def get_info(self, url):
        a = 1
        for j in self.get_url(url):
            time.sleep(random.randint(1, 3))
            self.driver.get(j)
            try:
                WebDriverWait(self.driver, 600).until(
                    lambda x: x.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/ul[1]'))
                room = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/ul[1]/li[2]/span[2]').text
                area = self.driver.find_element(By.XPATH,
                                                '/html/body/div[3]/div[2]/div[1]/ul[1]/li[3]/span[2]/b').text
                _type = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/ul/li[1]').text
                floor = self.driver.find_element(By.XPATH,
                                                 '/html/body/div[3]/div[2]/div[1]/ul[1]/li[5]/span[2]').text
                stype = self.driver.find_element(By.XPATH,
                                                 '/html/body/div[3]/div[2]/div[1]/ul[1]/li[6]/span[2]').text
                address = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/ul[1]/li[8]/a[1]').text
                money = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/span[1]/em/b').text
                link = j
                print(
                    f"户型:{room}\n租型:{_type}\n面积:{area}\n楼层:{floor}\n装修:{stype}\n地址:{address}\n租金:{money}\n链接:{j}\n")
                self.save_mysql(a, room, area, _type, floor, stype, address, money, link)
                a += 1
            except selenium.common.exceptions:
                pass

    def save_mysql(self, a, room, area, _type, floor, stype, address, money, link):
        con = pymysql.connections.Connection(host='127.0.0.1', user='root', password='root', db='demo')
        cur = con.cursor()
        sql = "insert into house values(%s ,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql, [a, room, area, _type, floor, stype, address, money, link])
        con.commit()
        cur.close()
        con.close()

    def save_csv(self):
        _dict = {
            '户型': self.room,
            '租型': self._type,
            '面积': self.area,
            '楼层': self.floor,
            '装修': self.stype,
            '地址': self.address,
            '租金': self.money,
            '链接': self.link
        }
        dataframe = pd.DataFrame(_dict)
        dataframe.to_csv("demo.csv", encoding='utf-8', index=False, sep=',')


pok = Pok()
for i in range(2, 10):
    pok.get_info(f'https://wh.zu.anjuke.com/fangyuan/jiangxiat/p{i}')


def main():
    response=requests.request()
    print(response.status_code)

