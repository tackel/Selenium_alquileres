from numpy.lib.function_base import append
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pandas import ExcelWriter
from openpyxl import Workbook
import random
from time import sleep
from selenium import webdriver
paginacion = 1
# Definimos la URL-principal y la ruta al driver de chrome

main = 'https://www.alquilerargentina.com/Chaco/'  # URL principal

main_pag = main+'_Ord:PD?pag='

main_url = main_pag+str(paginacion)

ciudad_list = []
provincia_list = []
contacto_tel = {}
nombre_list = []
tel_list = []
titulo_de_la_publicacion = []
cantidad_visitados = 0
esperaLarga = random.uniform(4.0, 6.0)
espera = random.uniform(2.0, 4.0)


chromedriver = './chromedriver'
# Abrimos una ventana con la URL-principal
driver = webdriver.Chrome(chromedriver)
driver.get(main_pag+str(paginacion))


# driver.maximize_window()

sleep(esperaLarga)
boton_next = 0
while boton_next == 0:
    try:
        sleep(esperaLarga)
        urls = driver.find_elements_by_xpath(
            '//div[@class="AnuncioCardListado__descripcion-texto"]')

        #   y los imorimo en consola
        sleep(espera)
        for u in urls:
            cantidad_visitados += 1
            u.click()
            sleep(espera)

            try:
                #driver.send_keys(Keys.CONTROL  + Keys.RETURN)
                driver.switch_to.window(driver.window_handles[1])
                # sleep(esperaLarga)
                ciudad = driver.find_element_by_xpath(
                    '//*[@class="BreadcrumbFicha__lista ul-limpia"]/li[3]').text
                provincia = driver.find_element_by_xpath(
                    '//*[@class="BreadcrumbFicha__lista ul-limpia"]/li[2]').text
                titulo = driver.find_element_by_xpath(
                    '//*[@class="BreadcrumbFicha__lista ul-limpia"]/li[4]').text
                sleep(espera)
                boton = driver.find_element_by_xpath(
                    '//button[@class="ContactosDesktop__llamar btn btn-naranja"]')

                # le doy click
                boton.click()
                # espero que cargue la informacion dinamica
                contactos = driver.find_elements_by_xpath(
                    '//div[@class="ModalTelefonosFicha__fondo"]')

                # busco el boton nuevamente para darle click en la siguiente iteracion

                # si hay algun error, rompo el lazo. No me complico.
                # Recorro cada uno de los anuncios que he encontrado
                for contacto in contactos:
                    # Por cada anuncio hallo el preico
                    nombres = contacto.find_element_by_xpath(
                        './/span[@class="ModalTelefonosFicha__nombre-contacto"]').text

                    # Por cada anuncio hallo la descripcion
                    telefonos = contacto.find_element_by_xpath(
                        './/div[@class="ModalTelefonosFicha__texto"]').text

                    contacto_tel[str(nombres)] = str(telefonos)
                    nombre_list.append(str(nombres))
                    tel_list.append(telefonos)
                    titulo_de_la_publicacion.append(titulo)
                    ciudad_list.append(ciudad)
                    provincia_list.append(provincia)

                    df = pd.DataFrame({
                        'Nombre': nombre_list,
                        'Telefono': tel_list,
                        'Publicacion': titulo_de_la_publicacion,
                        'Ciudad': ciudad_list,
                        'Provincia': provincia_list
                    })

                # Cerrar la nueva pestaña de URL-secundaria
                driver.close()

                # Cambiar el foco, para volver a la URL-principal
                driver.switch_to.window(driver.window_handles[0])
            except:

                driver.close()

                # Cambiar el foco, para volver a la URL-principal
                driver.switch_to.window(driver.window_handles[0])
                sleep(espera)

        siguiente = driver.find_element_by_xpath("//span[@aria-label='Next']")
        siguiente.click()

        print('######### apreto next #########')
        paginacion += 1
        print(f'pagina numero {str(paginacion)}')

        sleep(esperaLarga)
    except:
        boton_next += 1

df = df[['Provincia', 'Ciudad', 'Publicacion', 'Nombre', 'Telefono', ]]
writer = ExcelWriter('./lista_de_contactos.xlsx')
df.to_excel(writer, 'Hoja de datos', index=False)
writer.save()


print("######### Cerramos navegador #########")
print(
    f'#########  se visitaron {cantidad_visitados} de alojamientos #########')
driver.close()
