"""
基于词典的词汇切分方法
特点：速度快效率高，但受制于词典质量，不能处理歧义问题
基本原理：每次从句子中切分出尽可能长的词语
包含两种算法：
1. FMM 正向最大匹配法 Forward Maximum Matching :从待切分的句子的最左边开始
2. BMM 逆向最大匹配法 Backward Maximum Matching :从待切分的句子的最右边开始
统计数据表明，逆向最大匹配算切分的正确率高于正向最大匹配算法
"""
Dictionary = ["我","来到","杭州","浙江","工业","大学","选工","大有","底气","工大","有底气","业大"] 
Sentence = "我来到杭州浙江工业大学,选工大有底气"

# 1、FMM
def FMM(sentence, dic):
    result = []
    #获取字典中最长的词语长度
    max_word_length = len(max(dic, key=len))
    while sentence:
        # 当前匹配窗口大小
        match_size = min(len(sentence), max_word_length)
        matched = False
        # 尝试从最大长度开始匹配
        for length in range(match_size, 0, -1):
            word = sentence[:length]
            if word in dic:
                result.append(word)
                sentence = sentence[length:]
                matched = True
                break
        # 如果没有匹配到任何词，则切分单个字符
        if not matched:
            result.append(sentence[0])
            sentence = sentence[1:]
    return result

# 2、BMM
def BMM(sentence, dic):
    result = []
    #获取字典中最长的词语长度
    max_word_length = len(max(dic, key=len))
    while sentence:
        # 当前匹配长度大小
        match_size = min(len(sentence), max_word_length)
        matched = False
        # 尝试从最大长度开始匹配
        for length in range(match_size, 0, -1):
            word = sentence[-length:]
            if word in dic:
                result.insert(0, word) #在开头插入
                sentence = sentence[:-length]
                matched = True
                break
        # 如果没有匹配到任何词，则切分单个字符
        if not matched:
            result.insert(0, sentence[-1])
            sentence = sentence[:-1]
    return result

# 3、双向匹配算法
"""
双向匹配算法：
分别使用正向最大匹配法和逆向最大匹配法对句子进行切分
1. 切分结果完全相同时，准确率最大
2. 切分结果不同时，切分词数目小的作为将结果
3. 切分结果不同，且切分词数目相同，取逆向最大匹配算法结果
"""

def main():
    #主函数
    print("字典：", Dictionary)
    print("句子：", Sentence)

    FFM_result = FMM(Sentence, Dictionary)
    print("FMM切分结果：", FFM_result)

    BMM_result = BMM(Sentence, Dictionary)
    print("BMM切分结果：", BMM_result)

if __name__ == "__main__":
    main()

