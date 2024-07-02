import pytest
from playwright.sync_api import Page, expect
from vars import url_auth_page, url_main_page, url_cart_page, url_checkout_step_1_page
from pages.auth_page import authorization
from credentials import all_users, standard_user
from pages.checkout_step_1_page import (check_elements, check_opened_failed_checkout_elements,
                                        close_failed_checkout_elements)

error_message_empty_first_name = "Error: First Name is required"
error_message_empty_last_name = "Error: Last Name is required"
error_message_empty_postal_code = "Error: Postal Code is required"
input_values = (f"first_name, last_name, postal_code, error_message",
                    [("", "1", "1", f"{error_message_empty_first_name}"),
                     ("1", "", "1", f"{error_message_empty_last_name}"),
                     ("1", "1", "", f"{error_message_empty_postal_code}")
                     ])


@pytest.mark.checkout1
@pytest.mark.parametrize(*all_users)
def test_checkout_step_1_check_elements(page: Page, login, password):
    """Проверка элементов первой страницы проверки заказа"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    page.locator("button#checkout").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    check_elements(page)


@pytest.mark.checkout1
@pytest.mark.parametrize(*input_values)
@pytest.mark.parametrize(*all_users)
def test_checkout_empty_first_name(page: Page, login, password, first_name, last_name, postal_code, error_message):
    """Проверка отображения первой страницы проверки заказа при незаполненном поле Имя"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    page.locator("button#checkout").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    check_elements(page)
    check_opened_failed_checkout_elements(page, first_name, last_name, postal_code, error_message)
    close_failed_checkout_elements(page)

