import datetime
from time import sleep
from threading import Thread 
import re
import pytz
from datetime import datetime
import dill
import MeCab
import datetime 
import geocoder
breaker=False
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill
mecab = MeCab.Tagger()
mecab.parse('')

# SVMモデルの読み込み
with open("svc.model6","rb") as f:
    vectorizer = dill.load(f)
    label_encoder = dill.load(f)
    svc = dill.load(f)

# 発話から対話行為タイプを推定    
def extract_da(utt):
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            words.append(word)
    tokens_str = " ".join(words)
    X = vectorizer.transform([tokens_str])
    Y = svc.predict(X)
    # 数値を対応するラベルに戻す
    da = label_encoder.inverse_transform(Y)[0]
    return da

def f(date):
    mt=False
    mh=False
    if re.compile(r"\d{1,2}分").findall(date):
                minutes = int( re.compile(r"\d{1,2}分").findall(date)[0].replace("分",""))
    else:
            mt=True
    if re.compile(r"\d{1,2}時").findall(date):
                hours = int( re.compile(r"\d{1,2}時").findall(date)[0].replace("時",""))
    else:
        mh=True
    if mt==False:
        with open('ararmm.txt' , 'a') as text:
            text.write(str(minutes) + '\n')
    if mh==False:
        with open('ararmt.txt' , 'a') as text:
            text.write(str(hours) + '\n')
def readtimerhlist():
    with open('ararmt.txt','r') as text: 
        textlines=text.readlines() 
        numbers = []
        for element in textlines:
            element = element.strip()  # 先頭と末尾の空白文字を削除する
            if element.isdigit():  # 文字列が数字である場合
                numbers.append(int(element))  # 整数に変換してリストに追加する
        return numbers
def readtimermlist():
     with open('ararmt.txt','r') as text: 
        textlines=text.readlines() 
        numbers = []
        for element in textlines:
            element = element.strip()  # 先頭と末尾の空白文字を削除する
            if element.isdigit():  # 文字列が数字である場合
                numbers.append(int(element))  # 整数に変換してリストに追加する
 
        return numbers


text=input()

mecab = MeCab.Tagger()
mecab.parse('')

# 発話から対話行為タイプを推定    

def convertfalse(intext):
    seconds=0
    try:
        if re.compile(r"\d{1,2}時").findall(intext):
            seconds += int( re.compile(r"\d{1,2}時").findall(intext)[0].replace("時",""))*3600
        if re.compile(r"\d{1,2}分").findall(intext):
            seconds += int(re.compile(r"\d{1,2}分").findall(intext)[0].replace("分",""))*60
        if re.compile(r"\d{1,2}秒").findall(intext):
            seconds += int(re.compile(r"\d{1,2}秒").findall(intext)[0].replace("秒",""))
    except:
        print("e_Message")
    return seconds

def converttrue(intime):
    outtime=(intime//3600*10000)+(intime%3600//60*100)+(intime//3600%60)
    return outtime

def timer(secs):
        for i in range(0,secs):
            sleep(1)
        print("時間です")

def timer2(secs,thing):
        for i in range(0,secs):
            print(secs-i)
            sleep(1)
        print(thing)

def ararm():        
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.datetime.now(jst)
    if((now.hour*60+now.minute)*60+now.second)<convertfalse(text):
        print("")
        thread_2 = Thread(target=timer,args=((now.hour*60+now.minute)*60+now.second-convertfalse(text)))
        thread_2.start()
    else:
        print("時間を入力してください")
        try:
            s=input()
            if((now.hour*60+now.minute)*60+now.second)<convertfalse(s):
                thread_2 = Thread(target=timer,args=((now.hour*60+now.minute)*60+now.second-convertfalse(s)))
                thread_2.start()
        except:
            print("アラームが設定できませんでした")

def world_time(place):
    ret = geocoder.osm(place,timeout=5.0) 
    ido=ret.latlng[1] 
    print(round(ido/15)) 
    world_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=round(ido*240)))) 
    if world_time.strftime('%p') == 'AM': 
        print(world_time.strftime('今の' + place + 'は%Y年%m月%d日午前%I時%M分%S秒です')) 
    else: 
        print(world_time.strftime('今の' + place + 'は%Y年%m月%d日午後%I時%M分%S秒です'))

def settimer():
    print("タイマーをセットします")
    if convertfalse(text)==0:
        print("時間を決定します")
        s=input()
        thread_1 = Thread(target=timer,args=(convertfalse(text),))
        thread_1.start()
    else:
        thread_1 = Thread(target=timer,args=(convertfalse(text),))
        thread_1.start()

if"世界時計"in text:
    world_time(input())
elif "アラーム"in text or "目覚まし"in text:
    if "消し"in text or "止め"in text or "やめ"in text:
        print("アラームを初期化しますか")
        if extract_da(input())=="yes":
            with open("aramm", "w") as file:
                file.write("")  # 空
            with open("aramt", "w") as file:
                file.write("")  # 空
        else:
            print("ありがとうございました")
    else:       
        print('何時にアラームをかけますか')
        f(input())
elif 'タイマー'in text or "間" in text or "測" in text or"計"in text:
    settimer()
elif "時計" in text:
    now = datetime.datetime.now().time()
    if now.strftime('%p') == 'AM':
        print(now.strftime('今は約午前%I時%M分%S秒です'))
    else:
        print(now.strftime('今は約午後%I時%M分%S秒です'))
print("ありがとうございました")
#都市名をめかぶで出せるか調べる、リマインドの部分をメモ帳と一緒に作る、リマインドのジャンル分けのai
print(len(readtimerhlist()))
while(True):
    result = [[readtimerhlist()[i], readtimermlist()[i]] for i in range(len(readtimermlist()))]
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.datetime.now(jst)
    print(now.hour,now.minute)
    print(result[0])
    for i in result:
        print("AAA")
        print(i)
        if now.hour==i[0]and now.minute==i[1]and now.second==0:
            print("時間です")
            breaker=True
            break
    