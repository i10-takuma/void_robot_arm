#!/usr/bin/env python3
import os
import rospy
from robot_arm.srv import Word
from std_msgs.msg import String
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill

client_id = os.environ.get('SPOTIFY_CLIENT_ID', '')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET', '')
redirect_uri = os.environ.get('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
username = os.environ.get('SPOTIFY_USERNAME', '')
scope = 'user-read-playback-state,user-modify-playback-state,playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, 
                                            client_secret=client_secret, 
                                            redirect_uri=redirect_uri, 
                                            scope=scope))

mecab = MeCab.Tagger()
mecab.parse('')
# SVMモデルの読み込み
with open("/home/takuma/catkin_ws/src/robot_arm/scripts/svc/svc.model3","rb") as f:
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

def play_music(text):
    sp.pause_playback()
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text)
    words = []
    noun = 0
    while node:
            next_node = node.next
            # 数字の場合、リストに格納
            if node.feature.split(',')[0] == '名詞':
                words.append(node.surface)
                noun = 1
            elif next_node is not None and next_node.feature.split(',')[0] == '名詞' and noun == 1:
                words.append(node.surface)
            
            if node.feature.split(',')[0] != '名詞':
                noun = 0
            node = node.next
    search_term = ''.join(words)
    #search_type = random.choice(('artist', 'track'))
    #if search_type == 'artist':
    search_term = search_term.replace("の曲", "")
    search_term = search_term.replace("を再生", "")
    print(search_term)
    search_type = 'track'
    result = sp.search(search_term, limit=1, type=search_type)
    track_uri = result['tracks']['items'][0]['uri']
    track_name = result['tracks']['items'][0]['name']
    artist_name = result['tracks']['items'][0]['artists'][0]['name']
    talk(artist_name + "の" + track_name + "を再生します")
    print(result)
    sp.start_playback(uris=[track_uri])
    try:
        print(f"Playing {search_type}: {result['name']}...")
    except:
        pass

# Change volume
def set_volume(volume_percent):
    sp.volume(volume_percent)

# Pause playback
def pause(msg):
    sp.pause_playback()

# start playback
def resume():
    sp.start_playback()

def callback(msg):
    da=extract_da(msg.data)
    command = da
    if command == "artist":
        play_music(msg.data)
    if command == "volume":
        volume = input("set volume 0~100:")
        set_volume(volume)
    if command == "stop":
        pause()
    if command == "start":
        resume()

if __name__ == '__main__':
    rospy.init_node('spotify', anonymous=True)
    rospy.Subscriber('/task/stop', String, pause)
    rospy.Subscriber('/task/spotify', String, callback)
    talk = rospy.ServiceProxy('/text_talk/srv', Word)
    # ノードをループさせる
    rospy.spin()