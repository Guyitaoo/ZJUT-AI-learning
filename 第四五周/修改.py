import pandas as pd
import numpy as np
import os
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import matplotlib.pyplot as plt
import seaborn as sns

# 读取文本数据
text_contents = []
base_path = r'D:\Python study\text'

for i in range(1, 6):
    filename = os.path.join(base_path, f'text_{i}.txt')
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            text_contents.append(content)
    except FileNotFoundError:
        print(f"警告: 文件 {filename} 未找到，使用默认内容")
        text_contents.append(f'默认文本内容{i}')
    except Exception as e:
        print(f"读取文件 {filename} 时出错: {e}")
        text_contents.append(f'默认文本内容{i}')

# 对文本进行分词处理
def chinese_tokenizer(text):
    return ' '.join(jieba.cut(text))

segmented_texts = [chinese_tokenizer(text) for text in text_contents]

# 使用TfidfVectorizer进行文本向量化
vectorizer = TfidfVectorizer(max_features=50)
tfidf_matrix = vectorizer.fit_transform(segmented_texts)

# 获取词汇表
feature_names = vectorizer.get_feature_names_out()
print("词汇表（前20个）:")
print(feature_names[:20])
print(f"\n词汇表总大小: {len(feature_names)}")

# 显示TF-IDF矩阵
print("\nTF-IDF矩阵形状:", tfidf_matrix.shape)
print("TF-IDF矩阵（稠密形式）:")
print(tfidf_matrix.toarray())

# 计算文本间的相似度
# 1. 余弦相似度
cosine_sim = cosine_similarity(tfidf_matrix)
print("\n余弦相似度矩阵:")
print(cosine_sim)

# 2. 欧氏距离
euclidean_dist = euclidean_distances(tfidf_matrix)
print("\n欧氏距离矩阵:")
print(euclidean_dist)

# 找到最相似的两个人（基于余弦相似度）
np.fill_diagonal(cosine_sim, 0)  # 将对角线设为0，避免自己与自己比较
max_sim_idx = np.unravel_index(np.argmax(cosine_sim), cosine_sim.shape)
max_similarity = cosine_sim[max_sim_idx]

print(f"\n最相似的两人是: 用户{max_sim_idx[0]+1} 和 用户{max_sim_idx[1]+1}")
print(f"相似度: {max_similarity:.4f}")

# 可视化相似度矩阵 - 热力图
plt.figure(figsize=(12, 5))

# 余弦相似度热力图
plt.subplot(1, 2, 1)
sns.heatmap(cosine_sim, annot=True, cmap='Blues', 
            xticklabels=[f'用户{i}' for i in range(1, 6)], 
            yticklabels=[f'用户{i}' for i in range(1, 6)])
plt.title('余弦相似度矩阵')

# 欧氏距离热力图
plt.subplot(1, 2, 2)
sns.heatmap(euclidean_dist, annot=True, cmap='Reds',
            xticklabels=[f'用户{i}' for i in range(1, 6)], 
            yticklabels=[f'用户{i}' for i in range(1, 6)])
plt.title('欧氏距离矩阵')

plt.tight_layout()
plt.savefig(r'C:\Users\chenz\Desktop\Program\Python\自然语言处理\第四五周\相似度分析.png')
plt.show()

# 保存结果到Excel
output_path = r"C:\Users\chenz\Desktop\Program\Python\自然语言处理\第四五周"
os.makedirs(output_path, exist_ok=True)

output_file = os.path.join(output_path, "文本相似度分析结果.xlsx")

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 保存原始文本
    texts_df = pd.DataFrame({
        '用户ID': [f'用户{i}' for i in range(1, 6)],
        '自我介绍': text_contents
    })
    texts_df.to_excel(writer, sheet_name='原始文本', index=False)
    
    # 保存TF-IDF矩阵
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=feature_names,
        index=[f'用户{i}' for i in range(1, 6)]
    )
    tfidf_df.to_excel(writer, sheet_name='TF-IDF矩阵', index=True)
    
    # 保存余弦相似度矩阵
    cosine_df = pd.DataFrame(
        cosine_sim,
        columns=[f'用户{i}' for i in range(1, 6)],
        index=[f'用户{i}' for i in range(1, 6)]
    )
    cosine_df.to_excel(writer, sheet_name='余弦相似度', index=True)
    
    # 保存欧氏距离矩阵
    euclidean_df = pd.DataFrame(
        euclidean_dist,
        columns=[f'用户{i}' for i in range(1, 6)],
        index=[f'用户{i}' for i in range(1, 6)]
    )
    euclidean_df.to_excel(writer, sheet_name='欧氏距离', index=True)
    
    # 保存词汇表
    vocab_df = pd.DataFrame({'词汇': feature_names})
    vocab_df.to_excel(writer, sheet_name='词汇表', index=False)

print(f"\n文本相似度分析结果已保存至: {output_file}")