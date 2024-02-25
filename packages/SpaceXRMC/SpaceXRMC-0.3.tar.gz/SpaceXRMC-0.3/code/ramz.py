from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles

profile = profiles.Android()
try:
    driver  = Chrome(profile,executable_path='chromedriver.exe')
except:
    driver  = Chrome(profile,executable_path='chromedriver.exe',chrome_binary='chromedriver.exe')

input('laskmdkmakldklamds')