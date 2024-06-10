import pytest
from playwright.sync_api import Page, expect
from random import randint
header_text = "Swag Labs"
number_of_products_on_page = 6
number_of_menu_items = 4
left_menu_items = ["All Items", "About", "Logout", "Reset App State"]
filter_menu_items = ["Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)"]


# проверка элементов страницы
def check_elements_on_page(page):
    item_number = randint(1, number_of_products_on_page)
    expect(page.locator("#react-burger-menu-btn"), "Отсутствует кнопка раскрытия меню").to_be_visible()
    expect(page.locator("div.app_logo"), f"Некорректный текст хэдера. ОР: {header_text}").to_have_text("Swag Labs")
    expect(page.locator("a.shopping_cart_link"), "Отсутствует ссылка на корзину").to_be_visible()
    expect(page.locator("select.product_sort_container"), "Отсутствует меню сортировки").to_be_visible()
    expect(page.locator("div.inventory_item"), f"Некорректное количество товаров на странице. "
                                        f"ОР: {number_of_products_on_page}").to_have_count(number_of_products_on_page)
    expect(page.locator("footer.footer"), "Отсутствует футер").to_be_visible()
    expect(page.locator(f"div.inventory_item:nth-child({item_number})>div.inventory_item_img"),
           "Не отображается изображение товара").to_be_visible()
    expect(page.locator(f"div.inventory_item:nth-child({item_number}) div.inventory_item_label>a"),
           "Не отображается название товара").to_be_visible()
    expect(page.locator(f"div.inventory_item:nth-child({item_number}) div.inventory_item_desc"),
           "Не отображается описание товара").to_be_visible()
    expect(page.locator(f"div.inventory_item:nth-child({item_number}) div.inventory_item_description div.inventory_item_price"),
           "Не отображается стоимость товара").to_be_visible()
    expect(page.locator(f"div.inventory_item:nth-child({item_number}) button.btn"),
           "Не отображается кнопка добавления товара в корзину").to_be_visible()


# проверка пунктов меню
def check_left_menu_items(page):
    page.locator("#react-burger-menu-btn").click()
    expect(page.locator("div.bm-menu"), "Меню не отображается").to_be_visible()
    expect(page.locator("button#react-burger-cross-btn"), "Не отображается кнопка закрытия меню").to_be_visible()
    expect(page.locator("nav.bm-item-list>a"),
           f"Некорректное количество пунктов меню. ОР: {number_of_menu_items}").to_have_count(number_of_menu_items)
    for i in range(len(left_menu_items)):
        current_item = page.locator("nav.bm-item-list>a").nth(i).inner_text()
        expected_item = left_menu_items[i]
        assert current_item == expected_item, f"Некорректный пункт меню. ОР: {expected_item}, ФР: {current_item}"


# проверка пунктов меню фильтрации
def check_filter_items(page):
    page.locator("select.product_sort_container").click()
    for i in range(len(filter_menu_items)):
        current_item = page.locator("select.product_sort_container>option").nth(i).inner_text()
        expected_item = filter_menu_items[i]
        assert current_item == expected_item, f"Некорректный пункт меню. ОР: {expected_item}, ФР: {current_item}"




