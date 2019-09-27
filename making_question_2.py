import re
import random
import unicodedata

class Reading:  #原文取得
    def __init__(self, texts):
        self.sentences = [line.strip() for line in texts.splitlines() if line != ""]
        self.texts = texts
        print(self.sentences)

    def language(self):
        def uni(str):
            return unicodedata.east_asian_width(str) != 'Na'
        if uni(self.texts[0]):
            return "OTHER"
        elif len(self.sentences) == 1:
            return "EE"
        elif uni(self.sentences[1][-1]):
            return "EJ"
        else:
            return "EE"

    def rtn(self):
        return self.sentences

class Making:
    def __init__(self, sentences):
        self.sentences = sentences

    def en_divid(self, n):
        return [item for index, item in enumerate(self.sentences) if index % 2 == n]

    def do(self, sentences):  # 語群作成
        results = []
        for index, sentence in enumerate(sentences):
            words_list = sentence.split(" ")
            symbols = []
            hidden = []

            # 頭文字の処理: 'I' => 処理せず '_' => 削除
            def top(words):
                firstW = words[0]
                contracted = ["I", "I'm", "I've", "I'd", "I’m", "I’ve", "I’d" ]
                if firstW[0] == '_':
                    words[0] = re.sub('_', "", firstW)
                elif firstW not in contracted:
                    words[0] = firstW.lower()
                return words

            def remake(n, word):
                del_sym = '[.|,|?|!|!?|?!]'
                # 記号を除去
                reword = re.sub(del_sym, "", word)
                reword = re.sub('_', ' ', reword)
                words_list[n] = reword
                # 記号をsymbolsリストに格納
                symbol = re.findall(del_sym, word)
                if len(symbol) == 1: symbols.append(symbol[0])  # symbolリストが空の場合のバグ回避
                # 要補足単語リストに追加
                if '(' in word: hidden.append(n)

            words_list = top(words_list)
            for index, word in enumerate(words_list): remake(index, word)

            # 要補足単語を除去
            dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
            words_list = dellist(words_list, hidden)

            rnd_words = random.sample(words_list, len(words_list))
            choices = rnd_words + symbols
            choice = '( ' + ' / '.join(choices) + ' )'
            results.append(choice)
        return results

    def jpn(self):  # 日本語リスト作成
        return [sentence for index, sentence in enumerate(self.sentences) if index % 2 == 1]

class Export:  # 英文日文結合作業
    def combine(self, e, j = []):
        if len(j) == 0:
            questions = e
        else:
            questions = [Jpn + "　" + e[num] for num, Jpn in enumerate(j)]

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
    elif first.language() == "EE":
        group = second.do(first.rtn())
        return last.combine(group)
    elif first.language() == "EJ":
        eng = second.en_divid(0)
        group = second.do(eng)
        jpn = second.en_divid(1)
        return last.combine(group, jpn)
    else:
        return "入力形式が不適切です。\n\n◎入力方法を知りたい場合は「how to use」と送信してください。"

# with open("textdata2.txt", encoding='UTF-8') as f:
#     msg = f.read()
# print(answer(msg))
