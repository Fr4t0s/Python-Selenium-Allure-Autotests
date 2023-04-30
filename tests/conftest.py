"""
Configuration test
"""
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def browser():
    """
    Main fixture
    """
     # описываем опции запуска браузера
    chrome_options = Options()
    #chrome_options.add_argument("start-maximized") # открываем на полный экран
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars") # отключаем инфо сообщения
    chrome_options.add_argument("--disable-extensions") # отключаем расширения
    chrome_options.add_argument("--window-size=2560,1080") # необходимо для функционирования скрытого режима без запуска окна браузера
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless") # спец. режим без запуска окна браузера

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()
