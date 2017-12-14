from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# driver =webdriver.Firefox()
# driver.maximize_window()
# driver.get('http://mail.163.com/')
# time.sleep(2)
# driver.switch_to.frame('x-URS-iframe')
# elem = driver.find_element_by_name('email')
# elem.send_keys('songyue_bupt')
# elem = driver.find_element_by_name('password')
# elem.send_keys('19941210songyue')
# elem.send_keys(Keys.RETURN)


driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://www.baidu.com/')
time.sleep(2)
# elem = driver.find_element_by_name('wd')
# print(elem)
# elem.send_keys('python')
# elem.send_keys(Keys.RETURN)

print(driver.page_source)

driver.quit()