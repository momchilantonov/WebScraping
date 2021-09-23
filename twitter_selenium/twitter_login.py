# imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# set some options for headless scraping
options = Options()
options.headless = False
# options.add_argument('window-size=1920x1080')

# set website, path and connect (open) the website
web = 'https://twitter.com/?lang=bg'
path = '/home/momchil/Downloads/chromedriver/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=options)
driver.get(web)
# driver.maximize_window()

# got ot SignIn page if it's first try to login
time.sleep(5)
try:
    sign_in_page = driver.find_element_by_xpath('//span[@role="button"]')
    time.sleep(5)
    sign_in_page.click()
    time.sleep(5)
except:
    pass


# go to Login Form
sign_in = driver.find_element_by_xpath('//a[@href="/login"]')
time.sleep(5)
sign_in.click()
time.sleep(10)

# got to username field, fill it, and click Next button
username = driver.find_element_by_xpath('//input[@name="username"]')
username.send_keys('???')
time.sleep(5)
next_btn = driver.find_element_by_xpath('//div[@role="button" and '
                                        '@class="css-18t94o4 css-1dbjc4n r-l5o3uw r-42olwf r-sdzlij r-1phboty r-rs99b7 '
                                        'r-peo1c r-1ps3wis r-1ny4l3l r-1guathk r-o7ynqc r-6416eg r-lrvibr"]')
time.sleep(5)
next_btn.click()
time.sleep(10)

# go to password field, fil it, and click Login button
password = driver.find_element_by_xpath('//input[@name="password"]')
password.send_keys('???')
time.sleep(5)
login_btn = driver.find_element_by_xpath('//div[@role="button" and '
                                         '@class="css-18t94o4 css-1dbjc4n r-42olwf r-sdzlij r-1phboty r-rs99b7 r-peo1c '
                                         'r-1ps3wis r-1ny4l3l r-1guathk r-o7ynqc r-6416eg r-lrvibr"]')
time.sleep(5)
login_btn.click()
