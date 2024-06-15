import pytest
from vars import url_auth_page, url_main_page
from pages.auth_page import authorization
from pages.main_page import (check_elements_on_page, check_left_menu_items, check_filter_items, add_item_to_cart,
                             delete_item_from_cart)
from credentials import all_users, standard_user
from playwright.sync_api import Page

number_of_products_on_page = 6

@pytest.mark.auth
@pytest.mark.parametrize(*all_users)
def test_main_page_check_elements(page: Page, login, password):
    """Проверка элементов главной страницы"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    check_elements_on_page(page)
    check_left_menu_items(page)
    check_filter_items(page)


@pytest.mark.auth
@pytest.mark.parametrize(*all_users)
def test_log_out(page: Page, login, password):
    """Проверка деавторизации пользователя"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("#react-burger-menu-btn").click()
    page.get_by_text("Logout").click()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"


@pytest.mark.auth
@pytest.mark.parametrize(*all_users)
def test_counter_on_cart(page: Page, login, password):
    """Проверка работы счетчика на корзине"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    for i in range(number_of_products_on_page):
        expected_item_counter_on_cart = i+1
        current_item_counter_on_cart = add_item_to_cart(page, i)
        assert expected_item_counter_on_cart == current_item_counter_on_cart, \
            (f"Некорректное отображение счетчика на корзине. "
             f"ОР: {expected_item_counter_on_cart}, ФР: {current_item_counter_on_cart}")
    for i in reversed(range(number_of_products_on_page)):
        expected_item_counter_on_cart = i
        current_item_counter_on_cart = delete_item_from_cart(page, i)
        assert expected_item_counter_on_cart == current_item_counter_on_cart, \
            (f"Некорректное отображение счетчика на корзине. "
             f"ОР: {expected_item_counter_on_cart}, ФР: {current_item_counter_on_cart}")
