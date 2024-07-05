from vars import header_text, url_auth_page
from playwright.sync_api import Page, expect


class AuthPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_logo = page.locator(".login_logo")
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("div.error>h3")
        self.error_icon = page.locator("svg.error_icon")
        self.error_button = page.locator("button.error-button")

    def navigate(self):
        """Открыть страницу авторизации и проверить url"""
        self.page.goto(url_auth_page)

    def authorization(self, login, password):
        """Заполнить входные данные и нажать кнопку авторизации"""
        self.username_input.fill(login)
        self.password_input.fill(password)
        self.login_button.click()

    def auth_page_check_elements(self):
        """Проверка отображения элементов страницы авторизации"""
        expect(self.login_logo, "Не отображается текст логотипа").to_be_visible()
        expect(self.username_input, "Не отображается поле ввода логина").to_be_visible()
        expect(self.password_input, "Не отображается поле ввода пароля").to_be_visible()
        expect(self.login_button, "Не отображается кнопка Login").to_be_visible()
        expect(self.login_logo, f"Некорректный текст логотипа. ОР: {header_text}, "
                                f"ФР: {self.login_button.inner_text()}").to_have_text(header_text)
        expect(self.username_input, f"Некорректный текст плейсхолдера поля ввода логина. ОР: 'Username', "
                                    f"ФР: {self.username_input.get_attribute('placeholder')}").to_have_attribute(
            'placeholder', 'Username')
        expect(self.password_input, f"Некорректный текст плейсхолдера поля ввода пароля. ОР: 'Password', "
                                    f"ФР: {self.password_input.get_attribute('placeholder')}").to_have_attribute(
            'placeholder', 'Password')
        expect(self.login_button, f"Некорректный текст на кнопке Login. ОР: 'Login', "
                                  f"ФР: {self.login_button.get_attribute('value')}").to_have_text('Login')

    def check_opened_failed_auth_elements(self, expected_error_message):
        """Проверка отображения элементов страницы после неудачной авторизации"""
        expect(self.username_input, "Поле ввода логина не выделено красным").to_have_class(
            "input_error form_input error")
        expect(self.password_input, "Поле ввода пароля не выделено красным").to_have_class(
            "input_error form_input error")
        expect(self.error_message, "Не отображается сообщение об ошибке").to_be_visible()
        expect(self.error_icon, "Не отображаются иконки напротив полей ввода").to_have_count(2)
        expect(self.error_button,
               "Не отображается кнопка закрытия сообщения об ошибке").to_be_visible()
        current_error_message = self.error_message.inner_text()
        assert current_error_message == expected_error_message, \
            f"Некорректный текст ошибки. ОР: {expected_error_message}, ФР: {current_error_message}"

    def close_failed_auth_elements(self):
        """Закрыть сообщение о неудачной авторизации и проверить элементы страницы"""
        self.error_button.click()
        expect(self.error_icon, "Иконки напротив полей ввода не должны отображаться").not_to_be_visible()
        expect(self.error_message, "Сообщение об ошибке не должно отображаться").not_to_be_visible()
        expect(self.username_input, "Поле ввода логина не должно быть выделено красным").not_to_have_class(
            "input_error form_input error")
        expect(self.password_input, "Поле ввода пароля не должно быть выделено красным").not_to_have_class(
            "input_error form_input error")
