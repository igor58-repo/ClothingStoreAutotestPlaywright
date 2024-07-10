import pytest
from playwright.sync_api import Page
from vars import (url_auth_page, url_main_page, url_cart_page, url_checkout_step_1_page, url_checkout_step_2_page,
                  url_checkout_complete_page)
from pages.auth_page import AuthPage
from pages.checkout_step_1_page import CheckoutStepOnePage
from pages.finish_page import FinishPage
from credentials import all_users, standard_user


@pytest.mark.finish
@pytest.mark.parametrize(*all_users)
def test_finish_check_elements_empty(page, username, password):
    """Проверка элементов финальной страницы оформления заказа"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    page.locator("button#checkout").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    checkout_step_1_page = CheckoutStepOnePage(page)
    checkout_step_1_page.set_inputs_and_continue()
    assert page.url == url_checkout_step_2_page, f"Некорректный адрес. ОР: {url_checkout_step_2_page}, ФР: {page.url}"
    page.locator("button#finish").click()
    assert page.url == url_checkout_complete_page, (f"Некорректный адрес. ОР: {url_checkout_complete_page}, "
                                                    f"ФР: {page.url}")
    finish_page = FinishPage(page)
    finish_page.check_elements()
    page.locator("button#back-to-products").click()
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
