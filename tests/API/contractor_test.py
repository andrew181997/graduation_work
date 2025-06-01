import pytest
import allure
from dataclasses import replace,asdict
import ENV
from api.api_methods import HttpMethods
from api.login_methods import LoginApi
from api.module.contractors import ContractorData
from api.contractors_method import ContractorsAPI
import copy
import uuid
import ENV

import pytest
from datetime import datetime
from dataclasses import field
from typing import List, Dict, Optional

@pytest.fixture()
def party_data():
    """Генерация тестовых данных PartyData с уникальным именем"""
    random_name = f"test_party_{uuid.uuid4().hex[:8]}"  # Генерация уникального имени

    return ContractorData(
        name=random_name,
        tags=[],
        customFields = [],
        editByOwnerOnly =0,
        partyRoles =["SLA_SUPPLIER","SERVICE_SUPPLIER","CUSTOMER"],
        status = "ACTIVE",
        addressDto={},
        partyReport={},
        users=[],
        slaSupplier=0,
        serviceSupplier=1,
        customer=1,
        active =0,
        autoPublishReport = 1,
        hasRestrictions =0,
        roles = {"slaSupplier":1,"serviceSupplier":1,"customer":1},
        phone = ""
    )

# def test_create_contracor():
#     headers =LoginApi.get_token(ENV.ROOT_NAME,ENV.ROOT_PASS)
#     data = {"tags":[],"customFields":[],"editByOwnerOnly":0,"name":"dcsd1","partyRoles":["CUSTOMER"],"status":"ACTIVE","phone":"","addressDto":{},"users":[],"slaSupplier":0,"serviceSupplier":0,"customer":0,"active":0,"autoPublishReport":1,"hasRestrictions":0,"roles":{"customer":1},"partyReport":{"fullNameAgreed":"","jobTitleAgreed":"","fullNameApproved":"","jobTitleApproved":""}}
#     result = HttpMethods.post(url=ENV.WISLA_URL+"/engine/api/v1/parties/save",body=data,header=headers)
#     print(result.status_code)
@allure.title("Создание контрагента рутом")
def test_create_contractor(party_data):
    result = ContractorsAPI.create_contractor(party_data,ENV.ROOT_NAME,ENV.ROOT_PASS)
    assert result.status_code == 200, f"Ошибка, кода ответа {result.status_code}"


@allure.title("Создание контрагента оператором")
def test_create_contractor(party_data):
    result = ContractorsAPI.create_contractor(party_data,ENV.OPERATOR_NAME,ENV.OPERATOR_PASS)
    assert result.status_code == 200, f"Ошибка, кода ответа {result.status_code}"

@allure.title("Просмотр списка контрагентов")
def test_get_contractors():
    result = ContractorsAPI.get_list_contractors()
    assert result.status_code == 200, f"Ошибка , код ответа"
    assert result.json() is not None