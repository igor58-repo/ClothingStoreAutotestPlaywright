import pytest
from vars import url_auth_page, url_main_page
from pages.auth_page import (auth_page_check_elements, authorization, check_opened_failed_auth_elements,
                             close_failed_auth_elements)
from credentials import all_users, non_existent_user, locked_out_user, empty_login, empty_password
from playwright.sync_api import Page
error_message_non_existent_user = "Epic sadface: Username and password do not match any user in this service"
error_message_locked_out_user = "Epic sadface: Sorry, this user has been locked out."
error_message_empty_login = "Epic sadface: Username is required"
error_message_empty_password = "Epic sadface: Password is required"


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


@pytest.mark.auth
@pytest.mark.parametrize(*non_existent_user)
def test_authorization_non_existent_user(page: Page, login, password):
    """Проверка авторизации несуществующим пользователем"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    check_opened_failed_auth_elements(page, error_message_non_existent_user)
    close_failed_auth_elements(page)


@pytest.mark.auth
@pytest.mark.parametrize(*locked_out_user)
def test_authorization_locked_out_user(page: Page, login, password):
    """Проверка авторизации заблокированным пользователем"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    check_opened_failed_auth_elements(page, error_message_locked_out_user)
    close_failed_auth_elements(page)


@pytest.mark.auth
@pytest.mark.parametrize(*empty_login)
def test_authorization_empty_login(page: Page, login, password):
    """Проверка авторизации с незаполненным полем Логина"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    check_opened_failed_auth_elements(page, error_message_empty_login)
    close_failed_auth_elements(page)


@pytest.mark.auth
@pytest.mark.parametrize(*empty_password)
def test_authorization_empty_password(page: Page, login, password):
    """Проверка авторизации с незаполненным полем Пароль"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    check_opened_failed_auth_elements(page, error_message_empty_password)
    close_failed_auth_elements(page)
