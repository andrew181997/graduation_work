import allure
from page_objects.side_menu import Menu


class EntityListElements(Menu):
    main_button = ".mat-focus-indicator.mat-flat-button.mat-button-base.main-button"
    data_channel = "(//wi-button-item[@class='sub-button-item'])[1]"
    additional_actions_button = ".toolbar-buttons__more-btn"
    filers_button = ".toolbar-filter>button"
    search_input = ".base-toolbar__search>wi-toolbar-search>div>div>input"
    search_field = ".mat-autocomplete-trigger"
    search_help = "button.icon-help_outline"
    search_criteria_expand_button = "button.mat-menu-trigger:nth-child(2)"
    dialog_actions = ".mat-dialog-actions>button"
    entity_name = ".main-column-row>span"
    "====period select===="
    period_hour = "wi-select-period [value='hour'] button"
    period_day = "wi-select-period [value='day'] button"
    period_week = "wi-select-period [value='week'] button"
    period_month = "wi-select-period [value='month'] button"
    period_all = "wi-select-period [value='all'] button"
    period_custom = "wi-select-period [value='custom'] button"
    "====entity actions===="
    to_archive = "icon-archive"
    entity_action_first_button = "div.actions-button__wrapper:nth-child(1)>button"
    entity_action_first_button_arh = "div.actions-button__wrapper:nth-child(1)>button>span"
    entity_action_four_button = "div.actions - button__wrapper: nth - child(4) > button"
    entity_action_second_button = "div.actions-button__wrapper:nth-child(2)>button"
    entity_action_third_button = "div.actions-button__wrapper:nth-child(3)>button"
    entity_action_more_actions_button: str = "button.mat-focus-indicator:nth-child(4)"
    more_actions = ".icon-more_vert"
    table_columns_button = ".table-properties__toggle_btn"

    table_master_checkbox = (".mat-header-cell.mat-header-cell:"
                             "nth-child(1)>div>mat-checkbox>label")

    list_entity_names = ".mat-row>mat-cell>div.main-column-row>span.text-overflow"
    table_list_of_visible_rows = ".mat-row.mat-row"
    pagination_count = ".mat-paginator-range-actions>div"
    dynamic_chart = ".spinner-container-apx-chart>div"
    autocomplite_suggestions = "[role='listbox']"
    search_results = ".mat-option.mat-option"
    search_results_text = "mat-option .mat-option-text"
    search_results_name = "mat-option .mat-option-text .entity-row__name"
    tooltip = "mat-tooltip-component>div"
    notification = "wi-portal-notification"
    notification_entity_name = notification + " .details__entity-name"

    def entity_list_table_size_all(self):
        """
        Метод получения текста пагинации на странице списка сущностей
        :return: None
        """
        return self.get_text(self.pagination_count)

    def check_entity_visible_count(self, expected_result):
        """
        Проверка количества записей в таблице
        :param expected_result: ожидаемое количество записей
        """
        self.scroll_into_view(".mat-paginator-range-actions>div")
        result = int(self.entity_list_table_size_all().split()[-1])
        with allure.step("Проверяем общее количество сущностей в таблице, сверяем со значением в БД"):
            assert result == expected_result, (f'Некорректный результат: '
                                               f'на станице -> {result=} != в БД -> {expected_result=}')

    def parse_search_results(self):
        results = list(map(lambda x: x.text, self.find_elements(EntityListElements.search_results)))
        return results

    @allure.title("Проверка заголовка страницы")
    def check_page_title(self, expected_result: str):
        """
        Метод для проверки заголовка страницы
        :param expected_result: str - Ожидаемый заголовок
        :return: сравнивает текущий заголовок с переданным в expected_result
        """
        with allure.step("Проверка заголовка страницы"):
            self.wait_for_text(expected_result, EntityListElements.page_title)
            result = self.get_text(self.page_title)
            assert result == expected_result, (f'Некорректный результат {result=} != '
                                               f'{expected_result=}')

    @allure.title("Проверка главной кнопки на странице")
    def check_main_button(self, expected_result: str):
        """
        Проверка главной кнопки на странице
        :param expected_result: текст на главной кнопке
        :return:
        """
        with allure.step("Проверка главной кнопки страницы 'СОЗДАТЬ СЕРВИС'"):
            result = self.get_text(self.main_button)
            assert result == expected_result.upper(), (f'Некорректный результат {result=} != '
                                                       f'{expected_result=}')
            assert self.is_element_clickable(self.main_button), "Кнопка не кликабельна"

    def check_page_header(self, filters: bool = False):
        if filters:
            with allure.step("Проверка кнопки фильтров"):
                assert self.is_element_visible(self.filers_button), "Кнопка фильтрации отсутствует на странице"
        with allure.step("Проверка поля поиска"):
            assert self.is_element_visible(self.search_field), "Компонент поиска отсутствует на странице"

    def check_page_extra_actions(self):
        """
        Проверка кнопки дополнительных действий на странице
        """
        with allure.step("Проверка кнопки дополнительных действий на странице"):
            assert self.is_element_visible(self.additional_actions_button)

    def check_table_elements_visible(self):
        """
        Проверка наличия таблицы сущностей на странице
        """
        with allure.step("проверка видимости таблицы сущностей"):
            self.wait_for_element_present(self.table_list_of_visible_rows)
            assert self.is_element_visible(self.table_list_of_visible_rows), ("Таблица сущностей"
                                                                              " не появилась или пуста")

    def check_page(self, title: str,
                   count=None,
                   main_button_text: str = None,
                   period_select: bool = False,
                   filters: bool = True):
        """
        Общий метод проверки элементов на страницах сущностей
        :param title: ожидаемый заголовок страницы
        :param count: результат запроса в бд
        :param main_button_text: ожидаемый текст основной кнопки на странице
        :param period_select: есть ли на странице компонент выбора периода
        :param filters: есть ли на странице компонент фильтрации
        :return: None
        """
        self.check_page_title(expected_result=title)
        self.check_page_header(filters)
        if main_button_text:
            self.check_main_button(expected_result=main_button_text)
        if period_select:
            self.click(self.period_all)
            self.wait(1)
            self.wait_for_spinner_absence()
        if count:
            bd_count = count[0][0]
            if bd_count != 0:
                self.check_table_elements_visible()
            self.check_entity_visible_count(expected_result=bd_count)

    def check_statuses(self, entities: list, status):
        for row in range(2, len(entities)+2):
            current_status = self.get_attribute(f"mat-row:nth-child({row}) .table-icon", "class")
            match status:
                case "ACTIVE":
                    assert "icon-check_circle" in current_status
                case "NOT ACTIVE":
                    assert "icon-not_used" in current_status
                case "NO DATA":
                    assert "icon-grey" in current_status
                case _:
                    raise ValueError("Доступны только ACTIVE, NOT ACTIVE и NO DATA")