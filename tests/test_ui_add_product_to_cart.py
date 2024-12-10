import os

import allure
from dotenv import load_dotenv
from selene import browser, be, have

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


@allure.title('Добавление товара в корзину через UI, проверка его отображения на фронте и очистка корзины')
def test_ui_add_product_to_cart(browser_settings):
    with allure.step(f'Переход на сайт "/"'):
        browser.open('/')

    with allure.step(f'Переход в окно авторизации пользователя'):
        browser.element('.ico-login').click()

    with allure.step(f'Ввод значения в поле Email'):
        browser.element('#Email').should(be.blank).type(email)

    with allure.step(f'Ввод значения в поле Password'):
        browser.element('#Password').should(be.blank).type(password)

    with allure.step(f'Клик по кнопке Log in'):
        browser.element('[value="Log in"]').click()

    with allure.step(f'Проверка успешной авторизации'):
        browser.element('.account').should(have.text(email))

    with allure.step('Добавление товара в корзину'):
        browser.element(
            '//div[@class="product-item"][.//h2[@class="product-title"]/a[text()="14.1-inch Laptop"]]//input[@type="button" and @value="Add to cart"]').click()

    with allure.step('Переход на страницу Корзина'):
        browser.element('.cart-label').click()

    with allure.step('Проверка наличия товара в корзине'):
        browser.all('.product-name').with_(timeout=8).should(have.exact_texts('14.1-inch Laptop'))

    with allure.step('Удаление товаров из корзины'):
        browser.element('[name="removefromcart"]').click()
        browser.element('[name="updatecart"]').click()
        browser.element('.page-body').should(have.text('Your Shopping Cart is empty!'))
