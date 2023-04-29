import random

# 数学問題を出す関数
def math_quiz():
    # 2つの数をランダムに選択
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    # どの演算子を使うかをランダムに選択
    operator = random.choice(['+', '-', '×'])
    # 正しい答えを計算
    if operator == '+':
        answer = x + y
    elif operator == '-':
        while(True):
            if x - y>=0:
                answer=x-y
                break
            else:
                x+=random.randint(1, 10)
    else:
        answer = x * y
    # 問題を表示
    print('{} {} {}は?'.format(x, operator, y))
    # プレイヤーが答えを入力
    guess = input('Answer: ')
    # 入力された値が数字かどうかを確認
    if not guess.isnumeric():
        print('数字を言って下さい')
        return
    # 入力された値を整数に変換
    guess = int(guess)
    # 答えが正しいかどうかを確認
    if guess == answer:
        print('正解です')
    else:
        print('答えは', answer)

# 数学問題を10問出題
for i in range(1):
    print('Question', i+1)
    math_quiz()

#完成品