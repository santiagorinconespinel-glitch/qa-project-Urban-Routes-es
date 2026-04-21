import data
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time
import Helpers

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
        self.wait = WebDriverWait(self.driver, 20)

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
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.call_taxi)
        ).click()

#Seleccionar tarifa comfort
    def select_comfort_tariff(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.comfort_tariff)
        ).click()

# Seleccionar modulo agregar numero celular
    def module_phone_number(self, phone_number):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.phone_button)
        ).click()

    def set_phone_number(self):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.phone_input)
        ).send_keys(data.phone_number)

    def next_step_add_number(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.next_step_number)
        ).click()


    def confirm_code(self):
        code = Helpers.retrieve_phone_code(self.driver)
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.confirm_number)
        ).send_keys(code)


    def confirm_number_module(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.confirm_number)
        ).click()


#Agregar metodo de pago
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
       ).send_keys(data.card_number)


    def set_card_code(self, code):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.card_code_input)
        ).send_keys(data.card_code)


    def lost_focus(self):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.card_code_input)
        ).send_keys(Keys.TAB)


    def confirm_add_card(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.add_payment_card_button)
        ).click()


    def close_payment_modal(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.close_payment_modal_button)
        ).click()


    def send_message_to_driver(self, message):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.driver_message)
        ).send_keys(data.message_for_driver)


    def select_blanket_and_tissues(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.blanket_and_tissues_checkbox)
        ).click()


    def add_2_ice_cream(self, quantity=2):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)
        ).click()
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)
        ).click()


    def find_taxi(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.order_taxi)
        ).click()