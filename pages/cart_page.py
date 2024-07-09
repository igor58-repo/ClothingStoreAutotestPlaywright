import pytest
from playwright.sync_api import Page, expect
from vars import continue_shopping_text, checkout_text, cart_quantity_text, cart_desc_text, number_of_items_on_page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_quantity = page.locator("div.cart_quantity")
        self.cart_quantity_label = page.locator("div.cart_quantity_label")
        self.cart_desc = page.locator("div.cart_desc_label")
        self.continue_shopping_button = page.locator("button#continue-shopping")
        self.checkout_button = page.locator("button#checkout")
        self.cart_item = page.locator("div.cart_item")
        self.item_name = page.locator("div.inventory_item_name")
        self.item_desc = page.locator("div.inventory_item_desc")
        self.item_price = page.locator("div.inventory_item_price")
        self.remove_button = page.get_by_role("button", name='Remove')
        self.shopping_cart_badge = page.locator("span.shopping_cart_badge")

    def check_elements_cart(self, cart_state):
        """Проверка элементов страницы корзины"""
        expect(self.cart_quantity_label, "Не отображается элемент Количество товаров в корзине").to_be_visible()
        expect(self.cart_quantity_label, f"Некорректный текст. "
                                         f"ОР: {cart_quantity_text}").to_have_text(cart_quantity_text)
        expect(self.cart_desc, "Не отображается элемент Описание товаров в корзине").to_be_visible()
        expect(self.cart_desc, f"Некорректный текст. ОР: {cart_desc_text}").to_have_text(cart_desc_text)
        expect(self.continue_shopping_button, f"Не отображается кнопка {continue_shopping_text}").to_be_visible()
        expect(self.continue_shopping_button, f"Некорректный текст на кнопке. "
                                              f"ОР: {continue_shopping_text}").to_have_text(continue_shopping_text)
        expect(self.checkout_button, f"Не отображается кнопка {checkout_text}").to_be_visible()
        expect(self.checkout_button, f"Некорректный текст на кнопке. ОР: {checkout_text}").to_have_text(checkout_text)
        if cart_state == "empty":
            expect(self.cart_item, "Корзина должна быть пустой").not_to_be_visible()
        elif cart_state == "not_empty":
            expect(self.cart_quantity.first,
                   "Не отображается количество товаров в корзине").to_be_visible()
            expect(self.item_name.first, "Не отображается заголовок товара").to_be_visible()
            expect(self.item_desc.first, "Не отображается описание товара").to_be_visible()
            expect(self.item_price.first, "Не отображается стоимость товара").to_be_visible()
            expect(self.remove_button.first,
                   "Не отображается кнопка удаления товара").to_be_visible()
        else:
            assert False, "Параметр cart_state должен иметь значения empty или not_empty"

    def get_all_items_in_cart_info(self, number_of_items_on_cart):
        """Получить информацию о всех товарах в корзине"""
        items = []
        for i in range(number_of_items_on_cart):
            new_dict = {
                'item_name': self.item_name.nth(i).inner_text(),
                'item_desc': self.item_desc.nth(i).inner_text(),
                'item_price': float((self.item_price.nth(i).inner_text())[1:])}
            items.append(new_dict)
        return items

    def delete_all_items_from_cart(self, number_of_items_on_cart):
        """Удаление товара из корзины"""
        for i in reversed(range(number_of_items_on_cart)):
            remove_from_cart_button = self.remove_button.first
            expect(remove_from_cart_button, "Некорректная надпись на кнопке. ОР: 'Remove'").to_have_text("Remove")
            remove_from_cart_button.click()
            if i == 0:
                expect(self.shopping_cart_badge, "Отображается счетчик на корзине").not_to_be_visible()
            else:
                expect(self.shopping_cart_badge, "Не отображается счетчик на корзине").to_be_visible()
                current_item_counter_on_cart = self.shopping_cart_badge.inner_text()
                assert i == int(current_item_counter_on_cart), \
                    (f"Некорректное отображение счетчика на корзине. ОР: {i}, "
                     f"ФР: {current_item_counter_on_cart}")
        expect(self.cart_item, "Товары не удалены из корзины").not_to_be_visible()
