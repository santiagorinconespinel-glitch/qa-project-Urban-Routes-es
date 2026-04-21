import data
from selenium import webdriver
from selenium.webdriver.common.by import By
import Helpers
import Page

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
        cls.routes_page = Page.UrbanRoutesPage(cls.driver)

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
        code = Helpers.retrieve_phone_code(self.driver)
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
        code = Helpers.retrieve_phone_code(self.driver)
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
        