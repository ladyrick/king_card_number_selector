import requests
import json
import re

from notification import smtp_send
from config import search_values, detailed_values


def number_iter(search_values, stop_iter=0):
    iter = 0
    registerURL = "https://m.10010.com/queen/tencent/fill.html?product=0&channel=1023"
    requestURL = "https://m.10010.com/NumApp/NumberCenter/qryNum"
    headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # "Cookie": "UID=VfEELqc0qOgicLuplcjox6cyVz6JQgMf; gipgeo=11|110; WT_FPC=id=2e95bbbaeb5bea2fcf81542180813946:lv=1546060650016:ss=1546060650012; JSESSIONID=hnf4Zk0oSMeui_9-KCiYHbRG-hy9efOqvOtpnJrvcRoHt-BgBQSh!1997323720; SHOP_PROV_CITY=; TC_CD=e145b3eb-1adf-4b79-a03a-0e996d5164fe; mallcity=11%7C110",
        "Host": "m.10010.com",
        "Referer": registerURL,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {"ACOOKIE": "C8ctADEyMy4xNTEuMTkwLjI4LTgxNDg4NzM5Mi4zMDcwMjU3MwAAAAAAAAACAAAADQAAAKQDJ1ykAydcCAAAAHv5JVx7+SVcAQAAAAEAAACkAydcpAMnXAIAAAAIAAAAIjEyMy4xNTEuNzYuMjM5LTE2NTkxOTQ2ODguMzA3MDI1NzINAAAAITEyMy4xNTEuMTkwLjI4LTgxNDg4NzM5Mi4zMDcwMjU3Mw--",
               "JSESSIONID": "hnf4Zk0oSMeui_9-KCiYHbRG-hy9efOqvOtpnJrvcRoHt-BgBQSh!1997323720",
               "SHOP_PROV_CITY": "",
               "TC_CD": "e145b3eb-1adf-4b79-a03a-0e996d5164fe",
               "UID": "VfEELqc0qOgicLuplcjox6cyVz6JQgMf",
               "WEBTRENDS_ID": "123.151.190.28-814887392.30702573",
               "WT_FPC": "id=2e95bbbaeb5bea2fcf81542180813946:lv=1546060650016:ss=1546060650012",
               "gipgeo": "11|110",
               "mallcity": "11%7C110",
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
        "_": "1546060649894"
    }
    while stop_iter == 0 or iter < stop_iter:
        params["searchValue"] = str(search_values[iter % len(search_values)])
        try:
            res = requests.get(requestURL, headers=headers, params=params, cookies=cookies, timeout=2)
            m = re.match("^jsonp_queryMoreNums\((.*)\);{0,1}$", res.text)
            if not m:
                print(f"iter {iter}: Regexp matching error.")
                continue
            resjson = json.loads(m.group(1))
            numbers = resjson["numArray"][0::12]
            if numbers:
                for n in numbers:
                    print(f"iter {iter}: Candidate: {n}")
                    yield str(n)
            else:
                print(f"iter {iter}: Nothing found.")
        except requests.exceptions.Timeout:
            print(f"iter {iter}: Request time out.")
        except Exception as e:
            print(f"iter {iter}: {str(e)}")
        finally:
            iter += 1


if __name__ == "__main__":
    for number in number_iter(search_values, 0):
        if True in [number.find(dv) != -1 for dv in detailed_values]:
            print(f"Congratulations! {number}")
            smtp_send("king card", number)
        else:
            print(f"Wrong candidate: {number}")
