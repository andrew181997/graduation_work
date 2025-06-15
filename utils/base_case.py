import allure
from allure_commons.types import AttachmentType
from seleniumbase import BaseCase
from utils import ENV


class BaseTestCase(BaseCase):
    """
    Базовый класс в котором переопределены методы setUp и tearDown
    """
    page_additional_url = "/#/login"
    exit_button = ".user-menu__logout>button"
    log_out_button = ".user-menu__logout>button"

    def setUp(self, **kwargs):
        super().setUp()
        # self.driver = self.get_new_driver(browser="chrome", headless=True, user_data_dir=None)
        self.maximize_window()
        self.open_page()

    def tearDown(self):
        if self.has_exception():
            with allure.step("FALL"):
                self.attach_report_screenshot()
        if self.is_element_visible(self.exit_button):
            self.log_out()
        super().tearDown()

    def open_page(self):
        """
        Открытие страницы
        """
        self.open(ENV.WISLA_URL + self.page_additional_url)
        self.wait_for_element_visible('.copyright-invert')

    def log_out(self):
        self.click(self.log_out_button)

    def attach_report_screenshot(self):
        allure.attach(self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)