import pytest
from playwright.sync_api import Page, expect


# проверка элементов страницы
def check_elements_empty(page: Page):
    expect(page.get_by_text("Payment Information:"), "Не отображается Payment Information:").to_be_visible()
    expect(page.get_by_text("Shipping Information:"), "Не отображается Shipping Information:").to_be_visible()
    expect(page.get_by_text("Free Pony Express Delivery!"), "Не отображается Free Pony Express Delivery!").to_be_visible()
    expect(page.get_by_text("Price Total"), "Не отображается Price Total").to_be_visible()
    expect(page.get_by_text("Item total: $0"), "Не отображается Item total: $0").to_be_visible()
    expect(page.get_by_text("Tax: $0.00"), "Не отображается Tax: $0.00").to_be_visible()
    expect(page.get_by_text("Total: $0.00"), "Не отображается Total: $0.00").to_be_visible()
    expect(page.locator("#cancel"), "Не отображается кнопка Cancel").to_be_visible()
    expect(page.locator("#finish"), "Не отображается кнопка Finish").to_be_visible()


# получить информацию о всех товарах в корзине
def get_all_items_info_checkout_2(page: Page, number_of_products_on_page):
    items = []
    for i in range(number_of_products_on_page):
        new_dict = {
            'item_name':
                (page.locator("div.inventory_item_name").nth(i).inner_text()),
            'item_desc':
                (page.locator("div.inventory_item_desc").nth(i).inner_text()),
            'item_price':
                float((page.locator("div.inventory_item_price").nth(i).inner_text())[1:])}
        items.append(new_dict)
    return items


# получить цены товаров в корзине
def get_prices_of_items_in_cart(items_info_on_cart_page):
    prices = []
    for i in items_info_on_cart_page:
        prices.append(i["item_price"])
    return prices


# суммарная стоимость товаров в корзине
def get_item_total(item_prices):
    item_total = round(sum(item_prices), 2)
    return item_total


# сумма налогов
def get_tax(item_total):
    tax = round(item_total*0.08, 2)
    return tax


# общая сумма заказа
def get_total(item_total, tax):
    total = round(item_total+tax, 2)
    return total

