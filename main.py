import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    click_call_taxi = (By.XPATH, '//button[normalize-space(text())="Pedir un taxi"]')

    comfort_tariff_button = (By.ID, "tariff-card-4")

    phone_button = (By.CSS_SELECTOR, ".np-button")
    phone_input = (By.ID, 'phone')
    next_step_number = (By.XPATH, "//button[text()='Siguiente']")
    confirm_number = (By.XPATH, "//button[text()='Confirmar']")

    payment_method_button = (By.CSS_SELECTOR, ".pp-button.filled")
    add_card_button = (By.CSS_SELECTOR, ".pp-row.disabled")

    card_number_input = (By.ID, 'number')
    card_code_input = (By.ID, 'code')
    add_payment_card_button = (By.CSS_SELECTOR, "button[type='submit'].button.full")


    close_payment_modal_button = (By.CSS_SELECTOR, 'button.close-button.section-close')

    driver_message = (By.ID, 'comment')

    blanket_and_tissues_checkbox = (By.XPATH, '//div[div[text()="Manta y pañuelos"]]//input[contains(@class,"switch-input")]')

    ice_cream_plus_button = (By.XPATH, '//div[div[normalize-space(text())="Helado"]]//div[contains(@class,"counter-plus")]')

    order_taxi = (By.XPATH, '//div[@class="order"]//div[text()="Buscar automóvil"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def set_from(self, from_address):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def set_order_taxi(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.click_call_taxi)
        ).click()

    def select_comfort_tariff(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.comfort_tariff_button)
        ).click()

    def confirm_comfort_tariff(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(self.active_plan_card)
        ).text

    def add_phone_number(self, phone_number):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.phone_button)
        ).click()

        phone_input = self.wait.until(
            expected_conditions.visibility_of_element_located(self.phone_input)
        )
        phone_input.clear()
        phone_input.send_keys(phone_number)

    def open_method_payment(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.payment_method_button)
        ).click()

    def add_payment_method(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.add_card_button)
        ).click()

    def set_card_number(self, number):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.card_number_input)
        ).send_keys(number)

    def set_card_code(self, code):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.card_code_input)
        ).send_keys(code)

    def lost_focus(self):
        self.driver.find_element(*self.card_code_input).send_keys(Keys.TAB)

    def confirm_add_card(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.add_payment_card_button)
        ).click()

    def card_added(self, last4):
        card_checkbox = self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH,
                 f'//div[@class="card-list"]//div[contains(text(), "****{last4}")]/preceding-sibling::input')
            )
        )
        return card_checkbox.is_displayed() and card_checkbox.is_enabled()

    def close_payment_modal(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.close_payment_modal_button)
        ).click()

    def send_message_to_driver(self, message):
        input_box = self.wait.until(
            expected_conditions.visibility_of_element_located(self.driver_message)
        )
        input_box.clear()
        input_box.send_keys(message)

    def select_blanket_and_tissues(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.blanket_and_tissues_checkbox)
        ).click()

    def add_2_ice_cream(self, quantity=2):
        plus_button = self.wait.until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)
        )
        for _ in range(quantity):
            plus_button.click()

    def find_taxi(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.order_taxi)
        ).click()


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_route(data.address_from, data.address_to)

    def test_set_route(self):
        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    def test_set_order_taxi(self):
        self.routes_page.set_order_taxi()

    def test_set_comfort(self):
        self.routes_page.select_comfort_tariff()
        assert self.routes_page.confirm_comfort_tariff() == 'Comfort'

    def test_set_phone_number(self):
        self.routes_page.add_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(By.ID, 'code').send_keys(code)

    def test_set_payment_method(self):
        self.routes_page.open_method_payment()
        self.routes_page.add_payment_method()

        self.routes_page.set_card_number(data.card_number)
        self.routes_page.set_card_code(data.card_code)

        self.routes_page.lost_focus()
        assert self.routes_page.card_added(data.card_number[-4:]), \
            "La tarjeta no se agregó correctamente"

        self.routes_page.close_payment_modal()

    def test_send_message_to_driver(self):
        self.routes_page.send_message_to_driver('Voy muy pedo, manejar con cuidado')

    def test_select_blanket_and_tissues(self):
        self.routes_page.select_blanket_and_tissues()

    def test_add_2_ice_cream(self):
        self.routes_page.add_2_ice_cream(2)

    def test_find_taxi(self):
        self.routes_page.find_taxi()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()