#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
import time
import sys

# print(sys.argv)
path = sys.argv[1]
prog_file = sys.argv[2]
week = sys.argv[3]
# pdf programme de colle without extension
prog = prog_file[:-4]

def get_id():
    """
    Fetch the id and password of Cahier de Prepa
    """
    f_ident = open("/home/eb/Dropbox/.latex/Commands/ident-cahier-prepa.txt","r")
    lecture_ident = f_ident.read()
    f_ident.close()
    return lecture_ident.split()[0], lecture_ident.split()[1]

def uploaded(l,p):
    """
    Check if programme de colle already uploaded
    """
    for prog in l:
        if prog.text == p:
            return True
    return False

def waitabit(driver=None,t=1.5):
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    time.sleep(t)
    # pass

# connect to cahier de prepa
chrome_options = Options()
chrome_options.add_argument("--headless")       # to run in the background
service = Service('/home/eb/Dropbox/.latex/Commands/chromedriver')
# driver = webdriver.Chrome('/home/eb/Dropbox/.latex/Commands/chromedriver')
# , options=chrome_options)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
url1 = "https://cahier-de-prepa.fr/pc-theo/docs?rep=28"
driver.get(url1)

userName, passWord = get_id()
elem = driver.find_element(by=By.NAME, value="login")
elem.send_keys(userName)
elem = driver.find_element(by=By.NAME, value="motdepasse")
elem.send_keys(passWord)
elem.send_keys(Keys.RETURN)
waitabit(driver=driver)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

# go to programme de colle page
list_prog = driver.find_elements(by=By.CSS_SELECTOR, value="span[class='nom editable']")
waitabit(driver=driver)

# upload if not present
if uploaded(list_prog,prog):
    # print('---> Programme de colle already uploaded, updating...')
    driver.find_elements(by=By.CSS_SELECTOR, value="a[class='icon-actualise formulaire']")[-1].click()
    # waitabit(driver=driver)
    choose_file = driver.find_element(by=By.CSS_SELECTOR, value="input[id='fichier']")
    # waitabit(driver=driver)
    choose_file.send_keys(path + prog_file)
    # waitabit(driver=driver)
    driver.find_element(by=By.CSS_SELECTOR, value="a[class='icon-envoidoc']").click()
else:
    # print('---> Uploading programme de colle...')
    driver.find_element(by=By.CSS_SELECTOR, value="a[class='icon-ajoutedoc formulaire']").click()
    choose_file = driver.find_element(by=By.CSS_SELECTOR, value="input[name='fichier[]']")
    choose_file.send_keys(path + prog_file)
    driver.find_element(by=By.CSS_SELECTOR, value="a[class='icon-envoidoc']").click()

# ajout dans onglet programme de colle
waitabit(driver=driver)
try:
    url2 = "https://cahier-de-prepa.fr/pc-theo/progcolles?phys"
    driver.get(url2)
    waitabit(driver=driver)
    
    # essaye de supprimer le lien vers programme de colle si déjà présent
    try:
        # find the last element which contains the icon supprime
        driver.find_elements(by=By.CSS_SELECTOR, value="a[class='icon-supprime']")[-1].click()
        # driver.find_element(by=By.CSS_SELECTOR, value="a[class='icon-supprime']").click()
        waitabit(driver=driver)
        driver.find_element(by=By.CSS_SELECTOR, value="button[class='icon-ok']").click()
        waitabit(driver=driver)
    except:
        pass
    # print('---> Programme de colle already in onglet programme de colle')
    liste_semaines = driver.find_elements(by=By.CSS_SELECTOR, value="h3[class='edition']")
    for i, semaine in enumerate(liste_semaines):
        # print(i, semaine.text, week)
        if week in semaine.text:
            break
    # waitabit(driver=driver,t=0.2)
    driver.find_elements(by=By.CSS_SELECTOR, value="a[class='icon-ajoutecolle']")[i].click()
    waitabit(driver=driver)
    driver.find_element(by=By.CSS_SELECTOR, value="button[class='icon-lien1']").click()
    waitabit(driver=driver,t=0.2)
    background = driver.find_element(by=By.CSS_SELECTOR, value="select[id='rep']")
    menu = Select(driver.find_element(by=By.CSS_SELECTOR, value="select[id='rep']"))
    menu.select_by_visible_text('Physique/Programme de colle')
    waitabit(driver=driver,t=0.2)
    menu = Select(driver.find_element(by=By.CSS_SELECTOR, value="select[id='doc']"))
    menu.select_by_visible_text(prog_file[:-4] + ' (pdf)')
    waitabit(driver=driver,t=0.2)
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(background, 0, 200)
    action.click()
    action.perform()
    waitabit(driver=driver,t=0.2)
    driver.find_element(by=By.CSS_SELECTOR, value="article[id='fenetre']>a[class='icon-ok']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="a[class='icon-ok']").click()
    # waitabit(driver=driver)
except(NoSuchElementException):
    pass
    # print('---> Programme de colle already in onglet programme de colle')

# close the driver
driver.close()
# print('Programme de colle téléversé avec succès.')
