import pytest
from playwright.sync_api import Page, expect
from vars import url_auth_page, url_main_page, number_of_items_on_page
from data import expected_items
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from credentials import all_users, standard_user


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_main_page_check_elements(page, username, password):
    """Проверка элементов главной страницы"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    main_page.check_elements_on_main_page()
    main_page.check_left_menu_items()
    main_page.check_filter_items()


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_log_out(page, username, password):
    """Проверка деавторизации пользователя"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    main_page.logout()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_counter_on_cart(page: Page, username, password):
    """Проверка работы счетчика на корзине"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    for i in range(number_of_items_on_page):
        expected_item_counter_on_cart = i+1
        current_item_counter_on_cart = main_page.add_item_to_cart(i)
        assert expected_item_counter_on_cart == current_item_counter_on_cart, \
            (f"Некорректное отображение счетчика на корзине. ОР: {expected_item_counter_on_cart}, "
             f"ФР: {current_item_counter_on_cart}")
    for i in reversed(range(number_of_items_on_page)):
        expected_item_counter_on_cart = i
        current_item_counter_on_cart = main_page.delete_item_from_cart(i)
        assert expected_item_counter_on_cart == current_item_counter_on_cart, \
            (f"Некорректное отображение счетчика на корзине. "
             f"ОР: {expected_item_counter_on_cart}, ФР: {current_item_counter_on_cart}")


@pytest.mark.xfail(reason="Не реализован сброс состояний кнопок при нажатии Reset App State")
@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_reset_app_state(page, username, password):
    """Проверка сброса состояния приложения"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    main_page.add_item_to_cart_random()
    main_page.reset_app_state()
    expect(page.locator("span.shopping_cart_badge"), "Счетчик не должен отображаться").not_to_be_visible()
    main_page.check_all_item_buttons_state("Add to cart")


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_save_cart_state_after_logout(page, username, password):
    """Проверка, что товары остаются в корзине после выхода и авторизации"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    items_numbers = main_page.add_item_to_cart_random()
    main_page.logout()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page.check_specific_item_buttons_state(items_numbers, "Remove")


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_all_items(page, username, password):
    """Проверка всех карточек товаров"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    current_items = main_page.get_all_items_info()
    for i in range(number_of_items_on_page):
        assert current_items[i] == expected_items[i], \
            f"Некорректные элементы карточки. ОР: {expected_items[i]}, ФР: {current_items[i]}"


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_all_items_sort_name(page, username, password):
    """Проверка сортировки карточек товаров по имени"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    main_page.select_filter("Name (A to Z)")
    current_items = main_page.get_all_items_info()
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_name'])
    for i in range(number_of_items_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"
    main_page.select_filter("Name (Z to A)")
    current_items = main_page.get_all_items_info()
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_name'], reverse=True)
    for i in range(number_of_items_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"


@pytest.mark.main
@pytest.mark.parametrize(*all_users)
def test_all_items_sort_price(page, username, password):
    """Проверка сортировки карточек товаров по стоимости"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    main_page = MainPage(page)
    main_page.select_filter("Price (low to high)")
    current_items = main_page.get_all_items_info()
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_price'])
    for i in range(number_of_items_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"
    main_page.select_filter("Price (high to low)")
    current_items = main_page.get_all_items_info()
    expected_items_sort = sorted(expected_items, key=lambda x: x['item_price'], reverse=True)
    for i in range(number_of_items_on_page):
        assert current_items[i] == expected_items_sort[i], \
            f"Некорректные элементы карточки. ОР: {expected_items_sort[i]}, ФР: {current_items[i]}"
