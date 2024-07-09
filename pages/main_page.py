from playwright.sync_api import Page, expect
from random import randint, sample
from vars import number_of_items_on_page, header_text, left_menu_items, filter_menu_items


class MainPage:
    def __init__(self, page: Page):
        item_number = randint(0, number_of_items_on_page - 1)
        self.page = page
        self.base_item = page.locator("div.inventory_item")
        self.random_base_item = page.locator("div.inventory_item").nth(item_number)
        self.open_menu_button = page.locator("#react-burger-menu-btn")
        self.logout_button = page.get_by_text("Logout")
        self.reset_button = page.get_by_text("Reset App State")
        self.app_logo = page.locator("div.app_logo")
        self.shopping_cart_link = page.locator("a.shopping_cart_link")
        self.product_sort_container = page.locator("select.product_sort_container")
        self.inventory_item = page.locator("div.inventory_item")
        self.footer = page.locator("footer.footer")
        self.menu = page.locator("div.bm-menu")
        self.close_menu_button = page.locator("button#react-burger-cross-btn")
        self.menu_items = page.locator("nav.bm-item-list>a")
        self.sort_products = page.locator("select.product_sort_container")
        self.sort_products_options = page.locator("select.product_sort_container>option")
        self.shopping_cart_badge = page.locator("span.shopping_cart_badge")
        self.item_name = page.locator("div.inventory_item_name")
        self.item_img = page.locator("img.inventory_item_img")
        self.item_desc = page.locator("div.inventory_item_desc")
        self.item_price = page.locator("div.inventory_item_price")

    # проверка элементов страницы
    def check_elements_on_main_page(self):
        """Проверка элементов главной страницы"""
        expect(self.open_menu_button, "Отсутствует кнопка раскрытия меню").to_be_visible()
        expect(self.app_logo, f"Некорректный текст хэдера. ОР: {header_text}").to_have_text(header_text)
        expect(self.shopping_cart_link, "Отсутствует ссылка на корзину").to_be_visible()
        expect(self.product_sort_container, "Отсутствует меню сортировки").to_be_visible()
        expect(self.inventory_item, f"Некорректное количество товаров на странице. "
                                    f"ОР: {number_of_items_on_page}").to_have_count(number_of_items_on_page)
        expect(self.footer, "Отсутствует футер").to_be_visible()
        expect(self.random_base_item.filter(has=self.page.locator("div.inventory_item_img")),
               "Не отображается изображение товара").to_be_visible()
        expect(self.random_base_item.filter(has=self.page.locator("div.inventory_item_label>a")),
               "Не отображается название товара").to_be_visible()
        expect(self.random_base_item.filter(has=self.page.locator("div.inventory_item_desc")),
               "Не отображается описание товара").to_be_visible()
        expect(self.random_base_item.filter(has=self.page.locator("div.inventory_item_description div.inventory_item_price")),
               "Не отображается стоимость товара").to_be_visible()
        expect(self.random_base_item.filter(has=self.page.locator("button.btn")),
               "Не отображается кнопка добавления товара в корзину").to_be_visible()

    def check_left_menu_items(self):
        """Проверка пунктов меню"""
        self.open_menu_button.click()
        expect(self.menu, "Меню не отображается").to_be_visible()
        expect(self.close_menu_button, "Не отображается кнопка закрытия меню").to_be_visible()
        expect(self.menu_items,
               f"Некорректное количество пунктов меню. ОР: {len(left_menu_items)}").to_have_count(len(left_menu_items))
        for i in range(len(left_menu_items)):
            current_item = self.menu_items.nth(i).inner_text()
            expected_item = left_menu_items[i]
            assert current_item == expected_item, f"Некорректный пункт меню. ОР: {expected_item}, ФР: {current_item}"

    def check_filter_items(self):
        """Проверка пунктов меню фильтрации"""
        self.sort_products.click()
        for i in range(len(filter_menu_items)):
            current_item = self.sort_products_options.nth(i).inner_text()
            expected_item = filter_menu_items[i]
            assert current_item == expected_item, f"Некорректный пункт меню. ОР: {expected_item}, ФР: {current_item}"

    def logout(self):
        """Выйти из системы"""
        self.open_menu_button.click()
        self.logout_button.click()

    def reset_app_state(self):
        """Сбросить состояние системы"""
        self.open_menu_button.click()
        self.reset_button.click()

    def select_filter(self, option):
        """Выбрать фильтр для сортировки товаров"""
        self.product_sort_container.select_option(option)

    def add_item_to_cart(self, item_number):
        """Добавить товар в корзину и вернуть значение счетчика на значке корзины"""
        add_to_cart_button = self.base_item.get_by_role("button").nth(item_number)
        expect(add_to_cart_button, "Некорректная надпись на кнопке. "
                                   "ОР: 'Add to cart'").to_have_text("Add to cart", timeout=1000)
        add_to_cart_button.click()
        expect(add_to_cart_button,
               "Некорректная надпись на кнопке. ОР: 'Remove'. "
               "Товар не добавлен в корзину").to_have_text("Remove", timeout=1000)
        expect(self.shopping_cart_badge, "Не отображается счетчик на корзине").to_be_visible()
        item_counter_on_cart = self.shopping_cart_badge.inner_text()
        return int(item_counter_on_cart)

    def delete_item_from_cart(self, item_number):
        """Удалить товар из корзины и вернуть значение счетчика на значке корзины"""
        add_to_cart_button = self.base_item.get_by_role("button").nth(item_number)
        expect(add_to_cart_button,
               "Некорректная надпись на кнопке. ОР: 'Remove'").to_have_text("Remove", timeout=1000)
        add_to_cart_button.click()
        expect(add_to_cart_button, "Некорректная надпись на кнопке. ОР: 'Add to cart'. "
                                   "Товар не удален из корзины").to_have_text("Add to cart", timeout=1000)
        if item_number == 0:
            expect(self.shopping_cart_badge, "Отображается счетчик на корзине").not_to_be_visible()
            item_counter_on_cart = 0
        else:
            expect(self.shopping_cart_badge, "Не отображается счетчик на корзине").to_be_visible()
            item_counter_on_cart = self.shopping_cart_badge.inner_text()
        return int(item_counter_on_cart)

    def add_item_to_cart_random(self):
        """Добавить в корзину случайные товары и вернуть индексы добавленных товаров"""
        number_of_items = randint(1, number_of_items_on_page)  # количество добавляемых товаров
        items_numbers = sample(range(0, number_of_items_on_page), number_of_items)  # индексы добавляемых товаров
        for i in items_numbers:
            add_to_cart_button = self.base_item.get_by_role("button").nth(i)
            add_to_cart_button.click()
            expect(add_to_cart_button,
                   "Некорректная надпись на кнопке. ОР: 'Remove'. "
                   "Товар не добавлен в корзину").to_have_text("Remove", timeout=1000)
        current_item_counter_on_cart = int(self.shopping_cart_badge.inner_text())
        assert number_of_items == current_item_counter_on_cart, \
            f"Некорректное отображение счетчика на корзине. ОР: {number_of_items}, ФР: {current_item_counter_on_cart}"
        return items_numbers

    def check_all_item_buttons_state(self, button_state):
        """Проверка состояния всех кнопок на странице товаров"""
        for i in range(number_of_items_on_page):
            add_to_cart_button = self.base_item.get_by_role("button").nth(i)
            expect(add_to_cart_button, f"Некорректная надпись на кнопке. "
                                       f"ОР: '{button_state}'. Товар не удален из корзины").to_have_text(button_state)

    def check_specific_item_buttons_state(self, items_numbers, button_state):
        """Проверить состояние определенных кнопок на странице товаров"""
        for i in items_numbers:
            add_to_cart_button = self.base_item.get_by_role("button").nth(i)
            expect(add_to_cart_button, f"Некорректная надпись на кнопке. ОР: '{button_state}'. "
                                       f"Товар не добавлен в корзину").to_have_text(button_state)

    def get_all_items_info(self):
        """Получить информацию о всех товарах на странице"""
        items = []
        for i in range(number_of_items_on_page):
            new_dict = {
                'item_name':
                    (self.item_name.nth(i).inner_text()),
                'item_img':
                    (self.item_img.nth(i).get_attribute('src')),
                'item_desc':
                    (self.item_desc.nth(i).inner_text()),
                'item_price':
                    float((self.item_price.nth(i).inner_text())[1:])}
            items.append(new_dict)
        return items

    def get_specific_items_info(self, items_numbers):
        """Получить информацию об определенных товарах на странице"""
        items = []
        for i in items_numbers:
            new_dict = {
                'item_name':
                    (self.item_name.nth(i).inner_text()),
                'item_img':
                    (self.item_img.nth(i).get_attribute('src')),
                'item_desc':
                    (self.item_desc.nth(i).inner_text()),
                'item_price':
                    float((self.item_price.nth(i).inner_text())[1:])}
            items.append(new_dict)
        return items

    def get_specific_items_info_without_img(self, items_numbers):
        """Получить информацию об определенных товарах на странице (без изображений)"""
        items = []
        for i in items_numbers:
            new_dict = {
                'item_name': self.item_name.nth(i).inner_text(),
                'item_desc': self.item_desc.nth(i).inner_text(),
                'item_price': float((self.item_price.nth(i).inner_text())[1:])}
            items.append(new_dict)
        return items
