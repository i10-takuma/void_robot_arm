import re
text=input("生年月日を入力してください")
def convertfalse(intext):
    seconds=1
    try:
        if re.compile(r"\d{1,2}年").findall(intext):
            seconds *= int( re.compile(r"\d{1,2}年").findall(intext)[0].replace("年",""))
        if re.compile(r"\d{1,2}月").findall(intext):
            seconds *= int( re.compile(r"\d{1,2}月").findall(intext)[0].replace("月",""))
        if re.compile(r"\d{1,2}{日").findall(intext):
            seconds *= int( re.compile(r"\d{1,2}日").findall(intext)[0].replace("日",""))
    except:
        print("e_Message")
    seconds%=7
    return seconds
resultint=convertfalse(text)
if resultint==0:
    print("仕事運は少し不安定です。")
if resultint==1:
    print("欲しいものを手に入れることができるかもしれません。")
if resultint==2:
    print("今、自分に自信を持つべき時です。")
if resultint==3:
    print("新しい出会いがあるかもしれません。")
if resultint==4:
    print("大きなチャンスが訪れるかもしれません。")
if resultint==5:
    print("今日は良いことが起こるでしょう。")
if resultint==6:
    print("健康面には気を付けてください。")

#完成