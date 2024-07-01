import pytest
from playwright.sync_api import Page, expect
from vars import (url_auth_page, url_main_page, url_cart_page, url_checkout_step_1_page, url_checkout_step_2_page,
                  number_of_products_on_page)
from pages.auth_page import authorization
from credentials import all_users, standard_user, problem_user
from pages.main_page import add_item_to_cart_random
from pages.cart_page import get_all_items_in_cart_info
from pages.checkout_step_1_page import set_inputs_and_continue
from pages.checkout_step_2_page import (check_elements_empty, get_all_items_info_checkout_2, get_prices_of_items_in_cart,
                                        get_item_total, get_tax, get_total)


@pytest.mark.checkout2
@pytest.mark.parametrize(*all_users)
def test_checkout_step_2_check_elements_empty(page: Page, login, password):
    """Проверка элементов второй страницы проверки заказа (пустой)"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    page.locator("#checkout").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    set_inputs_and_continue(page)
    assert page.url == url_checkout_step_2_page, f"Некорректный адрес. ОР: {url_checkout_step_2_page}, ФР: {page.url}"
    check_elements_empty(page)

@pytest.mark.new
@pytest.mark.checkout2
@pytest.mark.parametrize(*all_users)
def test_checkout_step_2_check_elements_empty(page: Page, login, password):
    """Проверка элементов второй страницы проверки заказа (не пустой)"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    add_item_to_cart_random(page, number_of_products_on_page)
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    number_of_products_on_cart = page.locator("div.cart_item").count()
    items_info_on_cart_page = get_all_items_in_cart_info(page, number_of_products_on_cart)
    page.locator("#checkout").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    set_inputs_and_continue(page)
    assert page.url == url_checkout_step_2_page, f"Некорректный адрес. ОР: {url_checkout_step_2_page}, ФР: {page.url}"
    number_of_products_on_cart_checkout_2_page = page.locator("div.cart_item").count()
    assert number_of_products_on_cart == number_of_products_on_cart_checkout_2_page, \
        "Количество товаров в корзине и на странице проверки заказа не совпадает"
    items_info_on_checkout_2_page = get_all_items_info_checkout_2(page, number_of_products_on_cart_checkout_2_page)
    for i in range(number_of_products_on_cart):
        assert items_info_on_cart_page[i] == items_info_on_checkout_2_page[i], \
            (f"Информация о товаре в корзине и на странице проверки заказа не совпадает. "
             f"Корзина: {items_info_on_cart_page[i]}. Проверка заказа: {items_info_on_checkout_2_page[i]}")
    prices = get_prices_of_items_in_cart(items_info_on_cart_page)
    current_item_total = float(page.locator("div.summary_subtotal_label").inner_text().split('$')[1])
    current_tax = float(page.locator("div.summary_tax_label").inner_text().split('$')[1])
    current_total = float(page.locator("div.summary_total_label").inner_text().split('$')[1])
    expected_item_total = get_item_total(prices)
    expected_tax = get_tax(expected_item_total)
    expected_total = get_total(expected_item_total, expected_tax)
    assert current_item_total == expected_item_total, \
        f"Некорректная сумма товаров. ОР: {expected_item_total}, ФР: {current_item_total}"
    assert current_tax == expected_tax, \
        f"Некорректное значение налога. ОР: {current_tax}, ФР: {expected_tax}"
    assert current_total == expected_total, \
        f"Некорректная общая сумма. ОР: {expected_total}, ФР: {current_total}"
