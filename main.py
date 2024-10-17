from telnetlib import XAUTH

import pytest
import json
import time
import data
from selenium.common import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

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
    div_personal = (By.XPATH, '//div[text()="Personal"]')
    button_taxi = (By.XPATH, '//button[text()="Pedir un taxi"]')
    div_tel = (By.XPATH, '//div[text()="Número de teléfono"]')
    input_tel = (By.XPATH, '//input[@id="phone"]')
    img_comfort = (By.XPATH, '(//img[@alt="Comfort"])[1]')
    button_siguiente = (By.XPATH, '//button[text()="Siguiente"]')
    input_code = (By.XPATH, '//input[@id="code"]')
    button_confirmar = (By.XPATH, '//button[text()="Confirmar"]')
    div_pago = (By.XPATH, '(//div[text()="Método de pago"])[2]')
    div_tarjeta = (By.XPATH, '(//div[text()="Agregar tarjeta"])[1]')
    input_tc_number = (By.XPATH, '//input[@id="number"]')
    input_tc_cvv = (By.XPATH, "//input[@id='code' and @name='code' and @placeholder='12']")
    button_agregar =(By.XPATH, '//button[text()="Agregar"]')
    button_close = (By.XPATH, "(//button[@class='close-button section-close'])[3]")
    input_comment =(By.XPATH, '//input[@id="comment"]')
    checkbox_manta_panuelos = 'input.switch-input'
    div_requisitos_pedido = (By.XPATH, '//div[@class="reqs-arrow open"]')
    div_cubeta_helado = (By.XPATH, '//div[text()="Cubeta de helado"]')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.from_field).send_keys(address_from)
        self.driver.find_element(*self.to_field).send_keys(address_to)

    def wait_element_is_visible(self, locator):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(locator))

    def click_element(self, locator):
        self.wait_element_is_visible(locator)
        self.driver.find_element(*locator).click()

    def fill_input(self, locator, text):
        self.driver.find_element(*locator).send_keys(text)

    def press_tab(self, locator):
        self.driver.find_element(*locator).send_keys(Keys.TAB)

    def scroll_to_element(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", element)
        time.sleep(1)

    def click_checkbox_manta_panuelos(self):
        self.driver.execute_script("document.querySelector('" + self.checkbox_manta_panuelos + "').click()")


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

    def fill_direction(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        # Wait element is visible
        routes_page.wait_element_is_visible(routes_page.from_field)
        # Fill form, from & to
        routes_page.set_route(data.address_from, data.address_to)

    def test_set_route(self):
        self.fill_direction()

        time.sleep(3)
        self.driver.save_screenshot("test_set_route_1.png")

        routes_page = UrbanRoutesPage(self.driver)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_rate(self):
        self.fill_direction()
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_element(routes_page.div_personal)
        routes_page.click_element(routes_page.button_taxi)
        routes_page.click_element(routes_page.img_comfort)
        routes_page.click_element(routes_page.div_tel)
        routes_page.fill_input(routes_page.input_tel, data.phone_number)
        routes_page.click_element(routes_page.button_siguiente)
        # Sección para SMS
        sms = retrieve_phone_code(self.driver)
        routes_page.fill_input(routes_page.input_code, sms)
        routes_page.click_element(routes_page.button_confirmar)
        # Método de pago
        routes_page.click_element(routes_page.div_pago)
        routes_page.click_element(routes_page.div_tarjeta)
        # Modal TC
        routes_page.fill_input(routes_page.input_tc_number, data.card_number)
        routes_page.press_tab(routes_page.input_tc_number)
        routes_page.fill_input(routes_page.input_tc_cvv, data.card_code)
        routes_page.click_element(routes_page.button_agregar)
        routes_page.click_element(routes_page.button_close)
        # Mensaje al controlador
        routes_page.fill_input(routes_page.input_comment, data.message_for_driver)
        routes_page.press_tab(routes_page.input_comment)
        # Click manta y pañuelos - Aquí ya está abierta la sección "Requisitos del pedido"
        routes_page.click_checkbox_manta_panuelos()

        self.driver.save_screenshot('test_select_comfort_rate_3.png')
        time.sleep(5)


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

