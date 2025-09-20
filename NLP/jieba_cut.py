import jieba
sentence="我来到杭州浙江工业大学"
#jieba.cut分词 segment片段
#jieba是基于统计的分词方法，jieba分词采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合，对于未登录词，采用了基于汉字成词能力的HMM模型，使用了Viterbi算法
#这就是一个典型的词典与统计相结合的混合策略。

#精确模式（默认）
#对待分的句子进行全词匹配，找出所有可能的词语，然后依据词典中的词语频率计算出最可能的切分结果。
seg_list=jieba.cut(sentence, cut_all = False)   #cut_all = False可不写
print("精确模式：" + "/".join(seg_list))

#全模式
#一种比较宽松的分词模式，会将文本中所有可能的词语都切分出来，速度较快。为正向最大匹配
seg_list=jieba.cut(sentence, cut_all = True)
print("全模式：" + "/".join(seg_list))

#搜索引擎模式
#一种更加智能的分词模式，它在精确模式的基础上，对长词再次进行切分，适用于搜索引擎等场景。在搜索引擎模式下，jieba分词库会使用最大概率法分出一些比较长的词语，然后在这些长词中再次使用全模式进行切分，最终得到最可能的切分结果。
#sentence="我来到杭州浙江工业大学，我喜欢这个大学，选工大有底气！"
sentence="小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
seg_list=jieba.cut_for_search(sentence)
print("搜索引擎模式：" + "/".join(seg_list))

#jieba词典增加、删除词
sentence="我来到杭州浙江工业大学"
#增加或删除词只能比原来切分的长度要长才起效果
#变长案例：
jieba.add_word("我来到")
seg_list=jieba.cut(sentence, cut_all = False)   
print("加入“我来到”：" + "/".join(seg_list))
#变短案例：
jieba.add_word("浙")
seg_list=jieba.cut(sentence, cut_all = False)   
print("加入“浙”：" + "/".join(seg_list))
#删除：
jieba.del_word("浙江工业大学")
seg_list=jieba.cut(sentence, cut_all = False)   
print("删除“浙江工业大学”：" + "/".join(seg_list))