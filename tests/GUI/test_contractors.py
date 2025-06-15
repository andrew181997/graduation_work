import time
import allure
import pytest
import uuid
from api.module.contractors import ContractorData
from api.api_methods import HttpMethods
from api.api_contractors_methods import ContractorsAPI
from page_objects.contractors import Contractors, ContractorsFilters
from page_objects.common_entity_lists_elements import EntityListElements




@pytest.mark.acceptance
@pytest.mark.xdist_group("group_contractor")
class TestContractorPage(Contractors, ContractorsFilters):
    name = f"NEW_CONTRACTOR_{uuid.uuid4().hex[:8]}"

    @allure.title("Создание нового контрагента")
    def test_create_new_contractor(self):
        self.login_as_root()
        self.go_to_contractors()
        self.wait_for_spinner_absence()
        self.click(EntityListElements.main_button)
        self.wait_for_spinner_absence()
        entity_id = Contractors.create_new_contractor(self, name=TestContractorPage.name, add_user=True)
        self.click(Contractors.contractor_users_tab)
        self.click(Contractors.users_delete)
        self.wait_for_element_visible(EntityListElements.dialog_actions)
        self.click_nth_visible_element(EntityListElements.dialog_actions, 1)
        self.wait_for_element_clickable(EntityListElements.main_button)
        self.click(EntityListElements.main_button)
        self.wait_for_element_visible(f"//span[contains(text(), '{TestContractorPage.name}')]")

        with allure.step("Aрхивация тестовых данных через API"):
            r = HttpMethods.attach_response_data(ContractorsAPI.archive_contractor(entity_id))
            assert r.status_code == 200, "Контрагент не был архивирован"

        with allure.step("Удаление тестовых данных через API"):
            r = HttpMethods.attach_response_data(ContractorsAPI.delete_contractor(entity_id))
            allure.attach(f"Request:{r.request.url}\nSTATUS:{r.status_code}")
            assert r.status_code == 200, "Контрагент не был  удален"



    @allure.title("Проверка элементов созданного контрагента")
    def test_created_contractor_elements(self):
        self.login_as_root()
        self.go_to_contractors()
        self.wait_for_spinner_absence()
        self.type(EntityListElements.search_input, "Wellink")
        self.wait_for_spinner_absence()
        self.click("//div[@class = 'party-main-column ng-star-inserted']/span[text()='Wellink']")
        self.wait_for_spinner_absence()
        self.check_contractor_elements(created=True)



    @allure.title("Проверка элементов нового контрагента")
    def test_new_contractor_elements(self):
        self.login_as_root()
        self.go_to_contractors()
        self.wait_for_spinner_absence()
        self.click(EntityListElements.main_button)
        self.wait_for_spinner_absence()
        self.check_contractor_elements(created=False)



    @allure.title("Архивация контрагента")
    def test_archive_contractor(self):
        contractor = ContractorData()
        contractor_name = contractor.name
        with allure.step("Создание контрагента через API"):
            r = HttpMethods.attach_response_data(ContractorsAPI.create_contractor(contractor))
            assert r.status_code == 200, f"Контрагент не был создан {r.json()}"
        self.login_as_root()
        self.go_to_contractors()
        self.type(EntityListElements.search_input, f'"{contractor_name}"')
        self.wait_for_spinner_absence()
        self.click(f"//span[text()= '{contractor_name}']")
        entity_id = self.get_current_url().split("/")[-1]
        self.click(EntityListElements.backwards_button)
        self.wait_for_spinner_absence()
        self.click_nth_visible_element(".mat-row>mat-cell>div>mat-checkbox", 0)
        self.click(EntityListElements.entity_action_first_button)
        self.wait_for_element_clickable(self.filers_button)

        with allure.step("Переход к фильтрам, выбор Архивных контрагентов"):
            self.click(self.filers_button)
            self.click("[title='Архивный']")
            self.wait_for_text("1 - 1 из 1", EntityListElements.pagination_count)
            self.attach_report_screenshot()

        with allure.step("Проверка созданного контрагента в архиве"):
            archive_name = self.find_elements(".party-main-column__name")[0]
            self.attach_report_screenshot()
            assert archive_name.text == contractor_name

        with allure.step("Удаление тестовых данных через API"):
            r = HttpMethods.attach_response_data(ContractorsAPI.delete_contractor(entity_id))
            assert r.status_code == 200, "Контрагент не был  удален"


    @allure.title("Удаление архивного контрагента")
    def test_delete_contractor(self):
        contractor = ContractorData()
        contractor_name = contractor.name
        self.login_as_root()

        with allure.step("Создание контрагента через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.create_contractor(contractor))
            allure.attach(f"Request URL: {response.request.url}\nResponse Status: {response.status_code}")
            assert response.status_code == 200, f"Контрагент не был создан: {response.json()}"
            self.go_to_contractors()

            # Получение идентификатора созданного контрагента
            self.click(f"//span[text()= '{contractor_name}']")
            entity_id = self.get_current_url().split("/")[-1]
            self.click(EntityListElements.backwards_button)
            self.wait_for_spinner_absence()

        with allure.step("Архивация тестовых данных через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.archive_contractor(entity_id))
            allure.attach(f"Request URL: {response.request.url}\nResponse Status: {response.status_code}")
            assert response.status_code == 200, "Контрагент не был архивирован"

        with allure.step("Переход к фильтрам и выбор архивных записей"):
            self.click(self.filers_button)
            self.click(ContractorsFilters.selectors.get("contractor_archived"))
            self.wait_for_spinner_absence()

        with allure.step("Выбор архивной записи для удаления"):
            self.type(EntityListElements.search_input, contractor_name)
            self.wait_for_text(contractor_name, ".party-main-column>span")
            self.click_nth_visible_element(".mat-row>mat-cell>div>mat-checkbox", 0)
            self.wait(1)
            if self.is_element_visible(".actions-row__toggle_btn"):
                self.click(".actions-row__toggle_btn")
            self.click(".icon-delete")
            self.attach_report_screenshot()

        with allure.step("Подтверждение удаления"):
            self.click_nth_visible_element(".mat-dialog-actions>button", 0)

        with allure.step("Проверка отсутствия записи в таблице"):
            self.wait_for_text_not_visible(contractor_name)


    @allure.title("Проверка валидации при сохранении контрагента")
    def test_contractor_validation(self):
        self.login_as_root()
        self.go_to_contractors()
        self.click(EntityListElements.main_button)
        self.wait_for_element_visible(Contractors.name_input)
        self.check_contractor_validation()




    @allure.title("Восстановление из архива контрагента")
    def test_contractor_restore(self):
        contractor = ContractorData()
        contractor_name = contractor.name
        self.login_as_root()

        with allure.step("Создание контрагента через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.create_contractor(contractor))
            allure.attach(f"Request URL: {response.request.url}\nResponse Status: {response.status_code}")
            assert response.status_code == 200, f"Контрагент не был создан: {response.json()}"
            self.go_to_contractors()
            self.type(EntityListElements.search_input, f'"{contractor_name}"')
            self.wait_for_spinner_absence()
            self.click(f"//span[text()= '{contractor_name}']")
            entity_id = self.get_current_url().split("/")[-1]
            self.click(EntityListElements.backwards_button)

        with allure.step("Архивация контрагента через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.archive_contractor(entity_id))
            allure.attach(f"Request URL: {response.request.url}\nResponse Status: {response.status_code}")
            assert response.status_code == 200, "Контрагент не был архивирован"

        with allure.step("Переход к фильтрам и выбор архивных записей"):
            self.click(self.filers_button)
            self.click(ContractorsFilters.selectors.get("contractor_archived"))
            self.wait_for_spinner_absence()

        with allure.step("Восстановление контрагента"):
            self.type(EntityListElements.search_input, contractor_name)
            self.wait_for_text(contractor_name, ".party-main-column>span")
            self.click_nth_visible_element(".mat-row>mat-cell>div>mat-checkbox", 0)
            self.wait(1)
            if self.is_element_visible(".actions-row__toggle_btn"):
                self.click(".actions-row__toggle_btn")
            self.click(".icon-refresh")
            self.attach_report_screenshot()

        with allure.step("Проверка восстановления контрагента"):
            self.click(ContractorsFilters.selectors.get("contractor_archived"))
            self.click(ContractorsFilters.selectors.get("contractor_active"))
            self.wait_for_spinner_absence()
            self.attach_report_screenshot()
            self.wait_for_text(contractor_name, ".party-main-column>span")

        with allure.step("Aрхивация тестовых данных через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.archive_contractor(entity_id))
            allure.attach(f"Request URL: {response.request.url}\nResponse Status: {response.status_code}")
            assert response.status_code == 200, "Контрагент не был архивирован перед удалением"

            response = HttpMethods.attach_response_data(ContractorsAPI.delete_contractor(entity_id))
            allure.attach(f"Request URL: {response.request.url}\nResponse Status: {response.status_code}")
            assert response.status_code == 200, "Контрагент не был удален"



    @allure.title("Уход со страницы без изменений")
    def test_leave_page_without_change(self):
        contractor = ContractorData()
        contractor_name = contractor.name
        self.login_as_root()

        with allure.step("Создание контрагента через API"):
            r = HttpMethods.attach_response_data(ContractorsAPI.create_contractor(contractor))
            allure.attach(f"Request:{r.request.url}\nSTATUS:{r.status_code}")
            assert r.status_code == 200, f"Контрагент не был создан {r.json()}"
            self.go_to_contractors()

        with allure.step("Переход к контрагенту, уход со страницы без изменений"):
            self.click(f"//span[text()= '{contractor_name}']")
            entity_id = self.get_current_url().split("/")[-1]
            self.click(EntityListElements.backwards_button)
            self.assert_element_absent(EntityListElements.dialog_actions)

        with allure.step("Aрхивация тестовых данных через API"):
            r = HttpMethods.attach_response_data(ContractorsAPI.archive_contractor(entity_id))
            allure.attach(f"Request:{r.request.url}\nSTATUS:{r.status_code}")
            assert r.status_code == 200, "Контрагент не был архивирован"

        with allure.step("Удаление тестовых данных через API"):
            r = HttpMethods.attach_response_data(ContractorsAPI.delete_contractor(entity_id))
            allure.attach(f"Request:{r.request.url}\nSTATUS:{r.status_code}")
            assert r.status_code == 200, "Контрагент не был  удален"



    @allure.title("Уход со страницы с изменениями")
    def test_leave_page_with_change(self):
        contractor = ContractorData()
        contractor_name = contractor.name
        self.login_as_root()

        with allure.step("Создание контрагента через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.create_contractor(contractor))
            assert response.status_code == 200, f"Контрагент не был создан: {response.json()}"
            self.go_to_contractors()

        with allure.step("Переход к контрагенту, уход со страницы с изменениями"):
            self.click(f"//span[text()= '{contractor_name}']")
            entity_id = self.get_current_url().split("/")[-1]
            self.click(Contractors.role_sla_supplier)

            # Уход со страницы и проверка диалогового окна
            self.click(EntityListElements.backwards_button)
            self.assert_element_visible(EntityListElements.dialog_actions)
            dialog_text = self.get_text(EntityListElements.dialog_massage)
            assert dialog_text == "Хотите сохранить изменения?", \
                f"Ожидалось сообщение 'Хотите сохранить изменения?', получено: {dialog_text}"

            # Отмена изменений
            self.click_nth_visible_element(EntityListElements.dialog_actions, 1)
            self.wait_for_text("Контрагенты", EntityListElements.page_title)
            self.wait_for_element_visible(EntityListElements.table_list_of_visible_rows)

            # Проверка сохранения изменений
            self.click(f"//span[text()= '{contractor_name}']")
            is_checked = self.get_attribute(Contractors.role_sla_supplier + ">label>span>input", "aria-checked")
            self.attach_report_screenshot()
            assert is_checked == 'true', "Изменение не было сохранено после ухода со страницы"

        with allure.step("Архивация тестовых данных через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.archive_contractor(entity_id))
            assert response.status_code == 200, "Контрагент не был архивирован"

        with allure.step("Удаление тестовых данных через API"):
            response = HttpMethods.attach_response_data(ContractorsAPI.delete_contractor(entity_id))
            assert response.status_code == 200, "Контрагент не был удален"



