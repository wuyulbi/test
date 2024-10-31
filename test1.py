import httpx
from bs4 import BeautifulSoup
import pandas as pd

url = "https://iftp.chinamoney.com.cn/english/bdInfo/"
try:
    response = httpx.get(url, verify=False)  # 禁用 SSL 验证
    response.raise_for_status()  # 检查请求是否成功
except httpx.HTTPStatusError as e:
    print(f"HTTP Error: {e.response.status_code}")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()
# 解析 HTML 内容
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')  # 假设数据在第一个表格中
headers = [th.get_text(strip=True) for th in table.find_all('th')]
data = []
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    if len(cells) == len(headers):
        row_data = [cell.get_text(strip=True) for cell in cells]
        if row_data[3] == "Treasury Bond" and row_data[4].startswith("2023"):
            data.append(row_data)
df = pd.DataFrame(data, columns=headers)
df_filtered = df[['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating']]
output_file = "treasury_bonds_2023.csv"
df_filtered.to_csv(output_file, index=False, encoding='utf-8-sig')
# 由于网络与时间问题 再三尝试后 无法获取到题目1 网址中的数据 上述仅是考生解题思路


