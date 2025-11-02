import pandas as pd
import numpy as np
import os
import jieba
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

#正确的文件读取方式
text_contents = []
base_path = r'D:\Python study\text'

# 读取5个文件
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

data = pd.DataFrame({
    #分类列
    '城市': ['北京', '贵阳', '杭州', '宁波', '杭州'],
    '性别': ['男', '男', '女', '女', '男'],
    '高考选科': ['物化地', '物化生', '物化政', '物化地', '物化生'],
    #数值列
    '出生月份': [11, 1, 12, 3, 3],
    '生活费': [2000, 1700, 1880, 1560, 2100],
    #文本列
    '自我介绍': text_contents
})
print("原始数据:")
print(data)

################### 方法1: 基本的OneHotEncoder使用
print("\n=== 方法1: 基本OneHotEncoder ===")

categorical_columns = ['城市', '性别', '高考选科']
encoder = OneHotEncoder(sparse_output=False, drop='first')
encoded_array = encoder.fit_transform(data[categorical_columns])
feature_names = encoder.get_feature_names_out(categorical_columns)
encoded_df = pd.DataFrame(encoded_array,columns=feature_names)
print("编码后的数据:")
print(encoded_df)

###################方法2: 使用ColumnTransformer处理混合数据类型
print("\n=== 方法2: 使用ColumnTransformer ===")

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', ['出生月份', '生活费']),  # 数值列直接通过
        ('cat', OneHotEncoder(drop='first'), categorical_columns),  # 分类列进行编码
        ('text', TfidfVectorizer(max_features=10), '自我介绍')  # 文本列使用TF-IDF处理
    ]
)

try:
    # 应用变换
    transformed_data = preprocessor.fit_transform(data)
    print("转换后的数据形状:", transformed_data.shape)

    # 获取所有特征名称
    feature_names = (
        ['出生月份', '生活费'] + 
        list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_columns)) +
        list(preprocessor.named_transformers_['text'].get_feature_names_out())
    )

    # 创建DataFrame（处理可能的稀疏矩阵）
    if hasattr(transformed_data, 'toarray'):
        # 如果是稀疏矩阵，转换为密集数组
        transformed_df = pd.DataFrame(transformed_data.toarray(), columns=feature_names)
    else:
        # 如果已经是密集数组，直接使用
        transformed_df = pd.DataFrame(transformed_data, columns=feature_names)
    
    print("转换后的数据:")
    print(transformed_df)
    
except Exception as e:
    print(f"数据转换过程中出现错误: {e}")