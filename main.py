import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time
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

    call_taxi = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    comfort_tariff = (By.XPATH, '//div[@class="tcard-title" and contains(text(),"Comfort")]')

    phone_button = (By.XPATH, '//div[@class="np-text" and contains(text(),"Phone number")]')
    phone_input = (By.ID, 'phone')
    next_step_number = (By.XPATH, '//button[@type="submit"]')
    add_code = (By.ID, 'code')
    confirm_number = (By.XPATH, '//button[@class="button full" and contains(text(),"Confirm")]')

    payment_method_button = (By.XPATH, '//div[@class="pp-button filled"]')
    add_card_button = (By.XPATH, '//img[@src="/static/media/plus.d25b8941.svg"]')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, '//input[@placeholder="12"]')
    add_payment_card_button = (By.XPATH, '//button[@class="button full" and contains(text(),"Add")]')
    close_payment_modal_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')

    driver_message = (By.ID, 'comment')

    blanket_and_tissues_checkbox = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')

    ice_cream_plus_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')

    order_taxi = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')

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
        time.sleep(3)

#Pedir taxi
    def set_order_taxi(self):
        self.driver.find_element(*self.call_taxi).click()
        time.sleep(3)

#Seleccionar tarifa comfort
    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()
        time.sleep(3)

# Seleccionar modulo agregar numero celular
    def module_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_button).click()
        time.sleep(5)

    def set_phone_number(self):
        self.driver.find_element(*self.phone_input).send_keys(data.phone_number)
        time.sleep(5)

    def next_step_add_number(self):
        self.driver.find_element(*self.next_step_number).click()
        time.sleep(5)

    def confirm_code(self):
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.confirm_number).send_keys(code)
        time.sleep(5)

    def confirm_number_module(self):
        self.driver.find_element(*self.confirm_number).click()
        time.sleep(5)

#Agregar metodo de pago
    def open_method_payment(self):
        self.driver.find_element(*self.payment_method_button).click()
        time.sleep(5)

    def add_payment_method(self):
        self.driver.find_element(*self.add_card_button).click()
        time.sleep(5)

    def set_card_number(self, number):
        self.driver.find_element(*self.card_number_input).send_keys(data.card_number)
        time.sleep(5)

    def set_card_code(self, code):
        self.driver.find_element(*self.card_code_input).send_keys(data.card_code)
        time.sleep(5)

    def lost_focus(self):
        self.driver.find_element(*self.card_code_input).send_keys(Keys.TAB)
        time.sleep(5)

    def confirm_add_card(self):
        self.driver.find_element(*self.add_payment_card_button).click()
        time.sleep(5)

    def close_payment_modal(self):
        self.driver.find_element(*self.close_payment_modal_button).click()
        time.sleep(5)

    def send_message_to_driver(self, message):
        self.driver.find_element(*self.driver_message).send_keys(data.message_for_driver)
        time.sleep(5)

    def select_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_and_tissues_checkbox).click()
        time.sleep(5)

    def add_2_ice_cream(self, quantity=2):
        self.driver.find_element(*self.ice_cream_plus_button).click()
        time.sleep(3)
        self.driver.find_element(*self.ice_cream_plus_button).click()
        time.sleep(3)

    def find_taxi(self):
        self.driver.find_element(*self.order_taxi).click()
        time.sleep(5)

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # Importamos Options para las versiones nuevas de Selenium
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        # Aquí configuramos los logs de performance que necesitas para el código de confirmación
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        # Iniciamos el driver usando el argumento 'options'
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_route(data.address_from, data.address_to)

#LLenar rutas
    def test_set_route(self):
        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

#Seleccionar tarifa confort
    def test_set_comfort(self):
        self.routes_page.set_order_taxi()
        self.routes_page.select_comfort_tariff()

#Agregar numero telefonico
    def test_set_phone_number(self):
        self.routes_page.set_order_taxi()
        self.routes_page.select_comfort_tariff()
        self.routes_page.module_phone_number(data.phone_number)
        self.routes_page.set_phone_number()
        self.routes_page.next_step_add_number()
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(By.ID, 'code').send_keys(code)
        self.routes_page.confirm_number_module()

#Agrega metodo de pago
    def test_set_payment_method(self):
        self.routes_page.set_order_taxi()
        self.routes_page.select_comfort_tariff()
        self.routes_page.open_method_payment()
        self.routes_page.add_payment_method()
        self.routes_page.set_card_number(data.card_number)
        self.routes_page.set_card_code(data.card_code)
        self.routes_page.lost_focus()
        self.routes_page.confirm_add_card()
        self.routes_page.close_payment_modal()

#Enviar mensaje al conductor
    def test_send_message_to_driver(self):
        self.routes_page.set_order_taxi()
        self.routes_page.select_comfort_tariff()
        self.routes_page.send_message_to_driver(data.message_for_driver)

#Elegir mantas y pañuelos
    def test_select_blanket_and_tissues(self):
        self.routes_page.set_order_taxi()
        self.routes_page.select_comfort_tariff()
        self.routes_page.select_blanket_and_tissues()

#Elegir 2 helados
    def test_add_2_ice_cream(self):
        self.routes_page.set_order_taxi()
        self.routes_page.select_comfort_tariff()
        self.routes_page.add_2_ice_cream()

#Solicitar taxi
    def test_find_taxi(self):
        self.routes_page.set_order_taxi()
        self.routes_page.select_comfort_tariff()
        self.routes_page.module_phone_number(data.phone_number)
        self.routes_page.set_phone_number()
        self.routes_page.next_step_add_number()
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(By.ID, 'code').send_keys(code)
        self.routes_page.confirm_number_module()
        self.routes_page.open_method_payment()
        self.routes_page.add_payment_method()
        self.routes_page.set_card_number(data.card_number)
        self.routes_page.set_card_code(data.card_code)
        self.routes_page.lost_focus()
        self.routes_page.confirm_add_card()
        self.routes_page.close_payment_modal()
        self.routes_page.find_taxi()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()