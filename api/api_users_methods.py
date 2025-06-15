import allure
import time
from dataclasses import asdict
import requests
from api.api_login_methods import LoginApi
from api.api_methods import HttpMethods

# from utils.bd_controll.halpers.user_data_from_name import get_party_data
from utils import ENV
from api.module.user import UserData


class UsersAPI:
    endpoint = "/engine/api/v1/users?search=&limit=50"

    @staticmethod
    def get_list_users() -> requests.Response:
        """
        Метод для получения списка пользователей в системе
        :return: Response объект
        """
        token = LoginApi.get_token(user=ENV.ADMIN_OPERATOR_NAME,
                                   passwd=ENV.ADMIN_OPERATOR_PASS)
        body = {
            "roles": [],
            "status": []
            }
        result = HttpMethods.post(url=ENV.WISLA_URL + UsersAPI.endpoint,
                                  body=body,
                                  header=token)
        return result


    @staticmethod
    def create_user(user_data: UserData) -> requests.Response:
        """
        Создает пользователя через API

        Args:
            user_data: Объект UserCreateRequest с данными пользователя

        Returns:
            Response: Ответ от сервера
        """
        # Конвертируем dataclass в словарь
        body = asdict(user_data)
        endpoint = "/engine/api/v1/users/save"
        token = LoginApi.get_token(user=ENV.ROOT_NAME, passwd=ENV.ROOT_PASS)

        result = HttpMethods.post(url=ENV.WISLA_URL + endpoint, body=body, header=token)
        return result

    @staticmethod
    def block_user(entity_id) -> requests.Response:
        """
        Метод для блокировки пользователя
        :param entity_id: id пользователя
        :return:
        """
        endpoint = (f"/engine/api/v1/users/apply-action?entityIds={entity_id}&"
                    f"actionType=BLOCK&selectAllMode=false")
        token = LoginApi.get_token(user=ENV.ROOT_NAME, passwd=ENV.ROOT_PASS)
        result = HttpMethods.patch(url=ENV.WISLA_URL + endpoint, header=token)
        return result

    @staticmethod
    def archive_user(entity_id) -> requests.Response:
        """
        Метод для архивации пользователя
        :param entity_id: id пользователя
        :return:
        """
        endpoint = (f"/engine/api/v1/users/apply-action?entityIds={entity_id}&"
                    f"actionType=ARCHIVE&selectAllMode=false")
        token = LoginApi.get_token(user=ENV.ROOT_NAME, passwd=ENV.ROOT_PASS)
        result = HttpMethods.patch(url=ENV.WISLA_URL + endpoint, header=token)
        return result

    @staticmethod
    def delete_user(entity_id) -> requests.Response:
        """
        Метод для удаления пользователя
        :param entity_id: id пользователя
        :return:
        """
        endpoint = (f"/engine/api/v1/users/apply-action?entityIds={entity_id}&"
                    f"actionType=REMOVE&selectAllMode=false")
        token = LoginApi.get_token(user=ENV.ROOT_NAME, passwd=ENV.ROOT_PASS)
        result = HttpMethods.patch(url=ENV.WISLA_URL + endpoint, header=token)
        return result

    @staticmethod
    def clean_up(entity_id):
        """
        Общий метод очистки тестовых данных пользователя (блокировка-архивация-удаление)
        :param entity_id: id пользователя
        :return:
        """
        with allure.step("Блокировка пользователя"):
            is_blocked = UsersAPI.block_user(entity_id)
            print(is_blocked.text)
            print(is_blocked.status_code)
            assert is_blocked.status_code == 200
            time.sleep(1)
        with allure.step("Архивация пользователя"):
            is_archived = UsersAPI.archive_user(entity_id)
            print(is_archived.text)
            print(is_archived.status_code)
            assert is_archived.status_code == 200
            time.sleep(1)
        with allure.step("Удаление пользователя"):
            is_deleted = UsersAPI.delete_user(entity_id)
            print(is_deleted.text)
            print(is_deleted.status_code)
            assert is_deleted.status_code == 200
        return


# if __name__ == "__main__":
#     user = UserData(full_name="123", passwd='1q2w3e', login="2@2.ru", parties='Wellink', roles=["SIMPLE_USER",])
#     r = UsersAPI.delete_user(1538)
#     print(r.request.body)
#     print(r.status_code)
#     print(r.text)