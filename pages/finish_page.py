import pytest
from vars import header_text, final_title, complete_header_text, complete_message
from playwright.sync_api import Page, expect


class FinishPage:
    def __init__(self, page: Page):
        self.page = page
        self.app_logo = page.locator("div.app_logo")
        self.title = page.locator("span.title")
        self.img = page.locator("img.pony_express")
        self.complete_header = page.locator("h2.complete-header")
        self.complete = page.locator("div.complete-text")
        self.back_home_button = page.locator("button#back-to-products")

    def check_elements(self):
        """Проверка элементов страницы"""
        expect(self.app_logo, "Не отображается текст логотипа").to_be_visible()
        expect(self.title, "Не отображается заголовок").to_be_visible()
        expect(self.img, "Не отображается изображение").to_be_visible()
        expect(self.complete_header, "Не отображается сообщение в заголовке").to_be_visible()
        expect(self.complete, "Не отображается текст об успешном заказе").to_be_visible()
        expect(self.back_home_button, "Не отображается кнопка Back Home").to_be_visible()
        expect(self.app_logo, f"Некорректный текст логотипа. ОР: {header_text}, "
                              f"ФР: {self.app_logo.inner_text()}").to_have_text(header_text)
        expect(self.title, f"Некорректный текст заголовка. ОР: {final_title}, "
                           f"ФР: {self.title.inner_text()}").to_have_text(final_title)
        expect(self.complete_header, f"Некорректный текст хедера. ОР: {complete_header_text}, "
                                     f"ФР: {self.complete_header.inner_text()}").to_have_text(complete_header_text)
        expect(self.complete, f"Некорректный текст сообщения. ОР: {complete_message}, "
                              f"ФР: {self.complete.inner_text()}").to_have_text(complete_message)
