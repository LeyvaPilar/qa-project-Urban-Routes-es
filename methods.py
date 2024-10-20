import locators
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
        self.locators = locators.UrbanRoutesPage()

    def set_from(self, from_address):
        self.driver.find_element(*self.locators.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.locators.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.locators.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.locators.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.locators.from_field).send_keys(address_from)
        self.driver.find_element(*self.locators.to_field).send_keys(address_to)

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
        self.driver.execute_script("document.querySelector('" + self.locators.checkbox_manta_panuelos + "').click()")

    def wait_llegada_is_visible(self, locator):
        WebDriverWait(self.driver, 40).until(expected_conditions.visibility_of_element_located(locator))