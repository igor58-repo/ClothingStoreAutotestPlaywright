import pytest
from vars import url_auth_page, url_main_page
from pages.auth_page import auth_page_check_elements
from credentials import all_users
from playwright.sync_api import Page, expect


@pytest.mark.auth
def test_auth_page_check_elements(page: Page):
    """Проверка элементов страницы авторизации"""
    page.goto(url_auth_page)
    auth_page_check_elements(page)


