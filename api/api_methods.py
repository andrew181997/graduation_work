import json
from dataclasses import asdict
from typing import Any
import requests
import ENV



class HttpMethods:
    """Базовый клас в котором описана логика отправки HTTP запросов"""
    auth_headers = {"X-Requested-With": "XMLHttpRequest"}
    headers = {"Content-Type": "application/json", "Accept-Language": "ru-RU"}
    cookie = ""

    @staticmethod
    def get(url: str, header: dict) -> requests.Response:
        """
        Метод для отправки базового get
        :param url: url
        :param header: заголовки
        :return:  Объект ответа библиотеки requests
        """
        result = requests.get(url,
                              headers=header,
                              cookies=HttpMethods.cookie)
        return result

    @staticmethod
    def post(url: str, body: json, header: dict[str: str]) -> requests.Response:
        """
        Метод для отправки базового post
        :param url: url
        :param body: тело запроса (json)
        :param header: заголовки
        :return:  Объект ответа библиотеки requests
        """
        result = requests.post(url, json=body, headers=header, cookies=HttpMethods.cookie)
        return result


    @staticmethod
    def put(url, body) -> requests.Response:
        """
        Метод для отправки базового put
        :param url: url
        :param body: тело запроса (json)
        :return:  Объект ответа библиотеки requests
        """
        result = requests.post(url, json=body, headers=HttpMethods.headers, cookies=HttpMethods.cookie)
        return result

    @staticmethod
    def delete(url, header) -> requests.Response:
        """
        Метод для отправки базового delete
        :param url: url
        :param header: заголовки
        :return:  Объект ответа библиотеки requests
        """
        result = requests.delete(url, headers=header, cookies=HttpMethods.cookie)
        return result

    @staticmethod
    def patch(url, header) -> requests.Response:
        """
        Метод для отправки базового patch
        :param url: url
        :param header: заголовки
        :return:  Объект ответа библиотеки requests
        """
        result = requests.patch(url, headers=header, cookies=HttpMethods.cookie)
        return result

    # @staticmethod
    # def archive_entity(endpoint: str, data: Any, user: str, passwd: str) -> requests.Response:
    #     """
    #     Метод для архивации любой сущности
    #     """
    #     token = LoginApi.get_token(user=user, passwd=passwd)
    #     body = asdict(data)
    #     return HttpMethods.post(url=ENV.WISLA_URL + endpoint, body=body, header=token)

