import requests
from dataclasses import asdict
from utils import ENV
from api.api_methods import HttpMethods
from api.api_login_methods import LoginApi
from api.module.contractors import ContractorData
from typing import Optional


class ContractorsAPI:
    endpoint = "/engine/api/v1/parties"

    @staticmethod
    def get_list_contractors(kind_of_list: str = "SINGLE_LEVEL") -> requests.Response:
        """
        Метод для получения списка контрагентов в обычном виде и в виде дерева
        :param kind_of_list: Доступно только 2 варианта: SINGLE_LEVEL или HIERARCHICAL
                иначе будет возбуждена ошибка ValueError
        :return: Response объект, список контрагентов
        """
        available_kinds_for_list = ("SINGLE_LEVEL", "HIERARCHICAL")
        if kind_of_list not in available_kinds_for_list:
            raise ValueError("Доступны только SINGLE_LEVEL/HIERARCHICAL "
                             "типы списка для контрагентов")
        else:
            token = LoginApi.get_token(user=ENV.ROOT_NAME,
                                       passwd=ENV.ROOT_PASS)
            body = {"roles": [],
                    "status": [],
                    "$kind_of_list": [kind_of_list]
                    }
            if kind_of_list == "HIERARCHICAL":
                ContractorsAPI.endpoint += "/tree"
            result = HttpMethods.post(url=ENV.WISLA_URL + ContractorsAPI.endpoint,
                                      body=body,
                                      header=token)
        return result

    @staticmethod
    def create_contractor(contractor: ContractorData) -> requests.Response:
        """
        Метод для создания контрагента с указанным именем
        # :param name: имя контрагента
        :return: Объект ответа
        """
        endpoint = "/engine/api/v1/parties/save"
        token = LoginApi.get_token(user=ENV.ROOT_NAME, passwd=ENV.ROOT_PASS)
        body = asdict(contractor)
        result = HttpMethods.post(url=ENV.WISLA_URL + endpoint, body=body, header=token)
        return result

    @staticmethod
    def archive_contractor(entity_id: int) -> requests.Response:
        """
        Метод архивации контрагента
        :param entity_id: id контрагента для архивации
        :return: Объект ответа
        """
        endpoint = (f"/engine/api/v1/parties/apply-action?entityIds={entity_id}&"
                    f"actionType=ARCHIVE&selectAllMode=false")
        token = LoginApi.get_token(user=ENV.ROOT_NAME, passwd=ENV.ROOT_PASS)
        result = HttpMethods.patch(url=ENV.WISLA_URL + endpoint, header=token)
        return result

    @staticmethod
    def delete_contractor(entity_id: int) -> requests.Response:
        """
        Метод для удаления контрагента
        :param entity_id: id контрагента
        :return:
        """
        endpoint = (f"/engine/api/v1/parties/apply-action?entityIds={entity_id}&"
                    f"actionType=REMOVE&selectAllMode=false")
        token = LoginApi.get_token(user=ENV.ROOT_NAME, passwd=ENV.ROOT_PASS)
        result = HttpMethods.patch(url=ENV.WISLA_URL + endpoint, header=token)
        return result