import pytest
from vars import header_text, checkout_title
from playwright.sync_api import Page, expect
from vars import url_checkout_step_1_page


class CheckoutStepOnePage:
    def __init__(self, page: Page):
        self.page = page
        self.app_logo = page.locator("div.app_logo")
        self.title = page.locator("span.title")
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.cancel_button = page.locator("#cancel")
        self.continue_button = page.locator("#continue")
        self.error_message = page.locator("div.error>h3")
        self.error_icon = page.locator("svg.error_icon")
        self.error_button = page.locator("button.error-button")

    def check_elements(self):
        """Проверка элементов страницы"""
        expect(self.app_logo, "Не отображается текст логотипа").to_be_visible()
        expect(self.title, "Не отображается заголовок").to_be_visible()
        expect(self.first_name_input, "Не отображается поле ввода имени").to_be_visible()
        expect(self.last_name_input, "Не отображается поле ввода фамилии").to_be_visible()
        expect(self.postal_code_input, "Не отображается поле ввода почтового индекса").to_be_visible()
        expect(self.cancel_button, "Не отображается кнопка Cancel").to_be_visible()
        expect(self.continue_button, "Не отображается кнопка Continue").to_be_visible()
        expect(self.app_logo, f"Некорректный текст логотипа. ОР: {header_text}, "
                              f"ФР: {self.app_logo.inner_text()}").to_have_text(header_text)
        expect(self.title, f"Некорректный текст заголовка. ОР: {checkout_title}, "
                           f"ФР: {self.title.inner_text()}").to_have_text(checkout_title)
        (expect(self.first_name_input, f"Некорректный текст плейсхолдера поля имени. ОР: 'First Name', "
                                      f"ФР: {self.first_name_input.get_attribute('placeholder')}")
         .to_have_attribute('placeholder', 'First Name'))
        (expect(self.last_name_input, f"Некорректный текст плейсхолдера поля фамилии. ОР: 'Last Name', "
                                     f"ФР: {self.last_name_input.get_attribute('placeholder')}")
         .to_have_attribute('placeholder', 'Last Name'))
        (expect(self.postal_code_input, f"Некорректный текст плейсхолдера поля почтового индекса. ОР: 'Last Name', "
                                       f"ФР: {self.postal_code_input.get_attribute('placeholder')}")
         .to_have_attribute('placeholder', 'Zip/Postal Code'))
        expect(self.cancel_button, "Некорректный текст на кнопке Cancel").to_have_text("Cancel")
        expect(self.continue_button, "Некорректный текст на кнопке Continue").to_have_text("Continue")

    def check_opened_failed_checkout_elements(self, first_name, last_name, postal_code, expected_error_message):
        """Проверка элементов страницы при незаполненных полях ввода"""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()
        assert self.page.url == url_checkout_step_1_page, (f"Некорректный адрес. ОР: {url_checkout_step_1_page}, "
                                                           f"ФР: {self.page.url}")
        expect(self.first_name_input,
               "Поле ввода имени не выделено красным").to_have_class("input_error form_input error")
        expect(self.last_name_input,
               "Поле ввода фамилии не выделено красным").to_have_class("input_error form_input error")
        expect(self.postal_code_input,
               "Поле ввода почтового индекса не выделено красным").to_have_class("input_error form_input error")
        expect(self.error_message, "Не отображается сообщение об ошибке").to_be_visible()
        expect(self.error_icon, "Не отображаются иконки напротив полей ввода").to_have_count(3)
        expect(self.error_button,
               "Не отображается кнопка закрытия сообщения об ошибке").to_be_visible()
        current_error_message = self.error_message.inner_text()
        assert current_error_message == expected_error_message, \
            f"Некорректный текст ошибки. ОР: {expected_error_message}, ФР: {current_error_message}"

    def close_failed_checkout_elements(self):
        """Закрыть сообщение о незаполненных полях ввода и проверить элементы страницы"""
        self.error_button.click()
        expect(self.error_icon, "Иконки напротив полей ввода не должны отображаться").not_to_be_visible()
        expect(self.error_message, "Сообщение об ошибке не должно отображаться").not_to_be_visible()
        expect(self.first_name_input,
               "Поле ввода имени не выделено красным").not_to_have_class("input_error form_input error")
        expect(self.last_name_input,
               "Поле ввода фамилии не выделено красным").not_to_have_class("input_error form_input error")
        expect(self.postal_code_input,
               "Поле ввода почтового индекса не выделено красным").not_to_have_class("input_error form_input error")

    #
    def set_inputs_and_continue(self):
        """Заполнить поля и нажать continue"""
        self.first_name_input.fill("1")
        self.last_name_input.fill("1")
        self.postal_code_input.fill("1")
        self.continue_button.click()
        expect(self.error_message, "Сообщение об ошибке не должно отображаться").not_to_be_visible()
