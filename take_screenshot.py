from datetime import datetime


# создание скриншота
def take_screenshot(page):
    time_now = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    filename = f'{time_now}.jpg'
    page.screenshot(path=f'reports/screenshots/{filename}')
    img_url = f'screenshots/{filename}'
    return img_url
