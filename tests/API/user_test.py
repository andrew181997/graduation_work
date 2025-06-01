import pytest
import allure
from dataclasses import replace,asdict
import ENV
from ENV import OPERATOR_PASS, ROOT_PASS
from api.api_methods import HttpMethods
from api.login_methods import LoginApi
from api.module.user import UserData
from api.user_methods import UsersAPI
import copy
import uuid

@allure.title("Проверка кода ответа на корректный запрос получения списка пользователей")
def test_get_list_users():
    result = UsersAPI.get_list_users()
    print(result.json())
    assert result.status_code == 200

@pytest.fixture
def user_data():
    random_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
    return UserData(
        editByOwnerOnly=0,
        login=random_email,
        fullName="Test User",
        userRoles=["SIMPLE_USER"],
        phone="",
        newPassword="secure_password123",
        additionalEmails=[],
        address={},
        preferences={
            "troubleTicketsPopup": 1,
            "slaReportsPublishPopup": 0,
            "welcomeMessagePopup": 0,
            "actionEventPopup": 0,
            "useScale": 1,
            "ips": [""],
            "notificationSubscriptions": [],
            "mobileNotificationSubscriptions": [],
            "notificationChannels": []
        },
        contracts=[],
        parties=[],
        confirmPassword="secure_password123"
    )



@allure.title("Проверка запроса на создание пользователя")
@pytest.mark.parametrize("user_data_modifications, expected_status", [
    ({"userRoles": ["SIMPLE_USER"]}, 200),
    ({"userRoles": ["SIMPLE_USER", "SLA_OPERATOR"]}, 200),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"]}, 200),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"]}, 200),
    ({"userRoles": []}, 200)
])
def test_create_user(user_data, user_data_modifications, expected_status):
    test_data = replace(user_data, **user_data_modifications) # Копируем в переменную тестовые данные для теста
    response = UsersAPI.create_user(test_data,ENV.ROOT_NAME,ROOT_PASS)
    print(response.status_code)
    print(response.text)
    assert response.status_code == expected_status, \
        f"Ожидался {expected_status}, получили {response.status_code}. Ответ: {response.text}"

    response_data = response.json()

    assert response_data.get("login") == test_data.login, "Логин не совпадает"
    assert response_data.get("userRoles") == test_data.userRoles, "Роль не совпадает"

@allure.title("Проверка , что нет возможности залогиниться блокированному пользователю")
@pytest.mark.parametrize("user_data_modifications, expected_status", [
    ({"userRoles": ["SIMPLE_USER"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SLA_OPERATOR"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"]}, 401),
    ({"userRoles": []}, 401)
])
def test_block_user(user_data,user_data_modifications, expected_status):
    test_data = replace(user_data, **user_data_modifications) # Копируем в переменную тестовые данные для теста
    response = UsersAPI.create_user(test_data)
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
@pytest.mark.parametrize("user_data_modifications, expected_status", [
    ({"userRoles": ["SIMPLE_USER"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SLA_OPERATOR"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"]}, 401),
    ({"userRoles": []}, 401)
])
def test_archive_user(user_data,user_data_modifications, expected_status):
    test_data = replace(user_data, **user_data_modifications) # Копируем в переменную тестовые данные для теста
    response = UsersAPI.create_user(test_data)
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
@pytest.mark.parametrize("user_data_modifications, expected_status", [
    ({"userRoles": ["SIMPLE_USER"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SLA_OPERATOR"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR", "SLA_OPERATOR"]}, 401),
    ({"userRoles": ["SIMPLE_USER", "SYSTEM_ADMINISTRATOR"]}, 401),
    ({"userRoles": []}, 401)
])
def test_clean_up_user(user_data,user_data_modifications, expected_status):
    test_data = replace(user_data, **user_data_modifications) # Копируем в переменную тестовые данные для теста
    response = UsersAPI.create_user(test_data)
    response_data = response.json()
    entity_id = response_data.get("id")
    UsersAPI.clean_up(entity_id)
    login = response_data.get("login")
    password = response_data.get("newPassword")
    result_login = LoginApi.auth(login, password)
    print(result_login.json())
    assert result_login.status_code == expected_status, f"Код ответа {result_login.status_code}"
