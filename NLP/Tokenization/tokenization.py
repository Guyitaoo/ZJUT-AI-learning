import pandas as pd
import os
import dictionary_based as db
# 1. 读取Excel文件
#df = pd.read_excel(os.path.join(os.path.dirname(__file__), 'minidata.xlsx'))
#print(df)

Dictionary = ["我","来到","杭州","浙江","工业","大学","选工","大有","底气","工大","有底气","业大"] 
Sentence = "我来到杭州浙江工业大学,选浙工大有底气" 
print(db.FMM(Sentence, Dictionary))
