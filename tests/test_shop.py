"""
UI test for test.qa.studio
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tests.helper.common import CommonHelper


url = "https://testqastudio.me/"

def test_product_view_sku(browser):
    """
    Test case WERT-1
    """
		
	# определяем адрес страницы для теста и переходим на неё
    browser.get(url=url)
    
	# ищем по селектору элемент меню "Бестселлеры" и кликаем по нему
    browser.find_element(by=By.CSS_SELECTOR, value="[class*='tab-best_sellers']").click()
    
	# ищем по селектору карточку "ДИВВИНА Журнальный столик" и кликаем по нему
    browser.find_element(By.LINK_TEXT, value= 'ДИВВИНА Журнальный столик').click()
    
	# ищем по имени класса артикул для "ДИВВИНА Журнальный столик"
    article_table = browser.find_element(By.CLASS_NAME, value="sku")
    
	# проверяем соответствие
    assert article_table.text == 'C0MSSDSUMK', 'Артикул не соответствует ожидаемому'
    
    
def test_top_menu(browser):
    """
    Test case TC-1
    """

    # определяем функцию, как список навигационного меню
    expected_menu = ['Каталог', 'Блог', 'О компании', 'Контакты']

    # ищем блок навигационного меню и элементы с текстами кнопок
    browser.get(url)
    elements = browser.find_elements(by=By.CSS_SELECTOR, value="[id='menu-primary-menu'] li a")

    # определяем функцию результатов, как список текстовых данных с каждого найденного элемента
    result = [el.get_attribute('text') for el in elements]

    # сравниваем найденные тексты названий кнопок меню с ожидаемыми
    assert expected_menu == result, 'Навигацинное меню не соответствует ожидаемому'


@pytest.mark.xfail(reason="В ожидании фикса")
def test_products_group(browser):
    """
    Test case TC-2
    """
    # определяем через функцию список меню
    expected_menu = [
        ("Все", "", "[class='tab-all active']"), 
        ("Бестселлеры", "/?products_group=best_sellers", "[class*='tab-best_sellers ']"),
        ("Горячие товары", "/?products_group=featured", "[class='tab-featured']"),
        ("Новые товары", "/?products_group=new", "[class='tab-new ']"),
        ("Распродажа товаров", "/?products_group=sale", "[class='tab-sale ']")
    ]

    browser.get(url)
    # находим список элементы меню и сравниваем количество ожидаемых и фактических элементов в меню
    menu_element = "[class='catalog-toolbar-tabs__content'] a"
    elements = browser.find_elements(by=By.CSS_SELECTOR, value=menu_element)
    assert len(elements) == len(expected_menu), "Количество элементов меню не соответствует ожидаемому"
    
    # ищем каждый из элементов в ожидаемом меню по css селектору и кликаем на него
    for item in expected_menu:
        element = browser.find_element(by=By.CSS_SELECTOR, value=item[2])
        element.click()

    # определяем функцию результатов, как список текстовых данных с каждого найденного элемента
    result = [el.get_attribute('text') for el in elements]
    
    # создаем список проверки из названий кнопок из списка ожидаемого меню и сравниваем 
    expected_result = []
    for item in expected_menu:
        expected_result.append(item[0])
    assert expected_result == result, 'Элементы меню не соответствуют ожидаемым'

def test_count_of_all_products(browser):
    """
    Test case TC-3
    """
    browser.get(url)

    # осуществляем прокручивание страницы в низ
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ищем кнопку "Показать больше" и нажимаем на неё
    button_show_more = browser.find_element(by=By.ID, value='razzi-catalog-previous-ajax')
    button_show_more.click()

    # проверяем в теч 10 сек, каждые 2 сек что в элементе присутсвует текст
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "razzi-posts__found"), "Показано 16 из 16 товары"))

    # ищем список продуктов и проверяем их итоговое количество в ассерте
    elements = browser.find_elements(by=By.CSS_SELECTOR, value="[id='rz-shop-content'] ul li")
    assert len(elements) == 16, "Количество элементов не соответствует ожидаемому"

def test_right_way(browser):
    """
    Test case TC-4
    """
    browser.get(url)
    
    # осуществляем прокручивание страницы в низ
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ищем кнопку "Показать больше" и нажимаем на неё
    button_show_more = browser.find_element(by=By.ID, value='razzi-catalog-previous-ajax')
    button_show_more.click()

    # проверяем в теч 10 сек, каждые 2 сек что в элементе присутсвует текст количества показанных товаров
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "razzi-posts__found"), "Показано 16 из 16 товары"))

    # находим иконку быстрого просмотра ДИВВИНА Журнальный столик и кликаем по ней
    product = browser.find_element(by=By.CSS_SELECTOR, value="[class*='post-11094'] a.quick-view-button.rz-loop_button")
    ActionChains(browser).move_to_element(product).perform()
    product.click()

    # ждём 10 сек с проверкой каждые 2 сек, пока кнопка добавления в корзину станет активна и кликаем на неё
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="add-to-cart"]')))
    browser.find_element(by=By.CSS_SELECTOR, value='[name="add-to-cart"]').click()

    # ждём 10 сек с проверкой каждые 2 сек, пока всплывающее окно корзины станет активно 
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='cart-modal']")))

    # ищем кнопку закрытия окна быстрого просмотра и кликаем на неё
    browser.find_element(by=By.CSS_SELECTOR, value='[class="button-close active"]').click()

    # проверяем, что всплывающее окно корзины всё ещё активно по css-свойству
    cart_is_visible = browser.find_element(
        By.XPATH, value="//div[@id='cart-modal']").value_of_css_property("display")
    assert cart_is_visible == "block", "Окно корзины неактивно"

    # ищем кнопку "оформление заказа" и кликаем на неё
    browser.find_element(by=By.CSS_SELECTOR, value='p [class*="button checkout"]').click()
    
    # ждем 10 сек с проверкой каждые 1 сек, пока не прогрузится страница (по пути)
    WebDriverWait(browser, timeout=10, poll_frequency=1).until(EC.url_to_be(f"{url}checkout/"))

    # вводим данные пользователя для заказа 
    common_helper = CommonHelper(browser)
    common_helper.enter_input(input_id="billing_first_name", data="Andrey")
    common_helper.enter_input(input_id="billing_last_name", data="Ivanov")
    common_helper.enter_input(input_id="billing_address_1", data="2-26, Sadovaya street")
    common_helper.enter_input(input_id="billing_city", data="Moscow")
    common_helper.enter_input(input_id="billing_state", data="Moscow")
    common_helper.enter_input(input_id="billing_postcode", data="122457")
    common_helper.enter_input(input_id="billing_phone", data="+79995784256")
    common_helper.enter_input(input_id="billing_email", data="andrey.i@mail.ru")

    # ждем 10 сек с проверкой каждые 1 сек, пока блок с кнопкой "подтвердить заказ" не станет активным (по свойствам css) и кликаем на кнопку
    payments_el = '//*[@id="payment"] [contains(@style, "position: static; zoom: 1;")]'
    WebDriverWait(browser, timeout=10, poll_frequency=1).until(
        EC.presence_of_element_located((By.XPATH, payments_el)))
    browser.find_element(by=By.ID, value="place_order").click()

    # ждем 10 сек с проверкой каждые 1 сек, пока не прогрузится страница подтверждения заказа (по пути)
    WebDriverWait(browser, timeout=10, poll_frequency=1).until(EC.url_contains(f"{url}checkout/order-received/"))
    
    # ждём наличие текста подтвердающего оформление заказа и проверяем его через ассерт
    result = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "p.woocommerce-thankyou-order-received"), \
            "Ваш заказ принят. Благодарим вас."))

    assert result, 'Текст подтверждения не соответствует ожидаемому'
