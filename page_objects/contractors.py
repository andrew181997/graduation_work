import time

import allure

from page_objects.common_entity_lists_elements import EntityListElements
# from utils.bd_controll.base_bd_control import BdControl
# from utils.bd_controll.db_query import query


class Contractors(EntityListElements):
    name_input = "[formcontrolname='name']>div>input"
    name_validation = "[formcontrolname='name']>div>p"
    main_tab = "[aria-posinset='1']"
    contractor_users_tab = "[aria-posinset='2']"
    report_data_tab = "[aria-posinset='3']"
    change_history = ".icon-history"
    "====Кнопки главной страницы создания/редактирования контрагента===="
    phone = "[formcontrolname='phone']"
    street = "[formcontrolname='street']"
    house = "[formcontrolname='house']"
    floor = "[formcontrolname='floor']"
    room = "[formcontrolname='room']"
    city = "[formcontrolname='city']"
    postcode = "[formcontrolname='postcode']"
    country = "[formcontrolname='country']"
    description = "[formcontrolname='description']"
    role_sla_supplier = "[formcontrolname='slaSupplier']"
    role_service_supplier = "[formcontrolname='serviceSupplier']"
    role_customer = "[formcontrolname='customer']"
    auto_publish_reports = "[formcontrolname='autoPublishReport']"
    icon_tag = ".icon-tag"
    role_validation = "[role='alert']"
    "====Кнопки вкладки пользователей страницы создания/редактирования контрагента===="
    add_user_btn = ".entities-list__add"
    create_user_btn = ".entities-list__create-new"
    user_input = "[data-placeholder='pm_party_users_input_placeholder']"
    user_input_close = ".icon-close"
    user_search = ".search>div>input"
    users_names = ".user-row__fullName>span"
    users_roles = ".user-row__roles>span"
    users_other = ".user-row__other>span"
    users_edit = ".user-row__edit>button"
    users_delete = ".entities-list__buttons .icon-delete"
    "====Кнопки страницы отчетов при создания/редактирования контрагента===="
    add_report_logo = ".edit-icon>div"
    report_agreed_name = "[formcontrolname='fullNameAgreed']"
    report_agreed_job = "[formcontrolname='jobTitleAgreed']"
    report_approved_name = "[formcontrolname='fullNameApproved']"
    report_approved_job = "[formcontrolname='jobTitleApproved']"

    def add_user_to_contractor(self, already_at_contractor: bool = False, user: str = None):
        """
        Метод добавления пользователя к контрагенту
        :param already_at_contractor: Прикреплен ли пользователь к контрагенту
        :param user: имя пользователя
        :return:
        """
        self.click(Contractors.add_user_btn)
        # если нет контрагента, просто добавляем
        if not already_at_contractor:
            self.wait_for_element_visible(Contractors.users_names)
            self.type(Contractors.user_input, "user")
            self.wait_for_text("user", Contractors.users_names)
            self.click_nth_visible_element(Contractors.users_names, 0)
        else:
        # если контрагент есть, добавляем и проверяем текст на попапе
            self.wait_for_element_visible(Contractors.users_names)
            self.type(Contractors.user_input, f'"{user}"')
            self.wait(1)
            self.wait_for_element_visible(Contractors.users_names)
            self.attach_report_screenshot()
            self.wait_for_text(text=user, selector=Contractors.users_names)
            self.click_nth_visible_element(Contractors.users_names, 0)
            self.wait_for_element_visible(EntityListElements.page_dialog)
            dialog_massage = self.get_text(EntityListElements.dialog_massage)
            assert dialog_massage == "Выбранный пользователь уже прикреплен к другому контрагенту. Открепить?"

    def create_new_contractor(self, name: str, user=False,
                              sla_supplier: bool = False,
                              service_supplier: bool = False,
                              customer: bool = True,
                              auto_report: bool = True,
                              add_user: bool | int = False,):
        """
        Метод для создания нового контрагента
        :param name: имя контрагента
        :param user: пользователь
        :param sla_supplier: является ли контрагент провайдером SLA
        :param service_supplier: является ли контрагент провайдером сервиса
        :param customer: является ли контрагент потребителем сервиса
        :param auto_report: автоматическая публикация отчетов
        :param add_user: если False - пользователи не будут добавлены, если true - добавит пользователя user.
        если int - используется в случае создания контрагента пользователем без контрагента
        (автоматическое добавление пользователя)
        :return:
        """
        with allure.step("Заполнение формы"):
            self.type(Contractors.name_input, name)
            if sla_supplier:
                self.click(Contractors.role_sla_supplier)
            if service_supplier:
                self.click(Contractors.role_service_supplier)
            if not customer:
                self.click(Contractors.role_customer)
            if not auto_report:
                self.click(Contractors.auto_publish_reports)
            self.attach_report_screenshot()
            if isinstance(add_user, bool) and add_user:
                with allure.step("Заполнение вкладки Пользователи"):
                    self.click(Contractors.contractor_users_tab)
                    self.wait(1)
                    self.add_user_to_contractor()
            elif isinstance(add_user, int) and user:
                with allure.step("Проверяем что пользователь прикрепился к контрагенту"):
                    self.click(Contractors.contractor_users_tab)
                    self.wait(1)
                    self.assert_text(user, Contractors.users_names)
                    self.attach_report_screenshot()
                    return
            self.click(EntityListElements.main_button)

        with allure.step("Созданный контрагент находится в таблице"):
            self.wait(1)
            self.attach_report_screenshot()
            self.wait_for_element_visible(f"//span[text()= '{name}']")
        self.click(f"//span[text()= '{name}']")
        entity_id = self.get_current_url().split("/")[-1]
        return entity_id

    def check_contractor_elements(self, created: bool = False):
        """
        Метод для проверки наличия всех элементов в форме контрагента
        :param created: форма создания или редактирования
        :return:
        """
        with allure.step("Проверка элементов на странице"):

            with allure.step("Проверка вкладки ОСНОВНЫЕ ПАРАМЕТРЫ"):
                self.wait_for_element_visible(self.main_tab)
                if not created:
                    assert self.is_element_visible(self.name_input)
                else:
                    assert self.is_element_visible(self.page_title)
                self.assert_element_not_visible(self.name_validation)
                title_1 = self.get_text(self.main_tab)
                assert title_1 == "ОСНОВНЫЕ ПАРАМЕТРЫ", f"{title_1} != Основные параметры"
                assert self.is_element_visible(self.contractor_users_tab)
                title_2 = self.get_text(self.contractor_users_tab)
                assert title_2 == "ПОЛЬЗОВАТЕЛИ КОНТРАГЕНТА", f"{title_2} != ПОЛЬЗОВАТЕЛИ КОНТРАГЕНТА"
                assert self.is_element_visible(self.report_data_tab)
                title_3 = self.get_text(self.report_data_tab)
                assert title_3 == "ДАННЫЕ ДЛЯ ОТЧЁТОВ", f"{title_3} != ДАННЫЕ ДЛЯ ОТЧЁТОВ"
                assert self.is_element_visible(self.phone)
                assert self.is_element_visible(self.street)
                assert self.is_element_visible(self.house)
                assert self.is_element_visible(self.floor)
                assert self.is_element_visible(self.room)
                assert self.is_element_visible(self.city)
                assert self.is_element_visible(self.postcode)
                assert self.is_element_visible(self.country)
                assert self.is_element_visible(self.description)
                assert self.is_element_visible(self.role_sla_supplier)
                assert self.is_element_visible(self.role_service_supplier)
                assert self.is_element_visible(self.role_customer)
                assert self.is_element_visible(self.auto_publish_reports)
                assert self.is_element_visible(self.icon_tag)
                self.attach_report_screenshot()

            with allure.step("Проверка вкладки Пользователи"):
                self.click(self.contractor_users_tab)
                self.wait(1)
                assert self.is_element_visible(self.add_user_btn)
                assert self.is_element_visible(self.create_user_btn)
                time.sleep(5)
                assert self.is_element_visible(self.user_search)
                if created:
                    self.attach_report_screenshot()
                    assert self.is_element_present(self.users_names)
                    assert self.is_element_visible(self.users_roles)
                    assert self.is_element_visible(self.users_other)
                    assert self.is_element_visible(self.users_edit)
                    assert self.is_element_visible(self.users_delete)


            with allure.step("Проверка вкладки Данные для отчета"):
                self.click(self.report_data_tab)
                self.wait(1)
                assert self.is_element_visible(self.add_report_logo)
                assert self.is_element_visible(self.report_agreed_name)
                assert self.is_element_visible(self.report_agreed_job)
                assert self.is_element_visible(self.report_approved_name)
                assert self.is_element_visible(self.report_approved_job)
                self.attach_report_screenshot()

    def check_contractor_history(self):
        """
        Метод для проверки истории изменения контрагента !! Фиксированный
        :return:
        """
        with allure.step("Переход на страницу истории изменения"):
            self.click("//span[text()='Wellink']")
            party_id = self.get_current_url().split("/")[-1]
            self.click(self.additional_actions_button)
            self.wait_for_element_visible(".sub-menu-item-button")
            self.attach_report_screenshot()
        self.click(self.change_history)
        self.wait_for_element_visible(self.search_input)
        with allure.step("Проверка истории"):
            self.wait_for_element_visible(EntityListElements.table_list_of_visible_rows)
            title = self.get_text(self.page_title)
            assert title == "Журнал событий", f" Заголовок {title} != Журнал событий"
            res = self.get_text(self.search_input)
            self.attach_report_screenshot()
            assert res == f'"party.ID{party_id}"', f'некорректный результат {res} != "user.ID{party_id}"'
            assert len(self.find_elements(self.table_list_of_visible_rows)) == 0

    def check_contractor_validation(self):
        """
        Метод для проверки валидации формы контрагента
        :return:
        """
        with allure.step("Валидация отсутствует на незаполненной форме"):
            self.attach_report_screenshot()
            self.assert_element_absent(Contractors.name_validation)
            self.assert_element_absent(".tab__invalid")
            self.assert_element_not_present(".ng-invalid>mat-checkbox")

        with allure.step("Проверка валидации названия"):
            self.click(Contractors.role_customer)
            self.click(EntityListElements.main_button)
            self.wait_for_element_visible(".tab__invalid")
            self.wait_for_element_visible(Contractors.name_validation)
            self.attach_report_screenshot()
            er = self.get_text(Contractors.name_validation)
            assert er == "введите название контрагента", f"{er} == введите название контрагента"

        with allure.step("Проверка валидации ролей"):
            self.wait_for_element_visible(Contractors.role_validation)
            self.attach_report_screenshot()
            er = self.get_text(Contractors.role_validation)
            assert er == "выберите хотя бы одно значение", f"{er} == выберите хотя бы одно значение"

        with allure.step("Валидация пропадает после заполнения необходимых полей"):
            self.type(Contractors.name_input, "валидация")
            self.assert_element_absent(Contractors.name_validation)
            self.click(Contractors.role_sla_supplier)
            self.attach_report_screenshot()
            self.assert_element_absent(".tab__invalid")
            self.assert_element_not_present(".ng-invalid>mat-checkbox")

        with allure.step("Проверка на уникальность названия"):
            self.type(Contractors.name_input, "Wellink")
            self.click(EntityListElements.main_button)
            self.wait_for_element_visible(Contractors.name_validation)
            self.attach_report_screenshot()
            er = self.get_text(Contractors.name_validation)
            assert er == "объект с таким названием уже существует", (f"{er} == "
                                                                     f"объект с таким названием уже существует")

    def change_contractor_for_operator(self, user, contractor:str = None):
        """
        Метод для изменения контрагента у пользователя
        :param user: пользователь
        :param contractor: контрагент
        :return:
        """
        with allure.step("Добавление пользователя к контрагенту"):
            if contractor:
                self.type(Contractors.name_input, contractor)
            self.click(Contractors.contractor_users_tab)
            self.wait(1)
            self.add_user_to_contractor(already_at_contractor=True, user=user)


class ContractorsFilters(EntityListElements):
    selectors = {
        'filter_panel': ".filter-pane",
        'contractor_single_level_list': ".mat-radio-button:has([value='party_kind_of_list_single_level'])",
        'contractor_tree': ".mat-radio-button:has([value='party_kind_of_list_hierarchical'])",
        'contractor_expend_tree_node': ".mat-tree-node>button",
        'contractor_active': ".mat-checkbox:has([value='ACTIVE'])",
        'contractor_archived': ".mat-checkbox:has([value='ARCHIVED'])",
        'contractor_customer': ".mat-checkbox:has([value='CUSTOMER'])",
        'contractor_service_supplier': ".mat-checkbox:has([value='SERVICE_SUPPLIER'])",
        'contractor_by_tag': "[placeholder='Найти по тегам']",
        'contractor_drop_filters': ".filter-pane-template__clear button",
        'contractor_parent_tree_node': "mat-tree>mat-nested-tree-node",
        'contractor_tree_node': "[role='group']>mat-tree-node",
    }

    # def check_filters(self):
    #     with allure.step("Проверка видимости всех необходимых фильтров"):
    #         for name, sel in ContractorsFilters.selectors.items():
    #             self.wait_for_element_visible(ContractorsFilters.selectors.get("filter_panel"))
    #             if name not in ('contractor_drop_filters', 'contractor_expend_tree_node',
    #                             'contractor_parent_tree_node', 'contractor_tree_node'):
    #                 self.scroll_into_view(sel)
    #                 assert self.is_element_visible(selector=sel), f"Элемент {name} не найден"
    #
    # def check_contractors_filters(self):
    #     with allure.step("Проверка видимости фильтров"):
    #         self.check_filters()
    #
    #     with allure.step("Проверка фильтрации по роли ПОТРЕБИТЕЛЬ СЕРВИСА"):
    #         self.click(ContractorsFilters.selectors.get("contractor_customer"))
    #         self.wait_for_spinner_absence()
    #         self.wait(2)
    #         self.attach_report_screenshot()
    #         self.check_entity_visible_count(expected_result=BdControl.execute(query.count_customers_contractors)[0][0])
    #
    #         self.click(ContractorsFilters.selectors.get("contractor_customer"))
    #         self.wait_for_spinner_absence()
    #
    #     with allure.step("Проверка фильтрации по роли ПРОВАЙДЕР СЕРВИСА"):
    #         self.click(ContractorsFilters.selectors.get("contractor_service_supplier"))
    #         self.wait_for_spinner_absence()
    #         self.wait(2)
    #         self.attach_report_screenshot()
    #         self.check_entity_visible_count(expected_result=BdControl.execute(query.count_service_suppliers_contractors)[0][0])
    #
    #         self.click(ContractorsFilters.selectors.get("contractor_service_supplier"))
    #         self.wait_for_spinner_absence()
    #
    #     with allure.step("Проверка фильтрации по статусу АКТИВНЫЙ"):
    #         self.click(ContractorsFilters.selectors.get("contractor_active"))
    #         self.wait_for_spinner_absence()
    #         self.wait(2)
    #         self.attach_report_screenshot()
    #         self.check_entity_visible_count(expected_result=BdControl.execute(query.count_active_contractors)[0][0])
    #
    #         self.click(ContractorsFilters.selectors.get("contractor_active"))
    #         self.wait_for_spinner_absence()
    #
    #     with allure.step("Проверка смешанной фильтрации"):
    #         self.click(ContractorsFilters.selectors.get("contractor_active"))
    #         self.click(ContractorsFilters.selectors.get("contractor_customer"))
    #         self.click(ContractorsFilters.selectors.get("contractor_service_supplier"))
    #         self.click(ContractorsFilters.selectors.get("contractor_archived"))
    #         self.wait_for_spinner_absence()
    #         self.wait(2)
    #         self.attach_report_screenshot()
    #         self.check_entity_visible_count(expected_result=BdControl.execute(query.count_combine_contractors)[0][0])
    #
    #     with allure.step("Проверка кнопки сброса фильтров"):
    #         self.click(ContractorsFilters.selectors.get("contractor_drop_filters"))
    #         self.wait_for_spinner_absence()
    #         for name, sel in ContractorsFilters.selectors.items():
    #             if name not in ("filter_panel", "contractor_drop_filters", "contractor_tree_node", 'contractor_by_tag',
    #                             "contractor_single_level_list", "contractor_tree",
    #                             "contractor_expend_tree_node", "contractor_parent_tree_node"):
    #                 self.assert_attribute(selector=sel + ">label>span>input",
    #                                       attribute="aria-checked", value="false")
    #
    # def check_hierarchy(self):
    #     with allure.step("Включение иерархического режима"):
    #         self.click(ContractorsFilters.selectors.get("contractor_tree"))
    #         self.wait_for_spinner_absence()
    #         self.wait_for_element_visible(".cdk-tree-node .mat-row")
    #         self.attach_report_screenshot()
    #         assert self.is_element_visible(ContractorsFilters.selectors.get("contractor_expend_tree_node"))
    #
    #     with allure.step("Проверка нод в дереве"):
    #         nodes = len(self.find_elements(ContractorsFilters.selectors.get("contractor_parent_tree_node")))
    #         assert nodes == BdControl.execute(query.count_party_hierarchy_root_nodes)[0][0], (f"Неверное "
    #                                                                                           f"количество корневых нод "
    #                                                                                           f"{nodes} != 2")
    #         self.click(ContractorsFilters.selectors.get("contractor_expend_tree_node"))
    #         tree_size = len(self.find_elements(ContractorsFilters.selectors.get("contractor_tree_node")))
    #         self.attach_report_screenshot()
    #         assert tree_size == BdControl.execute(query.count_party_hierarchy_child_nodes)[0][0], (f"Неверное "
    #                                                                                                f"количество дочерних "
    #                                                                                                f"нод {tree_size} != 4")

    def select_all(self):
        for name, sel in ContractorsFilters.selectors.items():
            self.wait_for_element_visible(ContractorsFilters.selectors.get("filter_panel"))
            if name not in ('contractor_drop_filters', 'contractor_expend_tree_node',
                            'contractor_parent_tree_node', 'contractor_tree_node', 'contractor_by_tag'):
                self.click(sel)


    def archive_contact_for_tests(self, contractor_name):
        """Архивирования контрагента"""
        self.go_to_contractors()
        self.type(EntityListElements.search_input, f'"{contractor_name}"')
        self.wait_for_spinner_absence()
        self.click_nth_visible_element(".mat-row>mat-cell>div>mat-checkbox", 0)
        self.click(EntityListElements.entity_action_first_button)
        self.wait_for_element_clickable(EntityListElements.filers_button)

        with allure.step("Переход к фильтрам, выбор Архивных контрагентов"):
            self.click(EntityListElements.filers_button)
            self.click("[title='Архивный']")



    def delete_contact_for_tests(self, contractor_name):
        """Удаления контрагента."""
        with allure.step("Выбор архивной записи для удаления"):
            self.type(EntityListElements.search_input, contractor_name)
            self.wait(2)
            self.wait_for_text(contractor_name, ".party-main-column>span")
            self.click_nth_visible_element(".mat-row>mat-cell>div>mat-checkbox", 0)
            if self.is_element_visible(".actions-row__toggle_btn"):
                self.click(".actions-row__toggle_btn")
            self.click(".icon-delete")
            self.attach_report_screenshot()

        with allure.step("Подтверждение удаления"):
            self.click_nth_visible_element(".mat-dialog-actions>button", 0)