# -*- coding: utf-8 -*-



# 需要识别的句子（这里是中文）
str = 'Welcome'

# 需要识别的句子（这里是英文）
# str = 'Otec matka syn.'

# 引用库
from langdetect import detect
from langdetect import detect_langs

# 当文本过短或模糊时，判断出来的结果会不确定；
# 如果要让结果唯一，添加以下两行：
from langdetect import DetectorFactory
DetectorFactory.seed = 0

# 判断语言种类
print(detect(str))
f = detect_langs(str)
# 概率
print(f[0])