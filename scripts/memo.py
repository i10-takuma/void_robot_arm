
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill
import re

_=False
tf1=False
text=input()
mecab = MeCab.Tagger()
mecab.parse('')  

def writefile(filename,intxt):
    with open(filename, 'a') as f:
        f.write(intxt,"\n")

def readfile(filename,getdown):
    with open(filename, 'r') as f:
        lines = f.readlines()
    b=""
    for line in lines:
        if getdown==True:
            b += line.strip()
        if getdown==False:
            b += line
    return b
#allfiles,allwrites

def makelist(filename):
    b="["
    unnamed1=False
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        b+="'"
        b += line.strip()
        b+="'"
        b+=","
        unnamed1=True
    b+="]"
    if unnamed1==True:
        b = b[:-2] + b[-1]
    print(b)
    return b

def extract_da(utt):
    with open("svc.model6","rb") as f:
        vectorizer = dill.load(f)
        label_encoder = dill.load(f)
        svc = dill.load(f)
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

def extract_da2(utt):
    with open("svc.model6","rb") as f:
        vectorizer = dill.load(f)
        label_encoder = dill.load(f)
        svc = dill.load(f)
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
da=(text)

def writetxtdef2(infile,intxt):
    writefile("allfiles",infile)
    f=open(infile,"a")
    f.write(intxt)

def writetxtdef1(infile):
    #正規表現を使い並べる
    print("メモする内容を教えてください。")
    unnamed1=input()
    try:
        writetxtdef2(infile,unnamed1)
        print("記入しました")
    except:
        print("記入に失敗しました。")


def deletetxtdef(infile,intxt):

    with open(infile, encoding="cp932") as f:
        data_lines = f.read()

    # 文字列置換
    data_lines = data_lines.replace(intxt, '')

    # 同じファイル名で保存
    with open(infile, mode="w", encoding="cp932") as f:
        f.write(data_lines)

def writetxt():
    print("どれにメモしますか")
    filename=input()
    unnamed4=False
    for d in makelist("allfiles.txt"):
        if d in filename or filename in d:
            writetxtdef1(d)
            unnamed4=True
    if unnamed4==False:
        
        print("ファイルが見つかりませんでした。現在作成されているファイルは以下の通りです。新しく作成しますか。")
        print(readfile("allfiles.txt",True))
        da=extract_da(input())
        #正規表現を使い並べる
        if (da=="yes"):
            print("ファイル名を入力してください")
            unnamed2=input()
            for file in makelist("allfiles.txt"):
                if file in unnamed2 or unnamed2 in file:
                    writetxtdef1(file)
        else:
            print("現存のファイルに記入しますか")
            da=extract_da
            if (da=="yes"):
                print("ファイルを選んでください")
                print(readfile("allfiles.txt",True))
                unnamed2=input()
                for file in makelist("allfiles.txt"):
                    if file in unnamed2 or unnamed2 in file:
                        writetxtdef1(file)
                else:
                    for i in makelist("allfiles.txt"):
                        if i in unnamed2:
                            print(i,"このファイルで合っていますか")
                            extract_da(input())
                            if da=="yes":
                                writetxtdef1(i)
                            else:
                                print("申し訳ありませんメモはできません")
            else:
                print("新しくファイルを作成します")
                print("ファイル名を入力してください")
                writetxtdef1(input())

def remind():
    print("リママインダーを設定します")
    
    #時計の機能併せて作る

def deletetxt():
    print("ファイル名を入力してください")
    filename=input()
    for i in makelist("allfile.txt"):
        if i in filename or filename in i:
            print("選択されたファイルは",i,"です。削除したい文章を入力してください")
            deletetxtdef(filename,input())
    else:
        print("ファイルが見つかりませんでした。現在作成されているファイルは以下の通りです。この中に削除したい文章の含まれるファイルはありますか")
        print(readfile("allfiles.txt",True))
        da=extract_da(input())
        #正規表現を使い並べる
        if (da=="yes"):
            print("ファイル名を入力してください")
            unnamed=input()
            if i in unnamed:
                deletetxtdef(unnamed)
        else:
            print("現存のファイルに記入しますか")
            if extract_da(input())=="yes":
                print("ファイルを選んでください")
                for i in makelist("allfile.txt"):
                    if i in filename or filename in i:
                        print(i," このファイルで合っていますか")
                        if extract_da(input())=="yes":
                            print("選択されたファイルは",i,"です。削除したい文章を入力してください")
                            deletetxtdef(filename,input())
                    else:
                        print("ファイルが見つかりませんでした")

def changetxt():
    print("どのファイルを変更しますか")
    print(readfile("allfiles.txt",True))
    for i in makelist("allfile.txt"):
        unnamed3=input()
        if i in unnamed3 or unnamed3 in i:
            print(i," このファイルで合っていますか")
            if extract_da(input())=="yes":
                print("選択されたファイルは",i,"です。変更したい文章を入力してください")
                print(readfile,True)
                deletetxtdef(i,input())
        else:
            print("ファイルが見つかりませんでした")
    
command=da


if command=="memo":
    writetxt()
if command=="sakuzyo":
    deletetxt()
if command=="change":
    changetxt()
if command=="AAAAAAAAAAAAAAAAAAAAAAA":
    remind()


#ジャンル分けを作る
#関数でファイルをのぞけるようにしてリマインダーで使う
#構想が足りない
#リマインダーはここに作る
writetxt()