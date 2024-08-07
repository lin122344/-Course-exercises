from selenium import webdriver   #匯入(inport)操控瀏覽器相關程式
from selenium.webdriver.common.keys import Keys  #操作瀏覽器互動的程式
from selenium.webdriver.common.by import By  #DON tree 搜尋節點的類別集
import time
time.sleep(5)

driver = webdriver.Firefox()  #生成一個由程式操控的Furefox
driver.get("http://www.python.org")  #請瀏覽器幫忙訪問python.org網頁
assert "Python" in driver.title #檢查有沒有錯誤 有錯就會跳錯誤 #檢查分頁是否有包含python 

#https://selenium-python.readthedocs.io/locating-elements.html
elem = driver.find_element(By.NAME, "q")  #等同於BeautifulSoup的find ->去找python的搜尋欄
time.sleep(5)


elem.clear()  #清除搜尋欄
elem.send_keys("pycon") #輸入pycon 到搜尋欄
time.sleep(5)

elem.send_keys(Keys.RETURN)  #按下鍵盤enter
time.sleep(20)

assert "No results found." not in driver.page_source #"No results found"未出現在頁面上
driver.close() # 關掉當前分頁
#driver.quit() #關掉整個模擬瀏覽器

print("Done")