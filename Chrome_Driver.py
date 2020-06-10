import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import unittest
import os
import shutil
import glob
from datetime import datetime
import pandas as pd
from inicioSesionAdmin import *



class usando_unittest(unittest.TestCase):

    def setUp(self):
        self.inicioSesionAdmin=inicioSesionAdmin()
        self.inicioSesionAdmin.setUp()
        self.inicioSesionAdmin.test_nombreUsuarios()
        correos=self.inicioSesionAdmin.correos
        print(correos)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("prefs", {
          "download.default_directory": r"E:\ARUS S.A\Proyectos\Python\Webex\Chrome_Driver\Chrome_Driver\Archivos",
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'chromedriver.exe')

    def test_usando_toggle(self):
        reportes=[]
        driver = self.driver
        driver.get('https://contactounicauca.webex.com/');
                            # Optional argument, if not specified will search path.
                         # Let the user actually see something!
        link = driver.find_element_by_xpath('//*[@id="main_top_menu"]/div[2]/div/div[2]/a/div/button[1]')
        link.click()
        wait=WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="IDToken1"]')))
        usuario=driver.find_element_by_xpath('//*[@id="IDToken1"]')
        correo='csjulian@unicauca.edu.co'
        usuario.send_keys(correo)
        usuario.send_keys(Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="IDToken2"]')))
        clave = driver.find_element_by_xpath('//*[@id="IDToken2"]')
        clave.send_keys("G849jNN43#")
        clave.send_keys(Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="classicView"]'))) # Let the user actually see something!
        driver.get('https://contactounicauca.webex.com/tc3300/trainingcenter/report/endUserReport.do?actionFlag=SessionReport&typeFlag=menu&siteurl=contactounicauca')
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/select[1]')))
        fecha=datetime.now()
        #FECHA INICIO-REPORT
        mesInicio=Select(driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/select[2]'))
        mesInicio.select_by_value("4")
        diaInicio=Select(driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/select[1]'))
        diaInicio.select_by_value("2")
        #FECHA FIN-REPORT
        mesFin=Select(driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/select[2]'))
        mesFin.select_by_value(str(fecha.month))
        diaFin=Select(driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/select[1]'))
        diaFin.select_by_value(str(fecha.day))
        #boton display
        btnDisplay=driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/table/tbody/tr[4]/td[2]/nobr/input')
        btnDisplay.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr/td/table')))
        #abrir cada reporte
        rows=len(driver.find_elements_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr[2]")) 
        for n in range(0,rows+1):
            valor = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr["+ str(n+2) +"]/td[2]/font/a")
            rows=len(driver.find_elements_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr[2]")) 
            valor.click()
            wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/form/table[1]/tbody/tr[3]/td[2]/input[2]')))
            export = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/form/table[1]/tbody/tr[3]/td[2]/input[2]")
            export.click()
            #Cambiar nombre del reporte
            time.sleep(4)
            filepath = 'E:\ARUS S.A\Proyectos\Python\Webex\Chrome_Driver\Chrome_Driver\Archivos'
            filename = max([f for f in os.listdir(filepath)], key=lambda xa : os.path.getctime(os.path.join(filepath,xa)))
            clase1=driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/form/table[1]/tbody/tr[3]/td[1]/font/b").text
            clase=clase1.split('"')
            newname=correo+' '+clase[1]+'.csv'
            if '.part' in filename:
                time.sleep(2)
                os.rename(os.path.join(filepath, filename), os.path.join(filepath, newname))
            else:
                os.rename(os.path.join(filepath, filename),os.path.join(filepath,newname))
            dir=os.path.join(filepath,newname)
            reportes.append(open(os.path.join(filepath, newname), 'rb').read())
            driver.back()
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr/td/table')))
        fecha=datetime.now()
        newname='Reporte Completo '+ correo +' Fecha '+ str(fecha.date()) +'.csv'
        content=''
        content1=content.encode('cp1252')
        for n in range(0,len(reportes)):
            content1=content1+reportes[n]
        out = open(os.path.join(filepath,newname), 'wb')
        out.write(content1)
        out.close()



    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
	  unittest.main()

