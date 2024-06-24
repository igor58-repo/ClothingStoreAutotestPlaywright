import pytest
from playwright.sync_api import Page, expect
from vars import (url_auth_page, url_main_page, number_of_products_on_page, header_text, number_of_menu_items,
                  left_menu_items, filter_menu_items)
from data import expected_items
from pages.auth_page import authorization
from pages.main_page import (check_elements_on_page, check_left_menu_items, check_filter_items, add_item_to_cart,
                             delete_item_from_cart, add_item_to_cart_random, check_all_item_buttons_state,
                             check_specific_item_buttons_state, get_all_items_info)
from credentials import all_users, standard_user


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_main_page_check_elements(page: Page, login, password):
    """Проверка элементов главной страницы"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    check_elements_on_page(page, number_of_products_on_page, header_text)
    check_left_menu_items(page, number_of_menu_items, left_menu_items)
    check_filter_items(page, filter_menu_items)


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_log_out(page: Page, login, password):
    """Проверка деавторизации пользователя"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("#react-burger-menu-btn").click()
    page.get_by_text("Logout").click()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"


@pytest.mark.main
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


@pytest.mark.xfail(reason="Не реализован сброс состояний кнопок при нажатии Reset App State")
@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_reset_app_state(page: Page, login, password):
    """Проверка сброса состояния приложения"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    add_item_to_cart_random(page, number_of_products_on_page)
    page.locator("#react-burger-menu-btn").click()
    page.get_by_text("Reset App State").click()
    expect(page.locator("span.shopping_cart_badge")).not_to_be_visible()
    check_all_item_buttons_state(page, number_of_products_on_page, "Add to cart")


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_save_cart_state_after_logout(page: Page, login, password):
    """Проверка, что товары остаются в корзине после выхода и авторизации"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    products_numbers = add_item_to_cart_random(page, number_of_products_on_page)
    page.locator("#react-burger-menu-btn").click()
    page.get_by_text("Logout").click()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    check_specific_item_buttons_state(page, products_numbers, "Remove")


@pytest.mark.main
@pytest.mark.parametrize(*standard_user)
def test_all_items(page: Page, login, password):
    """Проверка всех карточек товаров"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    current_items = get_all_items_info(page, number_of_products_on_page)
    for i in range(number_of_products_on_page):
        assert current_items[i] == expected_items[i], \
            f"Некорректные элементы карточки. ОР: {expected_items[i]}, ФР: {current_items[i]}"


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_all_items_sort_name(page: Page, login, password):
    """Проверка сортировки карточек товаров по имени"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("select.product_sort_container").select_option("Name (A to Z)")
    current_items = get_all_items_info(page, number_of_products_on_page)
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_name'])
    for i in range(number_of_products_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"
    page.locator("select.product_sort_container").select_option("Name (Z to A)")
    current_items = get_all_items_info(page, number_of_products_on_page)
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_name'], reverse=True)
    for i in range(number_of_products_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_all_items_sort_price(page: Page, login, password):
    """Проверка сортировки карточек товаров по стоимости"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    page.locator("select.product_sort_container").select_option("Price (low to high)")
    current_items = get_all_items_info(page, number_of_products_on_page)
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_price'])
    for i in range(number_of_products_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"
    page.locator("select.product_sort_container").select_option("Price (high to low)")
    current_items = get_all_items_info(page, number_of_products_on_page)
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_price'], reverse=True)
    for i in range(number_of_products_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"
