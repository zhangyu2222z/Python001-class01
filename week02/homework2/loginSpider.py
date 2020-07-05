from selenium import webdriver
import time

try:
    # 操作系统为windows，这里使用windows版本的chrome驱动可执行文件
    browser = webdriver.Chrome('/chromeDriver/chromedriver.exe')
    browser.get('https://shimo.im/welcome')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button').click()
    time.sleep(1)
    browser.find_element_by_name('mobileOrEmail').send_keys('15060774157')
    time.sleep(1)
    browser.find_element_by_name('password').send_keys('123456')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()
    time.sleep(5)
    # browser.close()
except Exception as e:
    print(e)
finally:
    browser.close()