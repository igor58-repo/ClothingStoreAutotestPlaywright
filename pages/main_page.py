from playwright.sync_api import expect
from random import randint, sample


# проверка элементов страницы
def check_elements_on_page(page, number_of_products_on_page, header_text):
    item_number = randint(1, number_of_products_on_page)
    expect(page.locator("#react-burger-menu-btn"), "Отсутствует кнопка раскрытия меню").to_be_visible()
    expect(page.locator("div.app_logo"), f"Некорректный текст хэдера. ОР: {header_text}").to_have_text(header_text)
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
def check_left_menu_items(page, number_of_menu_items, left_menu_items):
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
def check_filter_items(page, filter_menu_items):
    page.locator("select.product_sort_container").click()
    for i in range(len(filter_menu_items)):
        current_item = page.locator("select.product_sort_container>option").nth(i).inner_text()
        expected_item = filter_menu_items[i]
        assert current_item == expected_item, f"Некорректный пункт меню. ОР: {expected_item}, ФР: {current_item}"


# добавление товара в корзину
def add_item_to_cart(page, item_number):
    add_to_cart_button = page.locator(f"div.inventory_item:nth-child({item_number+1}) button.btn")
    expect(add_to_cart_button, "Некорректная надпись на кнопке. ОР: 'Add to cart'").to_have_text("Add to cart")
    add_to_cart_button.click()
    expect(add_to_cart_button,
           "Некорректная надпись на кнопке. ОР: 'Remove'. Товар не добавлен в корзину").to_have_text("Remove")
    shopping_cart_badge = page.locator("span.shopping_cart_badge")
    expect(shopping_cart_badge, "Не отображается счетчик на корзине").to_be_visible()
    item_counter_on_cart = shopping_cart_badge.inner_text()
    return int(item_counter_on_cart)


# удаление товара из корзины
def delete_item_from_cart(page, item_number):
    add_to_cart_button = page.locator(f"div.inventory_item:nth-child({item_number+1}) button.btn")
    expect(add_to_cart_button,
           "Некорректная надпись на кнопке. ОР: 'Remove'").to_have_text("Remove")
    add_to_cart_button.click()
    expect(add_to_cart_button,
           "Некорректная надпись на кнопке. ОР: 'Add to cart'. Товар не удален из корзины").to_have_text("Add to cart")
    shopping_cart_badge = page.locator("span.shopping_cart_badge")
    if item_number == 0:
        expect(shopping_cart_badge, "Отображается счетчик на корзине").not_to_be_visible()
        item_counter_on_cart = 0
    else:
        expect(shopping_cart_badge, "Не отображается счетчик на корзине").to_be_visible()
        item_counter_on_cart = shopping_cart_badge.inner_text()
    return int(item_counter_on_cart)


# добавление в корзину случайных товаров
def add_item_to_cart_random(page, number_of_products_on_page):
    number_of_products = randint(1, number_of_products_on_page)
    products_numbers = sample(range(1, number_of_products_on_page + 1), number_of_products)
    for i in products_numbers:
        add_to_cart_button = page.locator(f"div.inventory_item:nth-child({i}) button.btn")
        add_to_cart_button.click()
        expect(add_to_cart_button,
               "Некорректная надпись на кнопке. ОР: 'Remove'. Товар не добавлен в корзину").to_have_text("Remove")
    shopping_cart_badge = page.locator("span.shopping_cart_badge")
    current_item_counter_on_cart = int(shopping_cart_badge.inner_text())
    assert number_of_products == current_item_counter_on_cart, \
        f"Некорректное отображение счетчика на корзине. ОР: {number_of_products}, ФР: {current_item_counter_on_cart}"
    return products_numbers


# проверить состояние всех кнопок на странице товаров
def check_all_item_buttons_state(page, number_of_products_on_page, button_state):
    for i in range(number_of_products_on_page):
        add_to_cart_button = page.locator(f"div.inventory_item:nth-child({i+1}) button.btn")
        expect(add_to_cart_button, f"Некорректная надпись на кнопке. "
                                   f"ОР: '{button_state}'. Товар не удален из корзины").to_have_text(button_state)


# проверить состояние определенных кнопок на странице товаров
def check_specific_item_buttons_state(page, products_numbers, button_state):
    for i in products_numbers:
        add_to_cart_button = page.locator(f"div.inventory_item:nth-child({i}) button.btn")
        expect(add_to_cart_button, f"Некорректная надпись на кнопке. ОР: '{button_state}'. "
                                   f"Товар не добавлен в корзину").to_have_text(button_state)


# получить информацию о всех товарах на странице
def get_all_items_info(page, number_of_products_on_page):
    items = []
    for i in range(number_of_products_on_page):
        new_dict = {
            'item_name':
                (page.locator("div.inventory_item_name").nth(i).inner_text()),
            'item_img':
                (page.locator("img.inventory_item_img").nth(i).get_attribute('src')),
            'item_desc':
                (page.locator("div.inventory_item_desc").nth(i).inner_text()),
            'item_price':
                float((page.locator("div.inventory_item_price").nth(i).inner_text())[1:])}
        items.append(new_dict)
    return items


# получить информацию об определенных товарах на странице
def get_specific_items_info(page, product_numbers):
    items = []
    for i in product_numbers:
        new_dict = {
            'item_name':
                (page.locator("div.inventory_item_name").nth(i-1).inner_text()),
            'item_img':
                (page.locator("img.inventory_item_img").nth(i-1).get_attribute('src')),
            'item_desc':
                (page.locator("div.inventory_item_desc").nth(i-1).inner_text()),
            'item_price':
                float((page.locator("div.inventory_item_price").nth(i-1).inner_text())[1:])}
        items.append(new_dict)
    return items
