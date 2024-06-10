import pytest
from vars import url_auth_page, url_main_page
from pages.auth_page import authorization
from pages.main_page import check_elements_on_page, check_left_menu_items, check_filter_items
from credentials import all_users, standard_user
from playwright.sync_api import Page


@pytest.mark.auth
@pytest.mark.parametrize(*all_users)
def test_main_page_check_elements(page: Page, login, password):
    """Проверка элементов главной страница"""
    page.goto(url_auth_page)
    authorization(page, login, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"
    check_elements_on_page(page)
    check_left_menu_items(page)
    check_filter_items(page)

