import pytest
from datetime import datetime
from playwright.sync_api import Page
from take_screenshot import take_screenshot


@pytest.fixture()
def page(context):
    page: Page = context.new_page()
    page.set_viewport_size({'height': 1000, 'width': 2000})
    yield page


# исправление отображения кириллицы в pytest.parametrize
def pytest_make_parametrize_id(config, val):
    return repr(val)


# заголовок отчета
def pytest_html_report_title(report):
    report.title = "Clothing Store Autotest"


# добавление дополнительных столбцов Description и Time
def pytest_html_results_table_header(cells):
    #cells.insert(1, '<th class="sortable text" data-column-type="text">Notes</th>')
    cells.insert(1, '<th class="sortable text" data-column-type="text">Description</th>')
    cells.insert(3, '<th class="sortable time" data-column-type="time">Time</th>')
    cells.pop()


# заполнение столбцов description и Time
def pytest_html_results_table_row(report, cells):
    #cells.insert(1, f"<td>{report.fail_reason}</td>")
    cells.insert(1, f"<td>{report.description}</td>")
    start = datetime.fromtimestamp(report.start)
    cells.insert(2, f'<td class="col-time">{start}</td>')
    cells.pop()


# hook для перехвата и модификации данных результатов тестов (добавление ссылки на скриншот)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.start = call.start
    #report.fail_reason = call.excinfo.value if call.excinfo else None
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        if report.failed or "page" in item.funcargs:
            img_url = ''
            page = item.funcargs["page"]
            img_url = take_screenshot(page)
            extra.append(pytest_html.extras.png(img_url))
        report.extras = extra

