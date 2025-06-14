import allure
import pytest
from utils import ENV
from page_objects.login_page import LoginPage


@allure.suite("Проверка страницы авторизации")
@pytest.mark.smoke
class LoginTest(LoginPage):

    @allure.title("Проверка элементов на странице авторизации")
    def test_login_page_content(self):

        with allure.step("Проверка элементов страницы авторизации"):
            self.attach_report_screenshot()
            self.assert_url(ENV.WISLA_URL + '/#/login')
            self.assert_element_present(LoginPage.logo_svg)
            assert self.is_element_visible(LoginPage.login_field)
            assert self.get_text(self.entry_button) == 'ВОЙТИ'
            assert self.get_text(self.change_language_link) == "Continue in English"
            assert self.get_attribute(selector=self.remember_me_checkbox, attribute="aria-checked") == "false"
            assert self.get_text(self.restore_password) == "Восстановить пароль"
            assert self.get_text(self.password_place_holder) == 'Пароль'
            assert self.get_text(self.login_place_holder) == 'Электронная почта'

        with allure.step("Пользователь может выбрать чек-бокс запомнить меня"):
            self.click(self.remember_me_checkbox)
            assert self.get_attribute(selector=self.remember_me_checkbox, attribute="aria-checked") == "true"
            self.attach_report_screenshot()

        with allure.step("Проверяем видимость валидационного сообщения логина"):
            self.click(self.login_field)
            self.focus(self.password_field)
            self.attach_report_screenshot()
            assert self.get_text(self.login_validation_massage) == "введите адрес электронной почты"

        with allure.step("Проверяем видимость валидационного сообщения пароля"):
            self.click(self.password_field)
            self.focus(self.login_field)
            self.attach_report_screenshot()
            assert self.get_text(self.password_validation_massage) == "введите пароль"

    @allure.severity("blocker")
    @allure.title("Пользователь может авторизоваться на сайте")
    @allure.description("""Тест авторизуется под учетной записью администратора и оператора, после
    чего ожидает появления иконки пользователя в боковой панели меню""")
    def test_correct_login_and_find_user_logo(self):
        """Проверяем авторизацию с корректным логином и паролем"""

        with allure.step("Вход на портал с корректным логином и паролем"):
            self.login_custom(user=ENV.ADMIN_OPERATOR_NAME, passwd=ENV.ADMIN_OPERATOR_PASS)

        with allure.step("Ожидание загрузки страницы, поиск блока с иконкой пользователя"):
            self.wait_for_element('.img-account')
            self.attach_report_screenshot()

    @allure.title("Проверка валидационного сообщения при попытке входа с некорректными данными")
    @allure.description("""Тест вводит неправильные авторизационные данные, после чего ожидает 
        валидационного сообщения: ошибочный адрес эл. почты/пароль или пользователь заблокирован""")
    def test_incorrect_login_and_pass(self):
        """Проверяем сообщение о некорректных данных авторизации при некорректном логине"""

        with allure.step("Ввод некорректных данных авторизации на странице и попытка входа"):
            self.login_custom(user=ENV.BLOCKED_USER_NAME, passwd=ENV.BLOCKED_USER_PASS, sucsess=False)

        with allure.step("Сверка валидационного сообщения"):
            self.wait_for_element_visible(LoginPage.error)
            self.attach_report_screenshot()
            assert self.get_text('.mat-error.send-error') == ('ошибочный адрес эл. почты/пароль '
                                                              'или пользователь заблокирован')