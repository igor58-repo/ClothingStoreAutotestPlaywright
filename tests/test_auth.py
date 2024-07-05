import pytest
from vars import url_auth_page, url_main_page
from pages.auth_page import AuthPage
from credentials import all_users, standard_user

error_message_non_existent_user = "Epic sadface: Username and password do not match any user in this service"
error_message_locked_out_user = "Epic sadface: Sorry, this user has been locked out."
error_message_empty_login = "Epic sadface: Username is required"
error_message_empty_password = "Epic sadface: Password is required"
input_values = (f"username, password, error_message",
                [("standard_user", "user", f"{error_message_non_existent_user}"),
                 ("locked_out_user", "secret_sauce", f"{error_message_locked_out_user}"),
                 ("", "secret_sauce", f"{error_message_empty_login}"),
                 ("standard_user", "", f"{error_message_empty_password}")
                 ])


@pytest.mark.auth
@pytest.mark.parametrize(*all_users)
def test_authorization_positive(page, username, password):
    """Проверка успешной авторизации"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.auth_page_check_elements()
    auth_page.authorization(username, password)
    assert page.url == url_main_page, f"Некорректный адрес. ОР: {url_main_page}, ФР: {page.url}"


@pytest.mark.auth
@pytest.mark.parametrize(*input_values)
def test_authorization_negative(page, username, password, error_message):
    """Проверка негативных сценариев авторизации и отображаемых ошибок"""
    auth_page = AuthPage(page)
    auth_page.navigate()
    assert page.url == url_auth_page, f"Некорректный адрес. ОР: {url_auth_page}, ФР: {page.url}"
    auth_page.authorization(username, password)
    auth_page.check_opened_failed_auth_elements(error_message)
    auth_page.close_failed_auth_elements()
