import re
import random
import unicodedata

class Reading:  #原文取得
    def __init__(self, texts):
        self.sentences = [line.strip() for line in texts.splitlines() if line != ""]
        self.texts = texts

    def uni(self, str):
        return unicodedata.east_asian_width(str) != 'Na'

    def language(self):
        if self.uni(self.sentences[0][-1]):
            return "OTHER"
        if len(self.sentences) == 1:
            return "ONLY ENG"
        if self.uni(self.sentences[1][-1]):
            return "ENG AND JPN"
        return "ONLY ENG"

    def rtn(self):
        return self.sentences

class Making:
    def __init__(self, sentences):
        self.sentences = sentences

    def en_or_jpn(self, n):
        return [item for index, item in enumerate(self.sentences) if index % 2 == n]

    # 頭文字の処理: 'I' => 処理せず '_' => 削除
    def top(self, words):
        firstW = words[0]
        contracted = ["I", "I'm", "I've", "I'd", "I’m", "I’ve", "I’d" ]
        if firstW[0] == '_':
            words[0] = re.sub('_', "", firstW)
        elif firstW not in contracted:
            words[0] = firstW.lower()
        return words

    def each_word(self, words):
        symbols = []
        hidden = []
        for index, word in enumerate(words):
            del_sym = '[.|,|?|!|!?|?!]'
            # 記号を除去
            no_sym_word = re.sub(del_sym, "", word)
            reword = re.sub('_', ' ', no_sym_word)
            words[index] = reword
            # 記号をsymbolsリストに格納
            symbol = re.findall(del_sym, word)
            if len(symbol) == 1:
                symbols.append(symbol[0])  # symbolリストが空の場合のバグ回避
            # 要補足単語リストに追加
            if '(' in word:
                hidden.append(index)
        return [words, symbols, hidden]

    def grouping(self, sentences):  # 語群作成
        results = []
        for index, sentence in enumerate(sentences):
            splited = self.top(sentence.split(" "))
            remade = self.each_word(splited)
            words_list = remade[0]
            symbols = remade[1]
            hidden = remade[2]

            # 要補足単語を除去
            dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
            words_list = dellist(words_list, hidden)

            rnd_words = random.sample(words_list, len(words_list))
            choices = rnd_words + symbols
            choice = '( {} )'.format(' / '.join(choices))
            results.append(choice)
        return results

class Export:  # 英文日文結合作業
    def combine(self, e, j):
        if len(j) == 0:
            questions = e
        else:
            questions = [j[i] + "　" + e[i] for i in range(len(j))]
        return '\n'.join(questions)

class Export_2(Export):
    def combine(self, e):
        return '\n'.join(e)

# 生成作業
def answer(msg):
    # クラスまとめ
    first = Reading(msg)
    second = Making(first.rtn())
    last = Export()

    if first.language() == "OTHER":
        return "英文を入力してください。\n\n◎入力方法を知りたい場合は「how to use」と送信してください。"
    if first.language() == "ONLY ENG":
        eng = first.rtn()
        group = second.grouping(eng)
        jpn = []
    elif first.language() == "ENG AND JPN":
        eng = second.en_or_jpn(0)
        group = second.grouping(eng)
        jpn = second.en_or_jpn(1)
    else:
        return "入力形式が不適切です。\n\n◎入力方法を知りたい場合は「how to use」と送信してください。"
    return last.combine(group, jpn)

# pushする際はデバック変数に0を代入
デバック = 0
if デバック == 0:
    exit()

with open("textdata.txt", encoding='UTF-8') as f:
    msg = f.read()

print(answer(msg))
