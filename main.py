from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from fake_useragent import UserAgent
from playsound import playsound
import pandas as pd
import time
import re
import smtplib
from email.mime.text import MIMEText

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
# 隐藏 正在受到自动软件的控制 这几个字
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
ua = UserAgent()
user_agent = ua.random
print(user_agent)
chrome_options.add_argument(f'user-agent={user_agent}')
# implicitly_wait方法
browser1 = webdriver.Chrome(options=chrome_options)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser1.implicitly_wait(60)
browser1.maximize_window()
# 修改 webdriver 值
browser1.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})
aimtxt = 'model.txt'
finaltxt = 'final.txt'

datas = pd.read_table(aimtxt, encoding="GBK", header=None)

KEYS = datas.values.tolist()
print(KEYS)

time_start = time.time()


def send_mail(subject, url):
    msg_from = '161983374@qq.com'  # 发送方邮箱
    passwd = 'yybemuygyoojbgeb'  # 填入发送方邮箱的授权码
    msg_to = '2557833850@qq.com'  # 收件人邮箱

    # subject = "有"  # 主题
    content = url  # 正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("邮件发送成功")

    except(s.SMTPException):
        print("邮件发送失败")

    finally:
        s.quit()


def search(keys):
    for i in range(len(keys)):
        url = "https://www.ti.com/store/ti/en/p/product/?p=" + str(keys[i][0])
        try:
            browser1.get(url)
            time.sleep(20)
        except:
            print(str(keys[i][0]) + '对应网站的网站打开失败，请检查网络连接！')
            browser1.quit()
        else:
            if i == 0:
                select = Select(browser1.find_element_by_id("llc-cartpage-ship-to-country"))  # 实例化select
                select.select_by_value('CN')  # 选择第1项选项：value='0'
                browser1.find_element_by_xpath('//*[@id="llc-cartpage-ship-to-continue"]').click()
                time.sleep(20)
            try:
                js1 = 'return document.querySelector("#inventoryDiv > span").textContent'
                Inventory = browser1.execute_script(js1)
            except:
                print(str(keys[i][0]) + ': 未检索到库存数量，')
            else:
                inventory = re.sub("\D", "", Inventory)
                number = str(Inventory).replace('\n', '').replace('\r', '')
                if len(inventory) != 0:
                    if int(inventory) > 100:
                        playsound('sound.wav')
                        print(str(keys[i][0]) + ': 库存数量大于100,库存为: ' + number)
                        subject = str(keys[i][0]) + '库存数量大于100'
                        send_mail(subject, url)

                    else:
                        print(str(keys[i][0]) + ': 库存数量小于100,库存为: ' + number)

            finally:
                textcontent = browser1.find_element_by_xpath('//*[@id="addToCartForm"]/div[1]/div/div[1]').text
                if textcontent == 'Out of stock':
                    print('且库存信息为: Out of stock')
                elif textcontent.replace('\n', '').replace('\r', '') == 'Unavailable':
                    playsound('sound.wav')
                    print('但库存信息为: Unavailable')
                    subject = str(keys[i][0]) + '库存信息为Unavailable'
                    send_mail(subject, url)
                else:
                    print(textcontent)

while True:
    search(KEYS)
