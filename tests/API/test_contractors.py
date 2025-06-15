import allure
from api.module.contractors import ContractorData
from api.api_contractors_methods import ContractorsAPI



class TestContractorsApi:

    @allure.title("Создание контрагента")
    def test_create_contractor(self):
        result = ContractorsAPI.create_contractor(ContractorData())
        assert result.status_code == 200, f"Ошибка, кода ответа {result.status_code}"



    @allure.title("Просмотр списка контрагентов")
    def test_get_contractors(self):
        result = ContractorsAPI.get_list_contractors()
        assert result.status_code == 200, f"Ошибка , код ответа {result.status_code,result.json()}"
        assert result.json() is not None


    @allure.title("Архивация контрагента,тест специально будет падать с 500 ошибкой")
    def test_archive_contractor(self):
        contractor2 = ContractorData(users=[{"id": 11550, "name": "с@c.ru"}])
        ContractorsAPI.create_contractor(contractor2)
        response = ContractorsAPI.get_list_contractors() # Запрашиваем список всех контрагентов, потому что в ответе при создании контрагента приходит пустой json
        result = response.json() # Через переменную , что бы найти по ID последнего созданного контрагента
        id_entity = result["list"][0]["id"] # берем в переменную id контрагента
        result = ContractorsAPI.archive_contractor(id_entity)
        assert result.status_code == 200, f"Ошибка , код ответа {result.status_code,result.json()}"

    @allure.title("Архивация контрагента,успешный")
    def test_archive_contractor(self):
        contractor2 = ContractorData()
        ContractorsAPI.create_contractor(contractor2)
        response = ContractorsAPI.get_list_contractors()  # Запрашиваем список всех контрагентов, потому что в ответе при создании контрагента приходит пустой json
        result = response.json()  # Через переменную , что бы найти по ID последнего созданного контрагента
        id_entity = result["list"][0]["id"]  # берем в переменную id контрагента
        result = ContractorsAPI.archive_contractor(id_entity)
        assert result.status_code == 200, f"Ошибка , код ответа {result.status_code, result.json()}"

    @allure.title("Удаление контрагента,успешный")
    def test_archive_contractor(self):
        contractor2 = ContractorData()
        ContractorsAPI.create_contractor(contractor2)
        response = ContractorsAPI.get_list_contractors()  # Запрашиваем список всех контрагентов, потому что в ответе при создании контрагента приходит пустой json
        result = response.json()  # Через переменную , что бы найти по ID последнего созданного контрагента
        id_entity = result["list"][0]["id"]  # берем в переменную id контрагента
        result = ContractorsAPI.archive_contractor(id_entity)
        assert result.status_code == 200, f"Ошибка , код ответа {result.status_code, result.json()}"