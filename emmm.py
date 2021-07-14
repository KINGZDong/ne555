from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from playsound import playsound
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
import math
import os


chrome_options = Options()

# 禁止弹窗
prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
# 禁止弹窗加入
chrome_options.add_experimental_option('prefs', prefs)

aimtxt = 'E:/PycharmProjects/ne555/model.txt'
datas = pd.read_table(aimtxt, encoding="utf-8", header=None)

keys = datas.values.tolist()
print(keys)

# implicitly_wait方法
time_start = time.time()
browser1 = webdriver.Chrome(options=chrome_options)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser1.get("https://www.ti.com.cn/ ")
browser1.implicitly_wait(60)

j = 1
for i in range(len(keys)):
    search_name = browser1.find_element_by_xpath("//*[@id='searchboxheader']/div[1]/div/div/div[1]/input")
    search_name.send_keys(keys[i])
    search_button = browser1.find_element_by_xpath("//*[@id='searchboxheader']/div[1]/div/a")
    search_button.click()

    time.sleep(30)
    # js1 = "return document.querySelector('ti-opn-snapshot').shadowRoot.children[0].children[0].children[1].children[0].shadowRoot.children[0].children[0].children[1].children[1].children[0].textContent"
    js1 = 'return document.querySelector("#search > section > div > div.ti_p-col-8.ti_p-col-tablet-12.ti_p-col-phone-12.u-padding-top-xl.ti_search-resilt-container > div > div > div.row.search-extras-section > ti-opn-snapshot").shadowRoot.querySelector("ti-card > div > div.ti-opn-snapshot-opn-match-details > ti-opn-details").shadowRoot.querySelector("div > div > div.ti-opn-details-add-to-cart > ul > li:nth-child(1)").textContent'
    Inventory = browser1.execute_script(js1)
    print(str(keys[i]) + ' ' + str(Inventory))
    inventory = re.sub("\D", "", Inventory)
    if len(inventory) != 0:
        playsound('sound.wav')
        time.sleep(5)
        #############下单############################
        js2 = 'document.querySelector("#search > section > div > div.ti_p-col-8.ti_p-col-tablet-12.ti_p-col-phone-12.u-padding-top-xl.ti_search-resilt-container > div > div > div.row.search-extras-section > ti-opn-snapshot").shadowRoot.querySelector("ti-card > div > div.ti-opn-snapshot-opn-match-details > ti-opn-details").shadowRoot.querySelector("div > div > div.ti-opn-details-add-to-cart > ti-add-to-cart").shadowRoot.querySelector("ti-form-element > ti-input").value="%s"' % math.ceil(int(inventory) * 0.8)
        Number = browser1.execute_script(js2)
        js_clik = 'document.querySelector("#search > section > div > div.ti_p-col-8.ti_p-col-tablet-12.ti_p-col-phone-12.u-padding-top-xl.ti_search-resilt-container > div > div > div.row.search-extras-section > ti-opn-snapshot").shadowRoot.querySelector("ti-card > div > div.ti-opn-snapshot-opn-match-details > ti-opn-details").shadowRoot.querySelector("div > div > div.ti-opn-details-add-to-cart > ti-add-to-cart").shadowRoot.querySelector("ti-button").shadowRoot.querySelector("button").click()'
        browser1.execute_script(js_clik)

        time.sleep(10)
        js_continue = """
        if(document.getElementsByClassName("ti-add-to-cart-dialog-content")) 
        {
          document.querySelector("body > ti-dialog-launcher > ti-dialog > div.ti-add-to-cart-dialog-action > ti-button.ti-button-primary.hydrated > a").click()
        }
        """
        browser1.execute_script(js_continue)

        js_check = 'document.querySelector("#add_to_cart_modal_checkout > a").click()'
        browser1.execute_script(js_check)
        time.sleep(2)

        if (j == 1):
            js_email = """
                let email = document.querySelector("#username").shadowRoot.querySelector("input[type=text]");
                email.value = "2533410138@qq.com"
                var event = document.createEvent("HTMLEvents");
                event.initEvent("input",true,true);
                event.eventType="message";
                email.dispatchEvent(event);

                """

            browser1.execute_script(js_email)
            time.sleep(2)
            js_next = 'document.querySelector("#nextbutton").shadowRoot.querySelector("button").click();'
            browser1.execute_script(js_next)
            print("密码")
            input()
            j = j + 1
            time.sleep(5)
            select = Select(browser1.find_element_by_id("llc-cartpage-ship-to-country"))  # 实例化select
            select.select_by_value('CN')  # 选择第1项选项：value='0'
            browser1.find_element_by_xpath('//*[@id="llc-cartpage-ship-to-continue"]').click()
            time.sleep(10)
            print(str(keys[i]) + ' 下单: ' + str(math.ceil(int(inventory) * 0.8)))
            #browser1.find_element_by_xpath('//*[@id="ab_widget_container_popin-simple_fef801d3_686831"]/div[2]/button').click()
            # browser1.find_element_by_xpath('//*[@id="tiCartCalculate_Continue"]').click()
        else:
            time.sleep(10)
            # browser1.find_element_by_xpath('//*[@id="ab_widget_container_popin-simple_fef801d3_686831"]/div[2]/button').click()
            # browser1.find_element_by_xpath('//*[@id="tiCartCalculate_Continue"]').click()
            print(str(keys[i])+'下单'+str(math.ceil(int(inventory) * 0.8)))
    browser1.find_element_by_xpath("//*[@id='searchboxheader']/div[1]/div/div/div[1]/input").clear()
    # try:
    #     browser1.find_element_by_xpath('//*[@id="ab_widget_container_popin-simple_fef801d3_686831"]/div[2]/button').click()
    #     browser1.find_element_by_xpath("//*[@id='searchboxheader']/div[1]/div/div/div[1]/input").clear()
    # except:
    #     browser1.find_element_by_xpath("//*[@id='searchboxheader']/div[1]/div/div/div[1]/input").clear()





# search_name = browser1.find_element_by_xpath("//*[@id='searchboxheader']/div[1]/div/div/div[1]/input")
# search_name.send_keys('ne555p')
# search_button = browser1.find_element_by_xpath("//*[@id='searchboxheader']/div[1]/div/a")
# search_button.click()
#
# time.sleep(20)
# #js1 = "return document.querySelector('ti-opn-snapshot').shadowRoot.children[0].children[0].children[1].children[0].shadowRoot.children[0].children[0].children[1].children[1].children[0].textContent"
# js1 = 'return document.querySelector("#search > section > div > div.ti_p-col-8.ti_p-col-tablet-12.ti_p-col-phone-12.u-padding-top-xl.ti_search-resilt-container > div > div > div.row.search-extras-section > ti-opn-snapshot").shadowRoot.querySelector("ti-card > div > div.ti-opn-snapshot-opn-match-details > ti-opn-details").shadowRoot.querySelector("div > div > div.ti-opn-details-add-to-cart > ul > li:nth-child(1)").textContent'
# Inventory = browser1.execute_script(js1)
# print(Inventory)
# inventory = re.sub("\D","",Inventory)
# print(inventory)
#
# time.sleep(5)
# #############下单############################
# js2 = 'document.querySelector("#search > section > div > div.ti_p-col-8.ti_p-col-tablet-12.ti_p-col-phone-12.u-padding-top-xl.ti_search-resilt-container > div > div > div.row.search-extras-section > ti-opn-snapshot").shadowRoot.querySelector("ti-card > div > div.ti-opn-snapshot-opn-match-details > ti-opn-details").shadowRoot.querySelector("div > div > div.ti-opn-details-add-to-cart > ti-add-to-cart").shadowRoot.querySelector("ti-form-element > ti-input").value="%s"'%(int(inventory))
# Number = browser1.execute_script(js2)
# js_clik = 'document.querySelector("#search > section > div > div.ti_p-col-8.ti_p-col-tablet-12.ti_p-col-phone-12.u-padding-top-xl.ti_search-resilt-container > div > div > div.row.search-extras-section > ti-opn-snapshot").shadowRoot.querySelector("ti-card > div > div.ti-opn-snapshot-opn-match-details > ti-opn-details").shadowRoot.querySelector("div > div > div.ti-opn-details-add-to-cart > ti-add-to-cart").shadowRoot.querySelector("ti-button").shadowRoot.querySelector("button").click()'
# browser1.execute_script(js_clik)
#
# time.sleep(10)
# js_check = 'document.querySelector("#add_to_cart_modal_checkout > a").click()'
# browser1.execute_script(js_check)
# print('bingo!')
#
# time.sleep(2)
# js_email = """
# let email = document.querySelector("#username").shadowRoot.querySelector("input[type=text]");
# email.value = "2533410138@qq.com"
# var event = document.createEvent("HTMLEvents");
# event.initEvent("input",true,true);
# event.eventType="message";
# email.dispatchEvent(event);
#
# """
# browser1.execute_script(js_email)
# time.sleep(2)
# js_next = 'document.querySelector("#nextbutton").shadowRoot.querySelector("button").click();'
# browser1.execute_script(js_next)




# js_nextbutton = """
# let pass = document.querySelector("#password").shadowRoot.querySelector("div > input[type=password]");
# pass.value = '123456890';
# var event = document.createEvent('KeyboardEvent');
#     event.initEvent("input", true, true);
#     event.eventType = 'keypress';
#     pass.dispatchEvent(event);
# """
# browser1.execute_script(js_nextbutton)
# nestbutton = browser1.find_element_by_class_name('ti-password-input')
# nestbutton.send_keys('2345')
# nestbutton.click()
# print('bingo!')
################################################
# password = browser1.find_element_by_id('password')
# password.send_keys('Ba15297973418!')
# login = browser1.find_element_by_xpath("//*[@id='app']/section/div/div/div/div[2]/form/div/div[5]/button")
# login.click()
# read = browser1.find_element_by_xpath("//*[@id='popup-ann-modal']/div/div/div[3]/button")
# read.click()
# sign_in = browser1.find_element_by_xpath("//*[@id='checkin-div']")
# sign_in.click()
# browser1.close()
time_end = time.time()
print('time cost', time_end-time_start, 's')
#############  time cost 28.579349517822266 s  ##############

