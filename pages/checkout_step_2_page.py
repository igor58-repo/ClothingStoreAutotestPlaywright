import pytest
from playwright.sync_api import Page, expect


class CheckoutStepTwoPage:
    def __init__(self, page: Page):
        self.page = page
        self.payment_info_text = page.get_by_text("Payment Information:")
        self.shipping_info_text = page.get_by_text("Shipping Information:")
        self.delivery_text = page.get_by_text("Free Pony Express Delivery!")
        self.price_total_text = page.get_by_text("Price Total")
        self.item_total_0_text = page.get_by_text("Item total: $0")
        self.tax_0_text = page.get_by_text("Tax: $0.00")
        self.total_0_text = page.get_by_text("Total: $0.00")
        self.cancel_button = page.locator("#cancel")
        self.finish_button = page.locator("#finish")
        self.item_name = page.locator("div.inventory_item_name")
        self.item_desc = page.locator("div.inventory_item_desc")
        self.item_price = page.locator("div.inventory_item_price")

    def checkout_step_2_check_elements_empty(self):
        """Проверка элементов страницы"""
        expect(self.payment_info_text, "Не отображается Payment Information:").to_be_visible()
        expect(self.shipping_info_text, "Не отображается Shipping Information:").to_be_visible()
        expect(self.delivery_text, "Не отображается Free Pony Express Delivery!").to_be_visible()
        expect(self.price_total_text, "Не отображается Price Total").to_be_visible()
        expect(self.item_total_0_text, "Не отображается Item total: $0").to_be_visible()
        expect(self.tax_0_text, "Не отображается Tax: $0.00").to_be_visible()
        expect(self.total_0_text, "Не отображается Total: $0.00").to_be_visible()
        expect(self.cancel_button, "Не отображается кнопка Cancel").to_be_visible()
        expect(self.finish_button, "Не отображается кнопка Finish").to_be_visible()

    def get_all_items_info_checkout_2(self, number_of_items_on_cart):
        """Получить информацию о всех товарах в корзине"""
        items = []
        for i in range(number_of_items_on_cart):
            new_dict = {
                'item_name': self.item_name.nth(i).inner_text(),
                'item_desc': self.item_desc.nth(i).inner_text(),
                'item_price': float((self.item_price.nth(i).inner_text())[1:])}
            items.append(new_dict)
        return items

    def get_prices_of_items_in_cart(self, items_info_on_cart_page):
        """Получить цены товаров в корзине"""
        prices = []
        for i in items_info_on_cart_page:
            prices.append(i["item_price"])
        return prices

    def get_current_total_prices(self):
        """Получить сумму товаров, налог, итоговую сумму со страницы"""
        total_prices = {
            'current_item_total': float(self.page.locator("div.summary_subtotal_label").inner_text().split('$')[1]),
            'current_tax': float(self.page.locator("div.summary_tax_label").inner_text().split('$')[1]),
            'current_total': float(self.page.locator("div.summary_total_label").inner_text().split('$')[1])
        }
        return total_prices

    def get_expected_total_prices(self, item_prices):
        """Рассчитать ожидаемые сумму товаров, налог, итоговую сумму"""
        item_total = round(sum(item_prices), 2)
        tax = round(item_total * 0.08, 2)
        total = round(item_total + tax, 2)
        total_prices = {
            'expected_item_total': item_total,
            'expected_tax': tax,
            'expected_total': total
        }
        return total_prices

