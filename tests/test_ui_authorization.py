import os

import allure
from dotenv import load_dotenv
from selene import browser, be, have

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


@allure.title('Авторизация пользователя через UI')
def test_ui_authorization(browser_settings):
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
