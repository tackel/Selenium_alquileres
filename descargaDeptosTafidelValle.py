
import pandas as pd
from pandas import ExcelWriter
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
paginacion = 1
# Definimos la URL-principal y la ruta al driver de chrome

main = 'https://tafidelvalle.com/donde-alojarse-en-tafi-del-valle'  # URL principal


ciudad_list = []
mail_list = []
direccion_list = []
contacto_tel = {}
nombre_list = []
tel_list = []
cel_list = []
titulo_de_la_publicacion = []
cantidad_visitados = 0
esperaLarga = 1
espera = 0.5
lista_links = []


# Abrimos una ventana con la URL-principal
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get(main)

driver.maximize_window()

sleep(esperaLarga)


try:

    cards = driver.find_elements_by_class_name('portfolio-desc')
    for card in cards:
        elem = card.find_elements_by_xpath(".//h3/a[@href]")
        for i in elem:
            lista_links.append(i.get_attribute("href"))

    # sleep(espera)

    for u in lista_links:
        cantidad_visitados += 1
        driver.get(u)

        sleep(espera)

        try:
            # driver.send_keys(Keys.CONTROL  + Keys.RETURN)

            # sleep(esperaLarga)
            try:
                nombres = driver.find_element(
                    By.XPATH, '//*[@id="page-title"]/div/h1/a').text
            except:
                nombres = '---'
            try:
                direccion = driver.find_element(By.XPATH,
                                                ".//li[@title='Dirección']/span").text

            except:
                direccion = '--'

            try:
                telefonos = driver.find_element(By.XPATH,
                                                ".//li[@title='Teléfono']/a").text
            except:
                telefonos = '--'

            try:
                celular = driver.find_element(By.XPATH,
                                              ".//li[@title='Celular']/a").text
            except:
                celular = '--'

            try:
                mail = driver.find_element(By.XPATH,
                                           ".//li[@title='Email']/span/a").text
            except:
                mail = '---'
            try:
                ciudad = driver.find_element(By.XPATH,
                                             ".//li[@title='Localidad']/span").text
            except:
                ciudad = '---'

            print(
                f'Direccion: {nombres}, {direccion}, {telefonos}, {celular}, {mail}, {ciudad} ')
            # sleep(espera)

            nombre_list.append(str(nombres))
            direccion_list.append(str(direccion))
            tel_list.append(telefonos)
            cel_list.append(celular)
            mail_list.append(mail)
            ciudad_list.append(ciudad)

            df = pd.DataFrame({
                'Nombre': nombre_list,
                'Direccion': direccion_list,
                'Telefono': tel_list,
                'Celular': cel_list,
                'Mail': mail_list,
                'Ciudad': ciudad_list,
            })

            # Cerrar la nueva pestaña de URL-secundaria
            # driver.close()

            # Cambiar el foco, para volver a la URL-principal

        except:
            driver.close()

            # Cambiar el foco, para volver a la URL-principal
            driver.switch_to.window(driver.window_handles[0])
            sleep(espera)

    # siguiente = driver.find_element_by_xpath("//span[@aria-label='Next']")
    # siguiente.click()

    # print('######### apreto next #########')
    # paginacion += 1
    # print(f'pagina numero {str(paginacion)}')

    # sleep(esperaLarga)
except:
    pass

df = df[['Ciudad', 'Nombre', 'Telefono', 'Celular', 'Mail', 'Direccion']]
writer = ExcelWriter('./lista_de_contactos.xlsx')
df.to_excel(writer, 'Hoja de datos', index=False)
writer.save()


print("######### Cerramos navegador #########")
print(
    f'#########  se visitaron {cantidad_visitados} de alojamientos #########')
driver.close()
