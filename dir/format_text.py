#!/usr/bin/env python
# coding: utf-8

import spacy

# import json
import pandas as pd
import emoji
import nagisa
import unicodedata
import re


BASE_PATH = "/home/nb-user/ksl_pub/suggestive_anger/data/fuman_survey"

# # install packages
get_ipython().system("pip install emoji nagisa")
get_ipython().system("pip install -U ginza ja-ginza ja_ginza")
get_ipython().system("python3 -m spacy download ja_core_news_sm")

# # Load Dataset


danwasMap = {
    "並列": 0,
    "対比": 1,
    "要望": 2,
    "条件": 3,
    "原因結果": 4,
    "例提示": 5,
    "詳細化": 6,
    "主題連鎖": 7,
    "焦点主題連鎖": 8,
    "順接": 9,
    "逆接": 10,
    "短文": 11,
    "質問応答": 12,
    "理由": 13,
}
labelsMap = {0: "感情的攻撃", 1: "感情的説得", 2: "理性的説得", 3: "嫌味皮肉", 4: "遠回し", 5: "怒っていない"}

baseData = pd.read_json(BASE_PATH + "/json/human_data_ver5.json")
baseData = baseData.rename(columns={"fulltext": "text", "label": "labels"})
baseData["danwa_result"] = (
    baseData["danwa_result"].map(danwasMap).fillna(3).astype("int64")
)

kushiroData = pd.concat(
    [
        pd.read_csv(BASE_PATH + "/kosen_features.csv"),
        pd.read_csv(BASE_PATH + "/kosen_labels.csv"),
    ],
    axis=1,
)
kushiroData = kushiroData.rename(columns={"feature": "text", "label": "labels"})

baseData = pd.concat([baseData, kushiroData])
baseData = baseData.reset_index(drop=True)  # オリジナルのindexを列として保存しない

print(baseData.labels.value_counts())
baseData


# # Load functions


def extract_emoji(words):
    """
    日本語のテキストから絵文字😉を抽出する
    （顔文字は抽出しない）
    """
    words = str(words)
    return [w for w in words if emoji.is_emoji(str(w))]


# In[9]:

KAOMOJI_LEN = 5


def extract_kaomoji(text):
    """与えられたテキストから抽出した顔文字リストを返却する。
    → ＼(^o^)／, m(_ _)m などの 手を含む顔文字があれば、それも抽出する
    """
    results = nagisa.extract(text, extract_postags=["補助記号"])
    words = results.words
    kaomoji_words = []
    kaomoji_idx = [i for i, w in enumerate(words) if len(w) >= KAOMOJI_LEN]
    kaomoji_hands = ["ノ", "ヽ", "∑", "m", "O", "o", "┐", "/", "\\", "┌"]
    # 顔文字と手を検索
    for i in kaomoji_idx:
        kaomoji = words[i]  # 顔文字列
        try:
            # 顔文字の左手
            if words[i - 1] in kaomoji_hands and 0 < i:
                kaomoji = words[i - 1] + kaomoji
            # 顔文字の右手
            if words[i + 1] in kaomoji_hands:
                kaomoji = kaomoji + words[i + 1]
        except IndexError:
            pass
        finally:
            kaomoji_words.append(kaomoji)
    return kaomoji_words


# In[10]:


# nlp = spacy.load("ja_ginza")
nlp = spacy.load("ja_core_news_sm")


def separate_sentence(feature):
    doc = nlp(feature)
    return [str(sent) for sent in doc.sents]


def delete(text, target_list):
    for target in target_list:
        text = text.replace(target, "")
    return text


# In[11]:


def replace_emoji(sentence):
    return (
        sentence.replace("❗", "!")
        .replace("❓", "?")
        .replace("‼️", "!!")
        .replace("⁉️", "!?")
    )
    # return sentence.replace('❗', '！').replace('❓', '？').replace('‼️', '！！').replace('⁉️', '！？')


def delete_emoji(sentence):
    emoji_list = extract_emoji(sentence)
    if len(emoji_list) == 0:
        return sentence

    for e in emoji_list:
        sentence = sentence.replace(e, "")
    return sentence


def delete_kaomoji(sentence):
    sentence = sentence.replace("　", "").replace(" ", "")

    if "(^^;;" in sentence:
        sentence = sentence.replace("(^^;;", "")

    if "́д`;" in sentence:
        sentence = sentence.replace("́д`;", "")

    kaomoji_list = extract_kaomoji(sentence)
    if len(kaomoji_list) == 0:
        return sentence

    for kaomoji in kaomoji_list:
        """unicode_sentence = unicodedata.normalize('NFKC', sentence)
        print(kaomoji)
        print(unicode_sentence)
        print(kaomoji in unicode_sentence)"""
        sentence = sentence.replace(kaomoji, "")
    return sentence


tilde_pattern = "[\u007E\u02DC\u0303\u1FC0\u2053\u223C\u223F\u3030\uFF5E]"
comma_pattern = r"[､、]{2,}"
full_stop_pattern = r"[｡。]{2,}"
unnecessary_full_stop_pattern = r"([!?]+)[｡。]+"
number_pattern = r"[0-9]+"
compiled_tilde = re.compile(tilde_pattern)
compiled_comma = re.compile(comma_pattern)
compiled_full_stop = re.compile(full_stop_pattern)
compiled_unnecessary = re.compile(unnecessary_full_stop_pattern)
compiled_number = re.compile(number_pattern)


def delete_slash(feature):
    return feature.replace("/", "")


def fix_tilde(feature):
    return compiled_tilde.sub("〜", feature)


def fix_multiple_punctuation(feature):
    return compiled_comma.sub(
        "、", compiled_full_stop.sub("。", compiled_unnecessary.sub(r"\1", feature))
    )


def delete_irregular_str(feature):
    return feature.replace("\uFE0E", "").replace("\uFE0F", "")


def replace_number_to_zero(feature):
    match_list = compiled_number.findall(feature)
    for match_str in match_list:
        feature = feature.replace(match_str, "0")
    return feature


# 文ごとに分けたあとの処理
def fix_bracket(sentences, left_bracket, right_bracket):
    count_left_bracket = sum([s.count(left_bracket) for s in sentences])
    count_right_bracket = sum([s.count(right_bracket) for s in sentences])

    if count_left_bracket == 0 and count_left_bracket == count_right_bracket:
        return sentences

    # print(f'count_left_bracket : {count_left_bracket}')
    sentence_length = len(sentences)
    new_sentences = []
    should_skip = False

    for i in range(sentence_length):
        if should_skip:
            should_skip = False
            continue

        if sentences[i].count(left_bracket) == sentences[i].count(right_bracket):
            new_sentences.append(sentences[i])
            continue

        right_bracket_position = i + 1

        if i != sentence_length - 1 and sentences[right_bracket_position].count(
            left_bracket
        ) != sentences[right_bracket_position].count(right_bracket):
            new_sentences.append(sentences[i] + sentences[right_bracket_position])
            should_skip = True

    return new_sentences


symbol_pattern = r"^[.!?]+"
leader_pattern = r"[.・]{2,}"
end_of_sentence_pattern = r"[。!?]$"
compiled_symbol = re.compile(symbol_pattern)
compiled_leader = re.compile(leader_pattern)
compiled_eos = re.compile(end_of_sentence_pattern)


def join_symbol_only_sentence(sentences):
    sentence_length = len(sentences)
    new_sentences = []
    is_matched = False

    for i in range(sentence_length):
        if is_matched:
            is_matched = False
            continue

        if compiled_symbol.match(sentences[i]) is None or i == 0:
            new_sentences.append(sentences[i])
            continue

        new_sentences[-1] += sentences[i]
        should_skip = True

    return new_sentences


def restore_leader(sentences):
    return [
        compiled_leader.sub("…", sentence)
        if compiled_leader.search(sentence)
        else sentence
        for sentence in sentences
    ]


def delete_sentence_only_symbols(sentences):
    return [s for s in sentences if s != "、"]


def join_sentence_if_start_left_paren(sentences):
    new_sentence = []
    for i, sentence in enumerate(sentences):
        if i == 0:
            new_sentence.append(sentence)
            continue

        if sentence[0] == "(":
            new_sentence[-1] += sentence
        else:
            new_sentence.append(sentence)

    return new_sentence


def fix_end_of_sentence(sentences):
    return [
        sentence if compiled_eos.search(sentence) else sentence + "。"
        for sentence in sentences
    ]


def make_sentences_from_feature(feature):
    sentences = separate_sentence(
        replace_number_to_zero(
            delete_irregular_str(
                fix_multiple_punctuation(
                    fix_tilde(
                        delete_slash(
                            delete_emoji(delete_kaomoji(replace_emoji(feature)))
                        )
                    )
                )
            )
        )
    )
    return fix_end_of_sentence(
        join_sentence_if_start_left_paren(
            delete_sentence_only_symbols(
                restore_leader(
                    join_symbol_only_sentence(
                        fix_bracket(
                            fix_bracket(fix_bracket(sentences, "「", "」"), "『", "』"),
                            "(",
                            ")",
                        )
                    )
                )
            )
        )
    )


# In[13]:


features = []

for i, data in enumerate(baseData.values):
    feature = data[0]
    feature = unicodedata.normalize("NFKC", feature)  # NFKC正規化
    # emoji_list = extract_emoji(feature)
    result = make_sentences_from_feature(feature)
    line_length = len(result)
    sentence = " ".join(result)
    features.append([i, line_length, sentence])  # [index, 文章数, 本文]
    # for sentence_i, sentence in enumerate(result):
    #     # index, 何文章目か, 文章数, 本文
    #     features.append([i, sentence_i, len_result, sentence])
