import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def wait_xpath(driver, xpath):
    try:
        wait = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        return wait
    except TimeoutException:
        print("Не дождались появления панели на форме " + xpath)


def wait_file_xpath(driver, xpath):
    try:
        wait = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return wait
    except TimeoutException:
        print("Не дождались появления панели на форме " + xpath)



def click_xpath(driver, xpath):
    driver.find_element_by_xpath(xpath).click()
    
def wait_and_click_xpath(driver, xpath):
    tmp = wait_xpath(driver, xpath)
    tmp.click()

def send_keys_xpath(driver, xpath, keys):
    tmp = wait_xpath(driver, xpath)
    #tmp.clear()
    tmp.send_keys(keys)

class ServiceTests(unittest.TestCase):
    def setUp(self):
        # Открываем портал логина в ЕСИА
        self.driver = webdriver.Chrome("C:/Users/maxim.rublev/Documents/selenium/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get("https://www.gosuslugi.ru/")
        # Проверяем успешность открытия портала
        assert "Портал государственных услуг Российской Федерации" \
            in self.driver.title
        
        # Входим в личный кабинет для логина
        sign_in_register = "//*[@id='header']/div[2]/div/ul/li[6]"
        wait_xpath(self.driver, sign_in_register)
        click_xpath(self.driver, sign_in_register)
        
        # Вводим данные логина и пароль
        send_keys_xpath(self.driver,
            '//*[@id="mobileOrEmail"]', 'rublevmr@gmail.com')
        send_keys_xpath(self.driver,
            '//*[@id="password"]', 'GosUslugi3')
        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)
        # Проверяем залогинились ли мы в системе
        assert "Портал государственных услуг Российской Федерации" \
            in self.driver.title
        
        # Переключаемся во фрейм "Каталог государственных сайтов"
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.frame_to_be_available_and_switch_to_it(0))
        #Открываем всплывающее окно выбора 
        wait_and_click_xpath(self.driver, '//*[@id="locationButton"]')
        # Возвращаемся обратно в родительский фрейм
        self.driver.switch_to.default_content()
        
        # Дожидаемся появления всплывающего окна и нажимаем кнопку "Выбрать вручную"
        wait_and_click_xpath(self.driver,
            '//*[@id="ngdialog1"]/*//div[.="Выбрать вручную"]')
        
        # Вводим название региона
        send_keys_xpath(self.driver,
            '//*[@id="_epgu_el5_input"]', 'Магаданская область')
        # Выбираем Магаданскую область
        wait_and_click_xpath(self.driver,
            '//div[@class="dropdown-el"]/ul/li[.="Магаданская область"]')
        # Нажимаем кнопку "Сохранить" для выбора местоположения
        click_xpath(self.driver,
            '//*[@id="ngdialog1"]/*//a[.="Сохранить"]')
        
        # Проверяем вернулись ли мы на главную страницу
        assert "Портал государственных услуг Российской Федерации" \
            in self.driver.title

    
    def test_case(self):
        #Переходим по ссылке на услугу(соц поддержка малоимущих граждан)
        self.driver.get(" https://www.gosuslugi.ru/20165/1/info ")
        # Переходим к получению услуги
        GetUsl_xpath = "//*[@id='content']/*//a[.='Получить услугу']"
        wait_file_xpath(self.driver, GetUsl_xpath)
        wait_and_click_xpath(self.driver,
            "//*[@id='content']/*//a[.='Получить услугу']")
