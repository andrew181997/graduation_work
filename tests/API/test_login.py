import allure
from api.api_login_methods import LoginApi
from utils import ENV



class TestLoginAPI:

    @staticmethod
    @allure.step("Отправка корректного запроса")
    def correct_login():
        result_post = LoginApi.auth(user=ENV.ADMIN_OPERATOR_NAME, passwd=ENV.ADMIN_OPERATOR_PASS)
        return result_post

    @staticmethod
    @allure.step("Отправка некорректного запроса")
    def incorrect_login():
        result_post = LoginApi.auth(user="x@x.ru", passwd="xxs")
        return result_post

    @allure.title("Проверка кода ответа на корректный запрос авторизации")
    def test_correct_login_response_code(self):
        with allure.step("Получание ответа, проверка статус-кода"):
            assert TestLoginAPI.correct_login().status_code == 200

    @allure.title("Проверка содержимого json в ответе на запрос авторизации")
    def test_correct_login_body_keys(self):
        keys = ("licenseStatus", "refreshToken", "token")
        with allure.step("сверка ключей в ответе на запрос авторизации"):
            assert set((TestLoginAPI.correct_login().json().keys())) == set(keys)

    @allure.title("Проверка, что в корректном запросе авторизации не истекла лицензия")
    def test_licence_status(self):
        res = TestLoginAPI.correct_login().json()
        assert res.get("licenseStatus") == 'true'

    @allure.title("Проверка статус-кода при попытке автризоваться с некорректными данными")
    def test_incorrect_login_response_code(self):
        with allure.step("Проверка статус-кода ответа"):
            assert TestLoginAPI.incorrect_login().status_code == 401
