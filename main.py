import requests
import json

from notification import smtp_send
from config import search_values, detailed_values


def number_iter(search_values, stop_iter=0):
    iter = 0
    registerURL = "https://m.10010.com/queen/tencent/fill.html?product=0&channel=67"
    requestURL = "https://m.10010.com/NumApp/NumberCenter/qryNum"
    headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "m.10010.com",
        "Referer": "https://m.10010.com/queen/tencent/fill.html?product=0&channel=67",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    params = {
        "callback": "jsonp_queryMoreNums",
        "provinceCode": "11",
        "cityCode": "110",
        "monthFeeLimit": "0",
        "groupKey": "85236889",
        "searchCategory": "3",
        "net": "01",
        "amounts": "200",
        "codeTypeCode": "",
        "qryType": "02",
        "goodsNet": "4",
        "_": "1545983414272"
    }
    while stop_iter == 0 or iter < stop_iter:
        params["searchValue"] = str(search_values[iter % len(search_values)])
        try:
            res = requests.get(requestURL, headers=headers, params=params, timeout=1)
            resjson = json.loads(res.text[20:-1])
            numbers = resjson["numArray"][0::12]
            if numbers:
                for n in numbers:
                    print(f"iter {iter}: Candidate: {n}")
                    yield str(n)
            else:
                print(f"iter {iter}: Nothing found.")
        except Exception as e:
            print(f"iter {iter}: Request time out.")
        finally:
            iter += 1


if __name__ == "__main__":
    for number in number_iter(search_values, 0):
        if True in [number.find(dv) != -1 for dv in detailed_values]:
            print(f"Congratulations! {number}")
            smtp_send(number)
        else:
            print(f"Wrong candidate: {number}")
