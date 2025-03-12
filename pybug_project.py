from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

service = Service('D:\\python\\MicrosoftWebDriver.exe')
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Edge(service=service, options=options)

# 假设这是你要抓取的页面
url = "http://218.12.43.28:2018/GouZBT2021To23/pub/gongshi"
driver.get(url)

# 打开文件，准备追加数据
with open('output.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 核心代码（根据实际结构调整选择器）
        target_div = soup.select_one("div.c-table.c-table--fit")  # 通过 class 定位目标 div（按实际 class 名称修改）
        table = target_div.select_one("table")  # 选择 div 内的 table

        # 提取 table 中的数据
        rows = table.select("tbody tr")
        data = []
        for row in rows:
            cols = row.select("td div")
            row_data = [col.text.strip() for col in cols]
            data.append(row_data)

        # 将数据写入文件
        writer.writerows(data)

        # 尝试找到并点击翻页链接
        try:
            # 先选择包含 a 标签的 div
            pagination_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagerItem"))
            )
            # 再选择 a 标签
            next_button = pagination_div.find_element(By.CSS_SELECTOR, "a > i.mdi.mdi-chevron-right").find_element(By.XPATH, "..")
            if next_button and "disabled" not in next_button.get_attribute("class"):
                next_button.click()
                # 等待新页面加载完成
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(pagination_div)
                )
            else:
                break  # 如果链接不可点击，退出循环
        except Exception as e:
            print(f"Error: {e}")
            break

# 关闭浏览器
driver.quit()