import requests

def getApiKey():
    # Checks the text file for a username/password combination.
    try:
        api = open("info/api.txt", "r")
        return api.read()
    except FileNotFoundError:
        print("getApiKey Error in file service.py")
        return False
    
def searchAQI(dataId, conditions):
    API=getApiKey()
    print(conditions)
    url='https://data.epa.gov.tw/api/v2/{dataID}?format={format}&offset={offset}&limit={limit}&api_key={apiKey}&filters={filtersValue}'.format(
        dataID=dataId,
        format="json", # json, xml, csv
        offset="0", # 第0筆
        limit="10",
        apiKey=API,
        filtersValue=conditions
    )
    x=requests.get(url)
    return x.text

# 資料集代碼:https://data.epa.gov.tw/dataset
# dataId="AQX_P_488"
# 條件查詢方式是使用filters參數加在API網址後:&filters='{資料字典英文欄位}',EQ,'{搜尋值}‘
# EQ、LT、LE、GR、GT(EQ表示等於; LT表示小於;LE表示小於等於;GR表示大於等於;GT表示大於)
# 舉例: &filters=SiteName,EQ,馬公,金門|status,EQ,普通|datacreationdate,GR,2022-02-06 09:00:00|datacreationdate,LE,2022-02-10 23:00:00
# 加入欄位：&fields=sitename,aqi,status,datacreationdate
# 加入排序：&sort=ImportDate desc

# x = requests.get(url)
# print(x.status_code)
# print(x.text)