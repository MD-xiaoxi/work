from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import csv

service = Service('D:\\python\\MicrosoftWebDriver.exe')
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Edge(service=service,options=options)

# 假设这是你要抓取的页面
url = "http://218.12.43.28:2018/GouZBT2021To23/pub/gongshi"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 核心代码（根据实际结构调整选择器）
target_div = soup.select_one("div.c-table.c-table--fit")  # 通过 class 定位目标 div（按实际 class 名称修改）
table = target_div.select_one("table")  # 选择 div 内所有 li 下的 a 标签


rows = table.select("tbody tr")
data = []
for row in rows:
    cols = row.select("td div")
    row_data = [col.text.strip() for col in cols]
    data.append(row_data)

# 提取文本
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    print(data)
    writer.writerows(data)

driver.quit()