import pytest
from vars import header_text
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
    expect(login_logo, f"Некорретный текст логотипа. ОР: {header_text}, "
                       f"ФР: {login_button.inner_text()}").to_have_text(header_text)
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



# проверка элементов страницы после неудачной авторизации
def check_opened_failed_auth_elements(page: Page, expected_error_message):
    error_message = page.locator("div.error>h3")
    expect(page.locator("#user-name"),
           "Поле ввода логина не выделено красным").to_have_class("input_error form_input error")
    expect(page.locator("#password"),
           "Поле ввода пароля не выделено красным").to_have_class("input_error form_input error")
    expect(error_message, "Не отображается сообщение об ошибке").to_be_visible()
    expect(page.locator("svg.error_icon"), "Не отображаются иконки напротив полей ввода").to_have_count(2)
    expect(page.locator("button.error-button"), "Не отображается кнопка закрытия сообщения об ошибке").to_be_visible()
    current_error_message = error_message.inner_text()
    assert current_error_message == expected_error_message, \
        f"Некорректный текст ошибки. ОР: {expected_error_message}, ФР: {current_error_message}"


# закрыть сообщение о неудачной авторизации и проверить элементы страницы
def close_failed_auth_elements(page: Page):
    page.locator("button.error-button").click()
    expect(page.locator("svg.error_icon"), "Иконки напротив полей ввода не должны отображаться").not_to_be_visible()
    expect(page.locator("div.error"), "Сообщение об ошибке не должно отображаться").not_to_be_visible()
    expect(page.locator("#user-name"),
           "Поле ввода логина не должно быть выделено красным").not_to_have_class("input_error form_input error")
    expect(page.locator("#password"),
           "Поле ввода пароля не должно быть выделено красным").not_to_have_class("input_error form_input error")
