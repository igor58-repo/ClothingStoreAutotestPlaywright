import pytest
from vars import url_auth_page, url_main_page
from pages.auth_page import auth_page_check_elements, authorization
from credentials import all_users
from playwright.sync_api import Page, expect


@pytest.mark.auth
def test_auth_page_check_elements(page: Page):
    """Проверка элементов страницы авторизации"""
    page.goto(url_auth_page)
    auth_page_check_elements(page)


@pytest.mark.auth
@pytest.mark.parametrize(*all_users)
def test_authorization(page: Page, login, password):
    """Проверка авторизации"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
