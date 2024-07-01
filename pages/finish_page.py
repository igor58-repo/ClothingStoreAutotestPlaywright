import pytest
from vars import header_text, checkout_title, complete_header, complete_text
from playwright.sync_api import Page, expect


# проверка элементов страницы
def check_elements_empty(page: Page):
    app_logo = page.locator("div.app_logo")
    title = page.locator("span.title")
    img = page.locator("img.pony_express")
    complete_header = page.locator("h2.complete-header")
    complete_text = page.locator("complete-text")
    back_home_button = page.locator("button#back-to-products")
    expect(app_logo, "Не отображается текст логотипа").to_be_visible()
    expect(title, "Не отображается заголовок").to_be_visible()
    expect(img, "Не отображается изображение").to_be_visible()
    expect(complete_header, "Не отображается сообщение в заголовке").to_be_visible()
    expect(complete_text, "Не отображается текст об успешном заказе").to_be_visible()
    expect(back_home_button, "Не отображается кнопка Back Home").to_be_visible()
    expect(app_logo, f"Некорректный текст логотипа. ОР: {header_text}, "
                     f"ФР: {app_logo.inner_text()}").to_have_text(header_text)
    expect(title, f"Некорректный текст заголовка. ОР: {checkout_title}, "
                  f"ФР: {title.inner_text()}").to_have_text(checkout_title)
    expect(complete_header, f"Некорректный текст заголовка. ОР: {checkout_title}, "
                  f"ФР: {title.inner_text()}").to_have_text(checkout_title)
