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
#1 Configurar la dirección
    def test_set_route(self):
        self.fill_direction()

        time.sleep(3)
        self.driver.save_screenshot("test_set_route_1.png")

        routes_page = methods.UrbanRoutesPage(self.driver)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

#2 Seleccionar la tarifa Comfort.
    def test_select_comfort_rate(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        self.driver.save_screenshot("test_select_comfort_rate_2.png")
        # Presionar botones de selección
        routes_page.click_element(routes_page.locators.div_personal)
        assert routes_page.get_element_text(routes_page.locators.div_personal) == 'Personal'

        routes_page.click_element(routes_page.locators.button_taxi)
        assert routes_page.get_element_text(routes_page.locators.button_taxi) == 'Pedir un taxi'

        routes_page.click_element(routes_page.locators.img_comfort)
#3 Rellenar el número de teléfono
    def test_phone_number(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        # Click en telefono para interactuar con el modal
        routes_page.click_element(routes_page.locators.div_tel)
        assert routes_page.get_element_text(routes_page.locators.div_tel) == 'Número de teléfono'

        routes_page.fill_input(routes_page.locators.input_tel, data.phone_number)
        assert routes_page.get_element_value(routes_page.locators.input_tel) == data.phone_number
        routes_page.click_element(routes_page.locators.button_siguiente)
        assert routes_page.get_element_text(routes_page.locators.button_siguiente) == 'Siguiente'

        self.driver.save_screenshot("test_phone_number_3.png")
        # Sección para SMS
        sms = funtions.retrieve_phone_code(self.driver)
        routes_page.fill_input(routes_page.locators.input_code, sms)
        assert routes_page.get_element_value(routes_page.locators.input_code) == sms
        #Sección boton confirmar
        self.driver.save_screenshot("test_phone_number_3-1.png")
        routes_page.click_element(routes_page.locators.button_confirmar)
        assert routes_page.get_element_text(routes_page.locators.button_confirmar) == 'Confirmar'

#4 Agregar una tarjeta de crédito
    def test_payment_method(self):
        routes_page = methods.UrbanRoutesPage(self.driver)

        # Metodo de pago
        routes_page.click_element(routes_page.locators.div_pago)
        routes_page.click_element(routes_page.locators.div_tarjeta)
        self.driver.save_screenshot("test_payment_method_4.png")
        # Modal TC
        routes_page.fill_input(routes_page.locators.input_tc_number, data.card_number)
        routes_page.press_tab(routes_page.locators.input_tc_number) # <---- Aquí esta el TAB
        routes_page.fill_input(routes_page.locators.input_tc_cvv, data.card_code)
        assert routes_page.get_element_value(routes_page.locators.input_tc_number) == data.card_number
        assert routes_page.get_element_value(routes_page.locators.input_tc_cvv) == data.card_code
        #boton agregar
        assert routes_page.get_element_text(routes_page.locators.button_agregar) == 'Agregar'
        routes_page.click_element(routes_page.locators.button_agregar)
        self.driver.save_screenshot("test_payment_method_4-1.png")
        routes_page.click_element(routes_page.locators.button_close)

#5 Escribir un mensaje para el controlador.
    def test_message_driver(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        # Mensaje al controlador
        routes_page.fill_input(routes_page.locators.input_comment, data.message_for_driver)
        assert routes_page.get_element_value(routes_page.locators.input_comment) == data.message_for_driver
        routes_page.press_tab(routes_page.locators.input_comment) # <---- Aquí esta el TAB
        self.driver.save_screenshot("test_message_driver_5.png")

#6 Pedir una manta y pañuelos.
    def test_blanket_scarve(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        # Click manta y pañuelos - Aquí ya está abierta la sección "Requisitos del pedido"
        routes_page.click_checkbox_manta_panuelos()

#7 Pedir 2 helados.
    def test_select_two_icecream(self):
        routes_page = methods.UrbanRoutesPage(self.driver)

        # Click dos veces en el helado
        routes_page.click_element(routes_page.locators.div_mas_helado)
        routes_page.click_element(routes_page.locators.div_mas_helado)
        assert routes_page.get_element_text(routes_page.locators.div_cantidad_helados) == '2'
        self.driver.save_screenshot("test_select_two_icecream_7.png")

#8 Aparece el modal para buscar un taxi.
    def test_start_button(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        #Click en boton final
        routes_page.click_element(routes_page.locators.button_final)
        assert routes_page.get_element_text(routes_page.locators.button_final) == '<span class="smart-button-main">Pedir un taxi</span><span class="smart-button-secondary">El recorrido será de 1 kilómetros y se hará en 2 minutos</span>'
        self.driver.save_screenshot('test_start_button_8.png')

#9 Esperar a que aparezca la información del conductor en el modal
    def test_wait_modal_recuest(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.wait_llegada_is_visible(routes_page.locators.div_llegada)
        self.driver.save_screenshot("test_wait_modal_recuest_9.png")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
