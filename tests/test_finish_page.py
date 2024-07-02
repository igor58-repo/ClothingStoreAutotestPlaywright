import pytest
from playwright.sync_api import Page, expect
from vars import (url_auth_page, url_main_page, url_cart_page, url_checkout_step_1_page, url_checkout_step_2_page,
                  url_checkout_complete_page)
from pages.auth_page import authorization
from credentials import all_users, standard_user
from pages.checkout_step_1_page import set_inputs_and_continue
from pages.finish_page import check_elements


@pytest.mark.finish
@pytest.mark.parametrize(*all_users)
def test_finish_check_elements_empty(page: Page, login, password):
    """Проверка элементов финальной страницы оформления заказа"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    page.locator("#checkout").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    set_inputs_and_continue(page)
    assert page.url == url_checkout_step_2_page, f"Некорректный адрес. ОР: {url_checkout_step_2_page}, ФР: {page.url}"
    page.locator("button#finish").click()
    assert page.url == url_checkout_complete_page, (f"Некорректный адрес. "
                                                    f"ОР: {url_checkout_complete_page}, ФР: {page.url}")
    check_elements(page)
    page.locator("button#back-to-products").click()
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
