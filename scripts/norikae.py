'''
現在時刻から直近の乗換案内を検索して、到着時間を表示する
Yahoo乗換から到着時間をスクレイピングで抽出している
'''
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse # URLエンコード、デコード
print('出発駅を入力してください')
startsta = input() # 出発駅
print('到着駅を入力してください')
endsta = input() # 到着駅

startstaen = urllib.parse.quote(startsta) # encode
endstaen = urllib.parse.quote(endsta) # encode

url0 = 'https://transit.yahoo.co.jp/search/result?from='
url1 = '&flatlon=&to='
url2 = '&viacode=&viacode=&viacode=&shin=&ex=&hb=&al=&lb=&sr=&type=1&ws=3&s=&ei=&fl=1&tl=3&expkind=1&ticket=ic&mtf=1&userpass=0&detour_id=&fromgid=&togid=&kw='

url = url0 + startstaen + url1 + endstaen + url2 + endstaen
req = urllib.request.urlopen(url)
html = req.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

time = soup.select("#rsltlst > li > dl > dd > ul > li.time > span.mark") # 到着時間の記載部分を抽出
transfer=soup.select('#rsltlst > li > dl > dd > ul > li.transfer')
station=soup.select('div.station')
access=soup.select('div.access')
print('#','到着時間:'+time[0].contents[0]+'着')
print('#','乗り換え回数:'+transfer[0].contents[2]+'回')
for _ in range(len(station)):
    print('#',station[_].contents[0].contents[0].contents[0],station[_].contents[2].contents[0].contents[0].contents[0])
    if _!=len(station)-1:
        print('#',access[_].contents[0].contents[0].contents[1].contents[1])