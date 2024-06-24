import pytest
from playwright.sync_api import Page, expect
from vars import url_auth_page, url_main_page, url_cart_page, number_of_products_on_page
from pages.auth_page import authorization
from credentials import all_users, standard_user
from pages.main_page import add_item_to_cart_random
from pages.cart_page import check_elements_cart, get_all_items_info, get_specific_items_info, delete_all_items_from_cart


@pytest.mark.cart
@pytest.mark.parametrize(*all_users)
def test_empty_cart_page_check_elements(page: Page, login, password):
    """Проверка элементов страницы корзины (пустой)"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    check_elements_cart(page, "empty")


@pytest.mark.cart
@pytest.mark.parametrize(*all_users)
def test_not_empty_cart_page_check_elements(page: Page, login, password):
    """Проверка элементов страницы корзины (не пустой)"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    products_numbers = add_item_to_cart_random(page, number_of_products_on_page)
    number_of_products_on_cart = len(products_numbers)
    items_info_on_main_page = get_specific_items_info(page, products_numbers)
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    check_elements_cart(page, "not_empty")
    expect(page.locator("div.cart_item"), f"Некорректное количество товаров корзине. "
                                          f"ОР: {number_of_products_on_cart}").to_have_count(number_of_products_on_cart)
    items_info_on_cart_page = get_all_items_info(page, number_of_products_on_cart)
    for i in range(len(items_info_on_cart_page)):
        assert items_info_on_cart_page[i] == items_info_on_main_page[i], \
            f"Некорректные данные в корзине. ОР: {items_info_on_main_page[i]}, ФР: {items_info_on_cart_page[i]}"

@pytest.mark.new
@pytest.mark.cart
@pytest.mark.parametrize(*all_users)
def test_remove_from_cart(page: Page, login, password):
    """Проверка удаления товаров из корзины"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    products_numbers = add_item_to_cart_random(page, number_of_products_on_page)
    number_of_products_on_cart = len(products_numbers)
    page.locator("a.shopping_cart_link").click()
    assert page.url == url_cart_page, f"Некорректный адрес. ОР: {url_cart_page}, ФР: {page.url}"
    check_elements_cart(page, "not_empty")
    expect(page.locator("div.cart_item"), f"Некорректное количество товаров корзине. "
                                          f"ОР: {number_of_products_on_cart}").to_have_count(number_of_products_on_cart)
    delete_all_items_from_cart(page, number_of_products_on_cart)
    check_elements_cart(page, "empty")
    page.locator("button#continue-shopping").click()
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    expect(page.locator("span.shopping_cart_badge"), "Отображается счетчик на корзине").not_to_be_visible()
    for i in range(number_of_products_on_page):
        expect(page.locator("button.btn_inventory").nth(i), "Товар не удален из корзины").to_have_text("Add to cart")
