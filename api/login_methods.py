from api.api_methods import HttpMethods
import ENV


class LoginApi:
    endpoint = "/engine/api/auth/login"

    @staticmethod
    def auth(user: str, passwd: str):
        result = HttpMethods.post(url=ENV.WISLA_URL + LoginApi.endpoint,
                                  body={"username": user, "password": passwd},
                                  header=HttpMethods.auth_headers)
        return result

    @staticmethod
    def get_token(user, passwd) -> dict[str:str]:
        """
        Метод отправляет запрос на авторизацию и возвращает токен,
        необходимый для дальнейшего использования в заголовках
        Пример: token = LoginApi.get_token(user=ENV.ADMIN_OPERATOR_NAME, passwd=ENV.ADMIN_OPERATOR_PASS)
        затем header=token
        :param user: имя пользователя
        :param passwd: пароль для авторизации
        :return: access-token (токен авторизации пользователя)
        """
        result = HttpMethods.post(url=ENV.WISLA_URL + LoginApi.endpoint,
                                  body={"username": user, "password": passwd},
                                  header=HttpMethods.auth_headers).json().get("token")
        HttpMethods.headers.update({'Authorization': f'wi-access_token-{result}'})
        return HttpMethods.headers