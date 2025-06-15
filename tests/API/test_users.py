import pytest
import allure
from dataclasses import replace
from utils import ENV
from utils.ENV import ROOT_PASS
from api.api_login_methods import LoginApi
from api.module.user import UserData
from api.api_users_methods import UsersAPI
import uuid

class TestContractorsApi:

    @allure.title("Проверка кода ответа на корректный запрос получения списка пользователей")
    def test_get_list_users(self):
        result = UsersAPI.get_list_users()
        print(result.json())
        assert result.status_code == 200


    @allure.title("Проверка запроса на создание пользователя")
    @pytest.mark.parametrize("roles,expected_status",[
        (["SIMPLE_USER"], 200),
        (["SIMPLE_USER", "SLA_OPERATOR"], 200),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"], 200),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"], 200),
        ([], 200),
        (["INVALID_USER"], 400)
    ])
    def test_create_user(self,roles, expected_status):
        user = UserData()
        # Подменяем userRoles
        user.userRoles = roles
        # Отправляем запрос
        response = UsersAPI.create_user(user)
        assert response.status_code == expected_status,f"Ожидался {expected_status}, получили {response.status_code}. Ответ: {response.text}"
        if expected_status == 200:
            response_data = response.json()
            assert set(response_data["userRoles"]) == set(roles), "Роли не совпадают"


    @allure.title("Проверка , что нет возможности залогиниться блокированному пользователю")
    @pytest.mark.parametrize("roles,expected_status", [
        (["SIMPLE_USER"], 401),
        (["SIMPLE_USER", "SLA_OPERATOR"], 401),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"], 401),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"], 401),
        ([], 401)
    ])
    def test_block_user(self,roles, expected_status):
        user = UserData()
        # Подменяем userRoles
        user.userRoles = roles
        # Отправляем запрос
        response = UsersAPI.create_user(user)
        response_data = response.json()
        entity_id = response_data.get("id")
        result = UsersAPI.block_user(entity_id)
        assert result.status_code == 200 , f"Код ответа {result.status_code}"
        login = response_data.get("login")
        password = response_data.get("newPassword")
        result_login = LoginApi.auth(login,password)
        print(result_login.json())
        assert result_login.status_code == expected_status , f"Код ответа {result_login.status_code}"

    @allure.title("Проверка , что нет возможности залогиниться архивному пользователю")
    @pytest.mark.parametrize("roles,expected_status", [
        (["SIMPLE_USER"], 401),
        (["SIMPLE_USER", "SLA_OPERATOR"], 401),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"], 401),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"], 401),
        ([], 401)
    ])
    def test_archive_user(self,roles, expected_status):
        user = UserData()
        # Подменяем userRoles
        user.userRoles = roles
        # Отправляем запрос
        response = UsersAPI.create_user(user)
        response_data = response.json()
        entity_id = response_data.get("id")
        is_block = UsersAPI.block_user(entity_id)
        assert is_block.status_code == 200, f"Код ответа {is_block.status_code}"
        is_archive =UsersAPI.archive_user(entity_id)
        assert is_archive.status_code == 200, f"Код ответа {is_archive.status_code}"
        login = response_data.get("login")
        password = response_data.get("newPassword")
        result_login = LoginApi.auth(login, password)
        print(result_login.json())
        assert result_login.status_code == expected_status, f"Код ответа {result_login.status_code}"

    @allure.title("Проверка , что нет возможности залогиниться удаленному пользователю")
    @pytest.mark.parametrize("roles,expected_status", [
        (["SIMPLE_USER"], 401),
        (["SIMPLE_USER", "SLA_OPERATOR"], 401),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"], 401),
        (["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"], 401),
        ([], 401)
    ])
    def test_clean_up_user(self,roles, expected_status):
        user = UserData()
        # Подменяем userRoles
        user.userRoles = roles
        # Отправляем запрос
        response = UsersAPI.create_user(user)
        response_data = response.json()
        entity_id = response_data.get("id")
        UsersAPI.clean_up(entity_id)
        login = response_data.get("login")
        password = response_data.get("newPassword")
        result_login = LoginApi.auth(login, password)
        print(result_login.json())
        assert result_login.status_code == expected_status, f"Код ответа {result_login.status_code}"
