import re
from datetime import datetime


def reg_search(text, regex_list):
    results = []
    # 遍历每一个包含字段和对应正则表达式的字典
    for regex_dict in regex_list:
        result = {}
        for field, pattern in regex_dict.items():
            if field == '标的证券':
                match = re.search(r'股票代码：(\d+\.\w+)', text)
                result[field] = match.group(1) if match else None
            elif field == '换股期限':
                # 匹配两个日期
                date_matches = re.findall(r'(\d{4}\s*年\s*\d+\s*月\s*\d+\s*日)', text)
                # 将日期转换为 YYYY-MM-DD 格式
                if date_matches:
                    formatted_dates = []
                    for date_str in date_matches:
                        date_str = date_str.replace(" ", "")
                        date_obj = datetime.strptime(date_str, "%Y年%m月%d日")
                        formatted_dates.append(date_obj.strftime("%Y-%m-%d"))
                    result[field] = formatted_dates
        results.append(result)
    return results

# 测试
text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2 日至 2027 年 6 月 1 日止。
'''
regex_list = [{
    '标的证券': '*自定义*',
    '换股期限': '*自定义*'
}]
print(reg_search(text, regex_list))



