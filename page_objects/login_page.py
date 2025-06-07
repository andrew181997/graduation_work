from utils.base_case import BaseTestCase
from utils import ENV
from typing import Any


class LoginPage(BaseTestCase):
    page_additional_url = "/#/login"
    logo_svg = '#main-logo'
    login_field = '[formcontrolname="username"]'
    login_place_holder = '#mat-form-field-label-1 > span:nth-child(1)'
    login_validation_massage = '#mat-error-0'
    password_field = '[formcontrolname="password"]'
    password_place_holder = '#mat-form-field-label-3 > span'
    password_validation_massage = "#mat-error-1"
    eye = '.mat - tooltip - trigger'
    entry_button = 'button.mat-focus-indicator'
    change_language_link = ".language-switch-link.language-switch-link"
    remember_me_checkbox = ".mat-checkbox-inner-container>input"
    restore_password = ".login-container__row>a"
    error = "wi-authorization mat-error"
    error500_banner = ".mat-snack-bar-center"

    def login_custom(self, user: str, passwd: str, sucsess: bool=True) -> Any:
        """
        Вход на портал кастомным пользователем
        :param user: Логин пользователя
        :param passwd: Пароль пользователя
        """
        self.send_keys(LoginPage.login_field, user)
        self.send_keys(LoginPage.password_field, passwd)
        self.wait(0.5)
        self.click(LoginPage.entry_button)
        if sucsess:
            self.wait_for_element("[href^='#/op/pm/users/management/edit']", timeout=60)
            self.wait_for_element_visible(".toolbar-name>div")

    def login_as_admin(self):
        """Вход на портал от имени администратора (данные из ENV)"""
        self.send_keys(LoginPage.login_field, ENV.ADMIN_NAME)
        self.send_keys(LoginPage.password_field, ENV.ADMIN_PASS)
        self.click(LoginPage.entry_button)
        self.wait_for_element("[href^='#/op/pm/users/management/edit']")
        self.wait_for_element_visible(".toolbar-name>div")

    def login_as_operator(self):
        """Вход на портал от имени оператора (данные из ENV)"""
        self.send_keys(LoginPage.login_field, ENV.OPERATOR_NAME)
        self.send_keys(LoginPage.password_field, ENV.OPERATOR_PASS)
        self.click(LoginPage.entry_button)
        self.wait_for_element("[href^='#/op/pm/users/management/edit']")
        self.wait_for_element_visible(".toolbar-name>div")

    def login_as_admin_and_operator(self):
        """Вход на портал от имени администратора + оператора (данные из ENV)"""
        self.send_keys(LoginPage.login_field, ENV.ADMIN_OPERATOR_NAME)
        self.send_keys(LoginPage.password_field, ENV.ADMIN_OPERATOR_PASS)
        self.click(LoginPage.entry_button)
        self.wait_for_element("[href^='#/op/pm/users/management/edit']")
        self.wait_for_element_visible(".toolbar-name>div")

    def login_as_root(self):
        self.send_keys(LoginPage.login_field, ENV.ROOT_NAME)
        self.send_keys(LoginPage.password_field, ENV.ROOT_PASS)
        self.click(LoginPage.entry_button)
        self.wait_for_element("[href^='#/op/pm/users/management/edit']")
        self.wait_for_element_visible(".toolbar-name>div")

    """Вход на портал под системными данными администратора с правами root (данные из ENV)"""
    def login_as_administrator(self):
        self.send_keys(LoginPage.login_field, ENV.ADMINISTRATOR_NAME)
        self.send_keys(LoginPage.password_field, ENV.ADMINISTRATOR_PASS)
        self.click(LoginPage.entry_button)
        self.wait_for_element("[href^='#/op/pm/users/management/edit']")
        self.wait_for_element_visible(".toolbar-name>div")