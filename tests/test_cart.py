import pytest
from playwright.sync_api import Page, expect
from vars import url_auth_page, url_main_page, url_cart_page, number_of_items_on_page
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from pages.cart_page import CartPage
from credentials import all_users, standard_user


@pytest.mark.cart
@pytest.mark.parametrize(*all_users)
def test_empty_cart_page_check_elements(page, username, password):
    """Проверка элементов страницы корзины (пустой)"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    cart_page = CartPage(page)
    cart_page.check_elements_cart("empty")


@pytest.mark.cart
@pytest.mark.parametrize(*all_users)
def test_not_empty_cart_page_check_elements(page, username, password):
    """Проверка элементов страницы корзины (не пустой)"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    items_numbers = main_page.add_item_to_cart_random()
    number_of_items_on_cart = len(items_numbers)
    items_info_on_main_page = main_page.get_specific_items_info_without_img(items_numbers)
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    cart_page = CartPage(page)
    cart_page.check_elements_cart("not_empty")
    expect(page.locator("div.cart_item"), f"Некорректное количество товаров корзине. "
                                          f"ОР: {number_of_items_on_cart}").to_have_count(number_of_items_on_cart)
    items_info_on_cart_page = cart_page.get_all_items_in_cart_info(number_of_items_on_cart)
    for i in range(len(items_info_on_cart_page)):
        assert items_info_on_cart_page[i] == items_info_on_main_page[i], \
            f"Некорректные данные в корзине. ОР: {items_info_on_main_page[i]}, ФР: {items_info_on_cart_page[i]}"


@pytest.mark.cart
@pytest.mark.parametrize(*all_users)
def test_remove_from_cart(page: Page, username, password):
    """Проверка удаления товаров из корзины"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    items_numbers = main_page.add_item_to_cart_random()
    number_of_items_on_cart = len(items_numbers)
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    cart_page = CartPage(page)
    cart_page.check_elements_cart("not_empty")
    expect(page.locator("div.cart_item"), f"Некорректное количество товаров корзине. "
                                          f"ОР: {number_of_items_on_cart}").to_have_count(number_of_items_on_cart)
    cart_page.delete_all_items_from_cart(number_of_items_on_cart)
    cart_page.check_elements_cart("empty")
    page.locator("button#continue-shopping").click()
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    expect(page.locator("span.shopping_cart_badge"), "Счетчик на корзине не должен отображаться").not_to_be_visible()
    for i in range(number_of_items_on_page):
        expect(page.locator("button.btn_inventory").nth(i), "Товар не удален из корзины").to_have_text("Add to cart")
