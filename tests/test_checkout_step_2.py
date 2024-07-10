import pytest
from playwright.sync_api import Page
from vars import url_auth_page, url_main_page, url_cart_page, url_checkout_step_1_page, url_checkout_step_2_page
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from pages.cart_page import CartPage
from pages.checkout_step_1_page import CheckoutStepOnePage
from pages.checkout_step_2_page import CheckoutStepTwoPage
from credentials import all_users, standard_user


@pytest.mark.checkout2
@pytest.mark.parametrize(*all_users)
def test_checkout_step_2_check_elements_empty(page, username, password):
    """Проверка элементов второй страницы проверки заказа (пустой)"""
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
    checkout_step_2_page = CheckoutStepTwoPage(page)
    checkout_step_2_page.checkout_step_2_check_elements_empty()


@pytest.mark.checkout2
@pytest.mark.parametrize(*all_users)
def test_checkout_step_2_check_elements_not_empty(page: Page, username, password):
    """Проверка элементов второй страницы проверки заказа (не пустой)"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    main_page = MainPage(page)
    main_page.add_item_to_cart_random()
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    number_of_items_on_cart = page.locator("div.cart_item").count()
    cart_page = CartPage(page)
    items_info_on_cart_page = cart_page.get_all_items_in_cart_info(number_of_items_on_cart)
    page.locator("#checkout").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    checkout_step_1_page = CheckoutStepOnePage(page)
    checkout_step_1_page.set_inputs_and_continue()
    assert page.url == url_checkout_step_2_page, f"Некорректный адрес. ОР: {url_checkout_step_2_page}, ФР: {page.url}"
    number_of_items_on_cart_checkout_2_page = page.locator("div.cart_item").count()
    assert number_of_items_on_cart == number_of_items_on_cart_checkout_2_page, \
        "Количество товаров в корзине и на странице проверки заказа не совпадает"
    checkout_step_2_page = CheckoutStepTwoPage(page)
    items_info_on_checkout_2_page = (
        checkout_step_2_page.get_all_items_info_checkout_2(number_of_items_on_cart_checkout_2_page))
    for i in range(number_of_items_on_cart):
        assert items_info_on_cart_page[i] == items_info_on_checkout_2_page[i], \
            (f"Информация о товаре в корзине и на странице проверки заказа не совпадает. "
             f"Корзина: {items_info_on_cart_page[i]}. Проверка заказа: {items_info_on_checkout_2_page[i]}")
    current_total_prices = checkout_step_2_page.get_current_total_prices()
    expected_total_prices = (checkout_step_2_page.get_expected_total_prices
                             (checkout_step_2_page.get_prices_of_items_in_cart(items_info_on_cart_page)))
    assert current_total_prices.get('current_item_total') == expected_total_prices.get('expected_item_total'), \
        (f"Некорректная сумма товаров. ОР: {expected_total_prices.get('expected_item_total')}, "
         f"ФР: {current_total_prices.get('current_item_total')}")
    assert current_total_prices.get('current_tax') == expected_total_prices.get('expected_tax'), \
        (f"Некорректное значение налога. ОР: {expected_total_prices.get('expected_tax')}, "
         f"ФР: {current_total_prices.get('current_tax')}")
    assert current_total_prices.get('current_total') == expected_total_prices.get('expected_total'), \
        (f"Некорректная общая сумма. ОР: {expected_total_prices.get('expected_total')}, "
         f"ФР: {current_total_prices.get('current_total')}")
