from page_objects.login_page import LoginPage


class Menu(LoginPage):

    analytics = "[href='#/op/analytics']"
    map = "[href='#/op/services-map']"
    events = "[href='#/op/events/management']"
    topology = "[href='#/op/network-topology']"
    reports_title = ".menu__items > div:nth-child(6)>wi-menu-item>div"
    sla_reports = "[href='#/op/slm/sla/reports']"
    services = "[href='#/op/slm/services/management']"
    contracts = "[href='#/op/slm/contracts/management']"
    probes = "[href='#/op/im/probes/management']"
    access_points = "[href='#/op/im/saps/management']"
    tests = "[href='#/op/pfm/tests/management']"
    metrics = "[href='#/op/slm/sla/metrics-constructor']"
    sla = "[href='#/op/slm/sla/management']"
    log_out_button = ".user-menu__logout>button"
    user_container = "[href^='#/op/pm/users/management/edit']"
    contractors = "[href='#/op/pm/parties/management']"
    users = "[href='#/op/pm/users/management']"
    sessions = "[href='#/op/pm/sessions/management']"
    audit = "[href='#/op/audit']"
    theme_button = ".theme-button"
    manuals_button = "wi-manual-download button"
    change_lang = ".lang-icon"
    page_title = ".toolbar-name>div"
    filter_icon = ".toolbar-filter > button"
    backwards_button = '//div[@class="base-toolbar__back ng-star-inserted"]//button'
    page_dialog = "[role='dialog']"
    dialog_massage = ".mat-dialog-content"
    page_spinner = ".mat-progress-spinner>svg"
    active_filters = ".mat-badge-active"
    filter_checkbox = ".filter-items__item>mat-checkbox"
    progress_bar = "mat-progress-bar.mat-progress-bar"
    manual_menu = "[role='menuitem']"

    def wait_for_spinner_absence(self, timeout: int = 20):
        """
        Метод для ожидания отсутствия спинеров на странице
        :param timeout: Настраиваемый таймиаут для ожидания
        :return:
        """
        self.wait_for_element_not_visible(selector=self.page_spinner, timeout=timeout)
        self.wait_for_element_not_visible(selector=self.progress_bar, timeout=timeout)

    def go_to_analytics(self):
        """
        Метод для перехода в раздел Аналитика
        :return:
        """
        self.wait_for_element_visible(self.analytics)
        self.click(self.analytics)
        self.wait_for_spinner_absence()

    def go_to_service_map(self):
        """
        Метод для перехода в раздел Карта сервисов
        :return:
        """
        self.wait_for_element_visible(self.map)
        self.click(self.map)
        self.wait_for_spinner_absence()

    def go_to_events(self):
        """
        Метод для перехода в раздел События
        :return:
        """
        self.wait_for_element_visible(self.events)
        self.click(self.events)
        self.wait_for_spinner_absence()

    def go_to_topology(self):
        """
        Метод для перехода в раздел Топология
        :return:
        """
        self.wait_for_element_visible(self.topology)
        self.click(self.topology)
        self.wait_for_spinner_absence()

    def go_to_reports(self):
        """
        Метод для перехода в раздел Отчеты SLA
        :return:
        """
        self.wait_for_element_visible(self.sla_reports)
        self.click(self.sla_reports)
        self.wait_for_spinner_absence()

    def go_to_services(self):
        """
        Метод для перехода в раздел Сервисы
        :return:
        """
        self.wait_for_element_visible(self.services)
        self.click(self.services)
        self.wait_for_spinner_absence()

    def go_to_contracts(self):
        """
        Метод для перехода в раздел Контрагенты
        :return:
        """
        self.wait_for_element_visible(self.contracts)
        self.click(self.contracts)
        self.wait_for_spinner_absence()

    def go_to_probes(self):
        """
        Метод для перехода в раздел Зонды
        :return:
        """
        self.wait_for_element_visible(self.probes)
        self.click(self.probes)
        self.wait_for_spinner_absence()

    def go_to_access_points(self):
        """
        Метод для перехода в раздел Точки доступа
        :return:
        """
        self.wait_for_element_visible(self.access_points)
        self.click(self.access_points)
        self.wait_for_spinner_absence()

    def go_to_tests(self):
        """
        Метод для перехода в раздел Тесты
        :return:
        """
        self.wait_for_element_visible(self.tests)
        self.click(self.tests)
        self.wait_for_spinner_absence()

    def go_to_metrics(self):
        self.wait_for_element_visible(self.metrics)
        self.click(self.metrics)
        self.wait_for_spinner_absence()

    def go_to_sla(self):
        self.wait_for_element_visible(self.sla)
        self.click(self.sla)
        self.wait_for_spinner_absence()

    def go_to_contractors(self):
        self.wait_for_element_visible(self.contractors)
        self.click(self.contractors)
        self.wait_for_spinner_absence()

    def go_to_users(self):
        self.wait_for_element_visible(self.users)
        self.click(self.users)
        self.wait_for_spinner_absence()

    def go_to_sessions(self):
        self.wait_for_element_visible(self.sessions)
        self.click(self.sessions)
        self.wait_for_spinner_absence()

    def go_to_audit(self):
        self.wait_for_element_visible(self.audit)
        self.click(self.audit)
        self.wait_for_spinner_absence()

    def select_first_2_filters(self):
        self.click(self.filter_icon)
        self.click_nth_visible_element(".filter-items__item>mat-checkbox", 1)
        self.click_nth_visible_element(".filter-items__item>mat-checkbox", 2)
        self.wait_for_spinner_absence()