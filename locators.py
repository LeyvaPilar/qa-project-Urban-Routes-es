from selenium.webdriver.common.by import By

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
    input_comment = (By.CSS_SELECTOR, 'input#comment')
    checkbox_manta_panuelos = 'input.switch-input'
    div_requisitos_pedido = (By.XPATH, '//div[@class="reqs-arrow open"]')
    div_cubeta_helado = (By.XPATH, '//div[text()="Cubeta de helado"]')
    div_mas_helado = (By.CLASS_NAME, "counter-plus")
    button_final = (By.CSS_SELECTOR, '.smart-button')
    div_llegada = (By.CLASS_NAME, 'order-number')
    div_cantidad_helados = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')