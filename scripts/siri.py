#!/usr/bin/env python3
import rospy
from robot_arm.srv import Word
from std_msgs.msg import String
import pykakasi
import random
import requests
from bs4 import BeautifulSoup 
import time

def is_valid_word(word):
    url='https://dictionary.goo.ne.jp/word/' + word + '/'
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    if '<h1>お探しの情報は見つかりませんでした。</h1>' in str(soup):
        return False
    else:
        return True

def dakuonn(a):
    j={
        'ガ':'カ','ギ':'キ','グ':'ク','ゲ':'ケ','ゴ':'コ','ザ':'サ','ジ':'シ','ズ':'ス','ゼ':'セ','ゾ':'ソ','ダ':'タ','ヂ':'チ','ヅ':'ツ',
        'デ':'テ','ド':'ト','バ':'ハ','パ':'ハ','ビ':'ヒ','ブ':'フ','プ':'フ','ピ':'ヒ','ペ':'ヘ','ベ':'ヘ','ポ':'ホ','ボ':'ポ'
    }
    if a in j:
        return j[a]
    else:
        return a

def owari(a):
    boinn={'a':'ア','i':'イ','u':'ウ','e':'エ','o':'オ'}
    small={'ャ':'ヤ','ュ':'ユ','ョ':'ヨ'}
    if a[-1]=='ッ':
        return dakuonn(a[-3])
    elif a[-1]=='ー':
        jj=pykakasi.kakasi().convert(a)
        kana=''
        for aa in jj:
            kana+=aa['hepburn']
        return boinn[kana[-1]]
    elif a[-1]=='ュ' or a[-1]=='ャ' or a[-1]=='ョ':
        return small[a[-1]]
    else:
        return dakuonn(a[-1])

def callback(msg):
    kks=pykakasi.kakasi()
    log=[]
    finish=False
    with open('/home/takuma/catkin_ws/src/robot_arm/scripts/srtr_words.txt') as a:
        list = a.read().split(',')
    random.shuffle(list)
    words_list = [item.replace("'", "") for item in list]
    keywords = ["止めて", "終わ", "終了", "停止"]
    print('しりとりを開始します。最初は「しりとり」からです')
    respons = talk('しりとりを開始します。最初は、しりとり、からです')
    print('しりとり')
    talk('しりとり')
    coms_word='しりとり'
    log.append('しりとり')
    coms_kana='シリトリ'
    turn = 1
    while True:
        while True:
            word=get_reply('')
            players_word = word.back
            if players_word == "":
                talk("返答が無かったため、しりとりを終了します。結果は" + str(turn) +"ターン目でした")
                players_word = ""
                break
            for word in players_word.split():
                if word in keywords:
                    talk("しりとりを終了します。結果は" + str(turn) +"ターン目でした")
                    players_word = ""
                    break
            print('プレイヤー：' + players_word)
            players_kana=''
            coms_kana=''
            for b in kks.convert(players_word):
                players_kana+=b['kana']
            for b in kks.convert(coms_word):
                coms_kana+=b['kana']
            if dakuonn(players_kana[0])!=owari(coms_kana):
                print(dakuonn(players_kana[0]) + ":" + owari(coms_kana)) 
                print('前の単語の終わりの文字から始まる単語にしてください')
                talk('前の単語の終わりの文字から始まる単語にしてください')
                continue
            elif is_valid_word(players_word)==False:
                print('この単語は存在しません')
                talk('この単語は存在しません')
                continue
            elif players_word in log:
                print('同じ単語は使えません')
                talk('同じ単語は使えません')
                continue
            elif players_kana[-1]=='ン':
                print(str(turn) +'ターン目で私の勝ち！ 何で負けたか、明日まで考えといてください。')
                talk(str(turn) +'ターン目で私の勝ち！ 何で負けたか、明日まで考えといてください。')
                finish=True
                break
            else:
                log.append(players_word)
                break
        if finish:
            break
        count=0
        for a in words_list:
            coms_kana=''
            for b in kks.convert(a):
                coms_kana+=b['kana']
            if coms_kana and dakuonn(coms_kana[0])==owari(players_kana) and coms_kana[-1]!='ン':
                break
            else:
                count+=1
        
        if count==len(words_list):
            print(str(turn) +'ターン目であなたの勝ちです！')
            talk(str(turn) +'ターン目であなたの勝ちです！')
            break
        
        if players_word == "":
            break
        print('Boid：' + words_list[count])
        talk(words_list[count])
        turn +=1
        print('ターン数：' + str(turn))
        coms_word=words_list[count]
        words_list.remove(coms_word)

if __name__ == '__main__':
    rospy.init_node('shiritori', anonymous=True)
    talk = rospy.ServiceProxy('/text_talk/srv', Word)
    get_reply = rospy.ServiceProxy('/greco/reply', Word) #サービスを定義
    rospy.Subscriber('/task/shiritori', String, callback)
    # ノードをループさせる
    rospy.spin()