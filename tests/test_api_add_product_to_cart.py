import os
from utils.utils import response_logging, response_attaching
import allure
import requests
from dotenv import load_dotenv
from selene import browser, have


load_dotenv()
web_url = os.getenv('URL')
api_url = os.getenv('API_URL')
login = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


@allure.title('Добавление товара в корзину через API, проверка его отображения на фронте и очистка корзины')
def test_api_add_product_to_cart(browser_settings):
    with allure.step('Авториизация через API'):
        authorization = requests.post(url=api_url + '/login',
                                      data={'Email': login,
                                            'Password': password,
                                            'RememberMe': 'false'},
                                      allow_redirects=False
                                      )
        assert authorization.status_code == 302

    response_logging(authorization)
    response_attaching(authorization)

    with allure.step('Получение авторизационной куки'):
        cookie = authorization.cookies.get('NOPCOMMERCE.AUTH')

    with allure.step('Добавление товаров в корзину через API'):
        response = requests.post(url=api_url + '/addproducttocart/catalog/31/1/1',
                                 cookies={"NOPCOMMERCE.AUTH": cookie})

        assert response.status_code == 200

    with allure.step('Подстановка авторизационной куки в браузер'):
        browser.open('/')
        browser.driver.add_cookie({'name': 'NOPCOMMERCE.AUTH', 'value': cookie})
        browser.driver.refresh()

    with allure.step('Проверка успешной авторизации в браузере через API'):
        browser.element('.account').should(have.text(login))

    with allure.step('Переход на страницу Корзина'):
        browser.element('.cart-label').click()

    with allure.step('Проверка наличия товара в корзине'):
        browser.all('.product-name').with_(timeout=8).should(have.exact_texts('14.1-inch Laptop'))

    with allure.step('Удаление товаров из корзины'):
        browser.element('[name="removefromcart"]').click()
        browser.element('[name="updatecart"]').click()
        browser.element('.page-body').should(have.text('Your Shopping Cart is empty!'))
