import pytest
from vars import login_logo_text
from playwright.sync_api import Page, expect


# проверка элементов страницы авторизации
def auth_page_check_elements(page: Page):
    login_logo = page.locator(".login_logo")
    login_input = page.locator("#user-name")
    password_input = page.locator("#password")
    login_button = page.locator("#login-button")
    expect(login_logo, "Не отображается текст логотипа").to_be_visible()
    expect(login_input, "Не отображается поле ввода логина").to_be_visible()
    expect(password_input, "Не отображается поле ввода пароля").to_be_visible()
    expect(login_button, "Не отображается кнопка Login").to_be_visible()
    expect(login_logo, f"Некорретный текст логотипа. ОР: {login_logo_text}, "
                       f"ФР: {login_button.inner_text()}").to_have_text(login_logo_text)
    expect(login_input, f"Некорретный текст плейсхолдера поля ввода логина. ОР: 'Username', "
                        f"ФР: {login_input.get_attribute('placeholder')}").to_have_attribute('placeholder', 'Username')
    expect(password_input, f"Некорретный текст плейсхолдера поля ввода пароля. ОР: 'Password', "
                        f"ФР: {password_input.get_attribute('placeholder')}").to_have_attribute('placeholder', 'Password')
    expect(login_button, f"Некорретный текст на кнопке Login. ОР: 'Login', "
                        f"ФР: {login_button.get_attribute('value')}").to_have_text('Login')


# авторизация
def authorization(page: Page, login, password):
    page.locator("#user-name").fill(login)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()
