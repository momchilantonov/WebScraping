# imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import time

# set some options for headless scraping
options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')

# set website, path and connect (open) the website
web = 'https://www.technopolis.bg/bg//TV%2C-Video-i-Gaming/Televizori/c/P11090104?pricerange=&pageselect=30&page=0&q=:price-asc&text=&layout=List'
path = '/home/momchil/Downloads/chromedriver/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=options)
driver.get(web)
# driver.maximize_window()

# set empty lists for the items (tags, values) that you want to scrap
titles = []
codes = []
price = []

# create paginator (pages) to scrap the whole website thru all pages
pagination = driver.find_element_by_xpath('//ul[@class="paging"]')
pages = pagination.find_elements_by_tag_name('li')
last_page = int(pages[-2].text)
current_page = 1

# loop while get the last page
while True:
    # add some time (3s) to let the website to render (implicit)
    # time.sleep(3)

    # break condition
    if current_page > last_page:
        break

    # set containers where all your data is (the code under comment is implicit variant, and the other is explicit)
    product_list = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'products-list-list')))
    # product_list = driver.find_element_by_class_name('products-list-list')
    products = WebDriverWait(product_list, 5).until(ec.presence_of_all_elements_located((By.XPATH, './li[@class="list-item"]')))
    # products = product_list.find_elements_by_xpath('./li[@class="list-item"]')

    # loop thru all elements in the container
    for product in products:
        titles.append(product.find_element_by_xpath('.//h3[@class="item-name"]/a').text)
        codes.append(product.find_element_by_xpath('.//span[@class="item-number"]').text)
        price.append(product.find_element_by_xpath('.//span[@class="price-value"]').text)

    # increase the current page for the while loop
    current_page += 1

    # try to click on the next page
    try:
        next_page = driver.find_element_by_xpath('//li[@class="next"]')
        next_page.click()
    except:
        pass

# disconnect (close) the website
driver.quit()

# create dataFrame with pandas
tv_2 = pd.DataFrame(
    {
        'title': titles,
        'code': codes,
        'price': price,
    }
)
# save the dataFrame to a CSV file
tv_2.to_csv('tv_2.csv', index_label='index')
