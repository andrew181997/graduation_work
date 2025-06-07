import allure
from api.module.contractors import ContractorData
from api.api_contractors_methods import ContractorsAPI
import uuid
from utils import ENV
import pytest


class TestContractorsApi:

    @pytest.fixture()
    def party_data(self):
        """Генерация тестовых данных PartyData с уникальным именем"""
        random_name = f"test_party_{uuid.uuid4().hex[:8]}"  # Генерация уникального имени

        return ContractorData(
            name=random_name,
            editByOwnerOnly =0,
            partyRoles =["SLA_SUPPLIER","SERVICE_SUPPLIER","CUSTOMER"],
            status = "ACTIVE",
            addressDto={},
            partyReport={},
            users=[{"id": 36951, "name": "b@b.ru"}],
            slaSupplier=0,
            serviceSupplier=1,
            customer=1,
            active =0,
            autoPublishReport = 1,
            hasRestrictions =0,
            roles = {"slaSupplier":1,"serviceSupplier":1,"customer":1},
            phone = ""
        )


    @allure.title("Создание контрагента рутом")
    def test_create_contractor(self,party_data):
        result = ContractorsAPI.create_contractor(party_data, ENV.ROOT_NAME, ENV.ROOT_PASS)
        assert result.status_code == 200, f"Ошибка, кода ответа {result.status_code}"


    @allure.title("Создание контрагента оператором")
    def test_create_contractor(self,party_data):
        result = ContractorsAPI.create_contractor(party_data, ENV.OPERATOR_NAME, ENV.OPERATOR_PASS)
        assert result.status_code == 200, f"Ошибка, кода ответа {result.status_code}"

    @allure.title("Просмотр списка контрагентов")
    def test_get_contractors(self):
        result = ContractorsAPI.get_list_contractors()
        assert result.status_code == 200, f"Ошибка , код ответа {result.status_code,result.json()}"
        assert result.json() is not None

    @pytest.fixture()
    def create_contractor(self,party_data):
        response = ContractorsAPI.create_contractor(party_data, ENV.ROOT_NAME, ENV.ROOT_PASS)
        yield response

    @allure.title("Архивация контрагента,тест специально будет падать с 500 ошибкой")
    def test_archive_contractor(self,create_contractor):
        response = ContractorsAPI.get_list_contractors() # Запрашиваем список всех контрагентов, потому что в ответе при создании контрагента приходит пустой json
        result = response.json() # Через переменную , что бы найти по ID последнего созданного контрагента
        id_entity = result["list"][0]["id"] # берем в переменную id контрагента
        result = ContractorsAPI.archive_contractor(id_entity)
        assert result.status_code == 200, f"Ошибка , код ответа {result.status_code,result.json()}"



