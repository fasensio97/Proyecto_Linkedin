#!/usr/bin/env python
# coding: utf-8

# In[21]:


# Import libraries and packages for the project
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from googlesearch import search

import pandas as pd

print('- Finish importing packages')


# In[22]:


# Inicializar el controlador de Selenium
driver = webdriver.Chrome()

url1 = 'https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22director+de+recursos+humanos%22+AND+%22Argentina%22&source=hp&ei=ADwHZLiUNbzX1sQPqvqawAk&iflsig=AK50M_UAAAAAZAdKEFBfi9Gijt50g9eYjaWC2X3f8JID'

# Navegar a la página web que deseas
driver.get(url1)

current_url = driver.current_url
page = requests.get(current_url)

soup = BeautifulSoup(page.content, "html.parser")


# In[10]:


# Task 1: Login to LinkedIn

# Task 1.1: Open Chrome and Access LinkedIn login site
driver = webdriver.Chrome()
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Task 1.2: Import username and password
username = 'federicoasensio1808@gmail.com'
from getpass import getpass
password = getpass('Introduce tu contraseña: ')
print('- Finish importing the login credentials')
sleep(2)

# Task 1.3: Key in login credentials
email_field = driver.find_element("id", 'username')
email_field.send_keys(username)
print('- Finish keying in email')
sleep(3)

password_field = driver.find_element("name", 'session_password')
password_field.send_keys(password)
print('- Finish keying in password')
sleep(2)

# Task 1.4: Click the Login button
signin_field = driver.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
sleep(3)

print('- Finish Task 1: Login to LinkedIn')


# In[11]:


search_query = input('What profile do you want to scrape? ')

search_field = driver.find_element(By.CSS_SELECTOR, '#global-nav-typeahead > input')
search_field.clear()
search_field.send_keys(search_query)

# Task 2.3: Search
search_field.send_keys(Keys.RETURN)

print('- Finish Task 2: Search for profiles')
sleep(5)
# Task 2.4: Click on People in the filter bar
button = driver.find_element(By.CSS_SELECTOR, '#search-reusables__filters-bar > ul > li:nth-child(1) > button')
button.click()

#posible problema, ver si no cambia de lugar el botón de personas en linkedin


# In[12]:


# Task 3: Scrape the URLs of the profiles

# Task 3.1: Write a function to extract the URLs of one page
def get_urls():
    page_source = BeautifulSoup(driver.page_source, "html.parser")
    profiles = page_source.find_all('a', class_="app-aware-link")
    all_profile_URL = []
    for profile in profiles:
        profile_URL = profile.get('href')
        if profile_URL not in all_profile_URL:
            all_profile_URL.append(profile_URL)
    return all_profile_URL

# Task 3.2: Navigate through many pages and extract the profile URLs of each page
input_page = int(input('How many pages do you want to scrape? '))
URLs_all_page = []
for page in range(input_page):
    URLs_one_page = get_urls()
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(3)
    next_button = driver.find_element("class name", "artdeco-pagination__button--next")
    driver.execute_script("arguments[0].click();", next_button)
    URLs_all_page = URLs_all_page + URLs_one_page
    sleep(2)

print('- Finish Task 3: Scrape the URLs')

for item in URLs_all_page[:]:
    if not 'www.linkedin.com/in' in item:
        URLs_all_page.remove(item)


# In[17]:


# Crear una instancia del controlador del navegador
df1 = pd.DataFrame(columns=['URL', 'Title']) # Agregar la columna "Title" al dataframe

for url in URLs_all_page:
    driver = webdriver.Chrome()
    # Abrir la página web en el navegador
    driver.get(url)

    # Obtener el contenido de la página web
    page_source = driver.page_source
    title = driver.title
    # Imprimir el contenido de la página web
    #print(page_source)
    
    # Agregar la información al dataframe
    df1 = df1.append({'URL': url, 'Title': title}, ignore_index=True)
    
    # Cerrar el navegador
    driver.quit()


# In[18]:


df1


# In[19]:


#df1.to_csv('output.csv', index=False)


# In[ ]:




