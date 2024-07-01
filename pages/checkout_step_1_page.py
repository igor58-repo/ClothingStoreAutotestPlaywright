import pytest
from vars import header_text, checkout_title
from playwright.sync_api import Page, expect
from vars import url_checkout_step_1_page


# проверка элементов страницы
def check_elements(page: Page):
    app_logo = page.locator("div.app_logo")
    title = page.locator("span.title")
    first_name_input = page.locator("#first-name")
    last_name_input = page.locator("#last-name")
    postal_code_input = page.locator("#postal-code")
    cancel_button = page.locator("#cancel")
    continue_button = page.locator("#continue")
    expect(app_logo, "Не отображается текст логотипа").to_be_visible()
    expect(title, "Не отображается заголовок").to_be_visible()
    expect(first_name_input, "Не отображается поле ввода имени").to_be_visible()
    expect(last_name_input, "Не отображается поле ввода фамилии").to_be_visible()
    expect(postal_code_input, "Не отображается поле ввода почтового индекса").to_be_visible()
    expect(cancel_button, "Не отображается кнопка Cancel").to_be_visible()
    expect(continue_button, "Не отображается кнопка Continue").to_be_visible()
    expect(app_logo, f"Некорректный текст логотипа. ОР: {header_text}, "
                       f"ФР: {app_logo.inner_text()}").to_have_text(header_text)
    expect(title, f"Некорректный текст заголовка. ОР: {checkout_title}, "
                  f"ФР: {title.inner_text()}").to_have_text(checkout_title)
    expect(first_name_input, f"Некорректный текст плейсхолдера поля имени. ОР: 'First Name', ФР: "
                             f"{first_name_input.get_attribute('placeholder')}").to_have_attribute('placeholder',
                                                                                                   'First Name')
    expect(last_name_input, f"Некорректный текст плейсхолдера поля фамилии. ОР: 'Last Name', "
                            f"ФР: {last_name_input.get_attribute('placeholder')}").to_have_attribute('placeholder',
                                                                                                     'Last Name')
    expect(postal_code_input, f"Некорректный текст плейсхолдера поля почтового индекса. ОР: 'Last Name', ФР: "
                              f"{postal_code_input.get_attribute('placeholder')}").to_have_attribute('placeholder',
                                                                                                     'Zip/Postal Code')
    expect(cancel_button, "Некорректный текст на кнопке Cancel").to_have_text("Cancel")
    expect(continue_button, "Некорректный текст на кнопке Continue").to_have_text("Continue")


# проверка элементов страницы при незаполненных полях ввода
def check_opened_failed_checkout_elements(page: Page, first_name, last_name, postal_code, expected_error_message):
    page.locator("#first-name").fill(first_name)
    page.locator("#last-name").fill(last_name)
    page.locator("#postal-code").fill(postal_code)
    page.locator("#continue").click()
    assert page.url == url_checkout_step_1_page, f"Некорректный адрес. ОР: {url_checkout_step_1_page}, ФР: {page.url}"
    error_message = page.locator("div.error>h3")
    expect(page.locator("#first-name"),
           "Поле ввода имени не выделено красным").to_have_class("input_error form_input error")
    expect(page.locator("#last-name"),
           "Поле ввода фамилии не выделено красным").to_have_class("input_error form_input error")
    expect(page.locator("#postal-code"),
           "Поле ввода почтового индекса не выделено красным").to_have_class("input_error form_input error")
    expect(error_message, "Не отображается сообщение об ошибке").to_be_visible()
    expect(page.locator("svg.error_icon"), "Не отображаются иконки напротив полей ввода").to_have_count(3)
    expect(page.locator("button.error-button"), "Не отображается кнопка закрытия сообщения об ошибке").to_be_visible()
    current_error_message = error_message.inner_text()
    assert current_error_message == expected_error_message, \
        f"Некорректный текст ошибки. ОР: {expected_error_message}, ФР: {current_error_message}"


# закрыть сообщение о незаполненных полях ввода и проверить элементы страницы
def close_failed_checkout_elements(page: Page):
    page.locator("button.error-button").click()
    expect(page.locator("svg.error_icon"), "Иконки напротив полей ввода не должны отображаться").not_to_be_visible()
    expect(page.locator("div.error"), "Сообщение об ошибке не должно отображаться").not_to_be_visible()
    expect(page.locator("#first-name"),
           "Поле ввода имени не выделено красным").not_to_have_class("input_error form_input error")
    expect(page.locator("#last-name"),
           "Поле ввода фамилии не выделено красным").not_to_have_class("input_error form_input error")
    expect(page.locator("#postal-code"),
           "Поле ввода почтового индекса не выделено красным").not_to_have_class("input_error form_input error")


# заполнить поля и нажать continue
def set_inputs_and_continue(page):
    page.locator("#first-name").fill("1")
    page.locator("#last-name").fill("1")
    page.locator("#postal-code").fill("1")
    page.locator("#continue").click()
    expect(page.locator("div.error"), "Сообщение об ошибке не должно отображаться").not_to_be_visible()
