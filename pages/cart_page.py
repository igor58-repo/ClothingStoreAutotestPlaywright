import pytest
from playwright.sync_api import Page, expect

continue_shopping_text = "Continue Shopping"
checkout_text = "Checkout"
cart_quantity_text = "QTY"
cart_desc_text = "Description"


# проверка элементов корзины
def check_elements_cart(page: Page, cart_state):
    cart_quantity = page.locator("div.cart_quantity_label")
    cart_desc = page.locator("div.cart_desc_label")
    continue_shopping_button = page.locator("button#continue-shopping")
    checkout_button = page.locator("button#checkout")
    cart_item = page.locator("div.cart_item")
    expect(cart_quantity, "Не отображается элемент Количество товаров в корзине").to_be_visible()
    expect(cart_quantity, f"Некорректный текст. ОР: {cart_quantity_text}").to_have_text(cart_quantity_text)
    expect(cart_desc, "Не отображается элемент Описание товаров в корзине").to_be_visible()
    expect(cart_desc, f"Некорректный текст. ОР: {cart_desc_text}").to_have_text(cart_desc_text)
    expect(continue_shopping_button, f"Не отображается кнопка {continue_shopping_text}").to_be_visible()
    expect(continue_shopping_button, f"Некорректный текст на кнопке. "
                                     f"ОР: {continue_shopping_text}").to_have_text(continue_shopping_text)
    expect(checkout_button, f"Не отображается кнопка {checkout_text}").to_be_visible()
    expect(checkout_button, f"Некорректный текст на кнопке. ОР: {checkout_text}").to_have_text(checkout_text)
    if cart_state == "empty":
        expect(cart_item, "Корзина должна быть пустой").not_to_be_visible()
    elif cart_state == "not_empty":
        expect(page.locator("div.cart_quantity").first, "Не отображается количество товаров в корзине").to_be_visible()
        expect(page.locator("div.inventory_item_name").first, "Не отображается заголовок товара").to_be_visible()
        expect(page.locator("div.inventory_item_desc").first, "Не отображается описание товара").to_be_visible()
        expect(page.locator("div.inventory_item_price").first, "Не отображается стоимость товара").to_be_visible()
        expect(page.get_by_role("button", name='Remove').first, "Не отображается кнопка удаления товара").to_be_visible()
    else:
        assert False, "Параметр cart_state должен иметь значения empty или not_empty"


# получить информацию о всех товарах в корзине
def get_all_items_in_cart_info(page: Page, number_of_products_on_page):
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


# получить информацию об определенных товарах на странице
def get_specific_items_info(page: Page, product_numbers):
    items = []
    for i in product_numbers:
        new_dict = {
            'item_name':
                (page.locator("div.inventory_item_name").nth(i-1).inner_text()),
            'item_desc':
                (page.locator("div.inventory_item_desc").nth(i-1).inner_text()),
            'item_price':
                float((page.locator("div.inventory_item_price").nth(i-1).inner_text())[1:])}
        items.append(new_dict)
    return items


# удаление товара из корзины
def delete_all_items_from_cart(page: Page, number_of_products_on_cart):
    for i in reversed(range(number_of_products_on_cart)):
        remove_from_cart_button = page.locator("button.cart_button").first
        expect(remove_from_cart_button, "Некорректная надпись на кнопке. ОР: 'Remove'").to_have_text("Remove")
        remove_from_cart_button.click()
        if i == 0:
            expect(page.locator("span.shopping_cart_badge"), "Отображается счетчик на корзине").not_to_be_visible()
        else:
            expect(page.locator("span.shopping_cart_badge"), "Не отображается счетчик на корзине").to_be_visible()
            current_item_counter_on_cart = page.locator("span.shopping_cart_badge").inner_text()
            assert i == int(current_item_counter_on_cart), \
                (f"Некорректное отображение счетчика на корзине. ОР: {i}, "
                 f"ФР: {current_item_counter_on_cart}")
    expect(page.locator("div.cart_item"), "Товары не удалены из корзины").not_to_be_visible()
