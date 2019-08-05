import re
import sys
import random
# from tkinter import messagebox

def do():
    texts = ["I think so.",
            "Do you play soccer?",
            "Help me, please.",
            "I'm using Python_3.",
            "_Keio is the best university in the world.",
            "I've been (to) America."]

    # texts = []
    # for line in sys.stdin.readlines():
    #     texts.append(line.rstrip())

    for sentence in texts:
        words = sentence.split(" ")
        wordsCount = len(words)
        symbols = []
        hidden = []

        # 頭文字の処理: 'I' => 処理せず '_' => 削除
        firstW = words[0]
        if firstW[0] == '_':
            words[0] = re.sub('_', "", firstW)
        elif firstW != 'I' and firstW != "I'm" and firstW != "I've":
            words[0] = firstW.lower()

        def remake(n, word):
            del_sym = '[.|,|?]'
            # 記号を除去
            reword = re.sub(del_sym, "", word)
            reword = re.sub('_', ' ', reword)
            words[n] = reword
            # 記号をsymbolsリストに格納
            symbol = re.findall(del_sym, word)
            if len(symbol) == 1:
                symbols.append(symbol[0])
            # elif len(symbol) >= 2:
            #     messagebox.showerror('エラー', '記号文字の使い方が正しくありません')
            # 要補足単語リストに追加
            if '(' in word:
                hidden.append(n)

        for (index, word) in enumerate(words):
                remake(index, word)

        # 要補足単語を除去
        dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
        words = dellist(words, hidden)

        rnd_words = random.sample(words, len(words))
        choices = rnd_words + symbols
        choice = '( ' + ' / '.join(choices) + ' )'
        return choice
