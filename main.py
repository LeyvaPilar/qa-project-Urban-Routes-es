import time
import data
import methods
import funtions

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

driver = webdriver.Chrome()

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
        routes_page = methods.UrbanRoutesPage(self.driver)
        # Wait element is visible
        routes_page.wait_element_is_visible(routes_page.locators.from_field)
        # Fill form, from & to
        routes_page.set_route(data.address_from, data.address_to)

    def test_set_route(self):
        self.fill_direction()

        time.sleep(3)
        self.driver.save_screenshot("test_set_route_1.png")

        routes_page = methods.UrbanRoutesPage(self.driver)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_rate(self):
        self.fill_direction()
        routes_page = methods.UrbanRoutesPage(self.driver)
        self.driver.save_screenshot("test_select_comfort_rate_1.png")
        routes_page.click_element(routes_page.locators.div_personal)
        routes_page.click_element(routes_page.locators.button_taxi)
        routes_page.click_element(routes_page.locators.img_comfort)
        routes_page.click_element(routes_page.locators.div_tel)
        routes_page.fill_input(routes_page.locators.input_tel, data.phone_number)
        routes_page.click_element(routes_page.locators.button_siguiente)
        self.driver.save_screenshot("test_select_comfort_rate_2.png")
        # Sección para SMS
        sms = funtions.retrieve_phone_code(self.driver)
        routes_page.fill_input(routes_page.locators.input_code, sms)
        self.driver.save_screenshot("test_select_comfort_rate_3.png")
        routes_page.click_element(routes_page.locators.button_confirmar)
        # Metodo de pago
        routes_page.click_element(routes_page.locators.div_pago)
        routes_page.click_element(routes_page.locators.div_tarjeta)
        self.driver.save_screenshot("test_select_comfort_rate_4.png")
        # Modal TC
        routes_page.fill_input(routes_page.locators.input_tc_number, data.card_number)
        routes_page.press_tab(routes_page.locators.input_tc_number)
        routes_page.fill_input(routes_page.locators.input_tc_cvv, data.card_code)
        routes_page.click_element(routes_page.locators.button_agregar)
        self.driver.save_screenshot("test_select_comfort_rate_5.png")
        routes_page.click_element(routes_page.locators.button_close)
        # Mensaje al controlador
        routes_page.fill_input(routes_page.locators.input_comment, data.message_for_driver)
        routes_page.press_tab(routes_page.locators.input_comment)
        self.driver.save_screenshot("test_select_comfort_rate_6.png")
        # Click manta y pañuelos - Aquí ya está abierta la sección "Requisitos del pedido"
        routes_page.click_checkbox_manta_panuelos()
        # Click dos veces en el helado
        routes_page.click_element(routes_page.locators.div_mas_helado)
        routes_page.click_element(routes_page.locators.div_mas_helado)
        self.driver.save_screenshot("test_select_comfort_rate_7.png")
        #Click en boton final
        routes_page.click_element(routes_page.locators.button_final)

        self.driver.save_screenshot('test_select_comfort_rate_8.png')
        time.sleep(35)
        self.driver.save_screenshot("test_select_comfort_rate_9.png")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
