import os
import allure
import requests
from dotenv import load_dotenv
from selene import browser, have
from utils.utils import response_logging, response_attaching

load_dotenv()
web_url = os.getenv('URL')
api_url = os.getenv('API_URL')
login = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


@allure.title('Авторизация пользователя через API и проверка успешной авторизации в браузере')
def test_authorization_with_api(browser_settings):
    with allure.step('Авториизация через API'):
        result = requests.post(url=api_url + '/login',
                               data={'Email': login,
                                     'Password': password,
                                     'RememberMe': 'false'},
                               allow_redirects=False
                               )
    assert result.status_code == 302
    response_logging(result)
    response_attaching(result)

    with allure.step('Получение авторизационной куки'):
        cookie = result.cookies.get('NOPCOMMERCE.AUTH')

    with allure.step('Подстановка авторизационной куки в браузер'):
        browser.open('/')
        browser.driver.add_cookie({'name': 'NOPCOMMERCE.AUTH', 'value': cookie})
        browser.open("/")

    with allure.step('Проверка успешной авторизации в браузере через API'):
        browser.element('.account').should(have.text(login))
