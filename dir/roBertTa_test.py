#!/usr/bin/env python
# coding: utf-8

import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

ja_models = ["nlp-waseda/roberta-base-japanese","nlp-waseda/roberta-large-japanese","nlp-waseda/roberta-large-japanese-seq512"]
ja_model = ja_models[1]

tokenizer =    AutoTokenizer.from_pretrained(ja_model)
model = AutoModelForMaskedLM.from_pretrained(ja_model)


# In[ ]:


# maskされたトークン位置を取得する
def get_masked_index(encoding):
    for idx, id in enumerate(encoding.input_ids.squeeze(0)):
        if id == tokenizer.mask_token_id:
            return idx

# 入力系列の処理
sentence = '日本 語 の 自然 言語 処理 は [MASK] 。'
encoding = tokenizer(sentence, return_tensors='pt')

# 予測
pred = model(**encoding)

# 後処理(取得した予測分布から、maskトークンの上位k件の予測結果を取得)
masked_idx = get_masked_index(encoding)
target_probs = pred.logits.squeeze(0)[masked_idx]

# 上位k件の予測結果をのindexを取得
top_k = torch.topk(target_probs, k=5).indices
for id in top_k:
    print(sentence.replace("[MASK]", f"'{tokenizer.decode(id)}'"))
# 日本 語 の 自然 言語 処理 は '得意' 。
# 日本 語 の 自然 言語 処理 は 'できる' 。
# 日本 語 の 自然 言語 処理 は '専門' 。
# 日本 語 の 自然 言語 処理 は 'ない' 。
# 日本 語 の 自然 言語 処理 は '苦手' 。


# In[ ]:


output.show()


# In[ ]:




