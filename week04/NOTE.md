### 本周主要学习内容如下：
#### 本周主要学习数据清洗，预处理等用到的pandas库、以及jieba、snownlp等相关库使用方法

#### 一、pandas：
##### 1、pandas简介：
当需要对抓取来的数据进行数据清洗（比如去除特殊符号，对指定种类数据筛选，对数据按照某种形式切分等）时，就需要用到pandas对数据进行处理；<br>
pandas是以python中numpy(数学库)为基础，因此可以使用numpy中的一些功能，也可以配合matplotlib库实现可视化功能；<br>
pandas处理数据文件(主要是excel形式)：先读取文件，转化成dataFrame对象，dataFrame对象可以对数据进行筛选，聚合等操作，还可以根据自己要求对数据添加自定义列。<br>
##### pandas使用简单示例：
```python
import pandas as pd
import numpy as np
import matplotlib as plt
import os
# __file__：指当前py文件，此处是获取当前文件绝对路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 拼接数据文件路径
book = os.path.join(pwd,'book_utf8.csv')
# df = pd.read_csv('book_utf8.csv')
df = pd.read_csv(book)
# 输出全部内容
print(df)

# 筛选标题为"还行"这一列
df['还行']

# 切片方式筛选
# 显示前3行
df[1:3]

# 增加列名
df.columns = ['star', 'vote', 'shorts']

# 显示特定的行、列
df.loc[1:3, ['star']]

# 过滤数据
df['star'] == '力荐'
df [ df['star'] == '力荐' ]

# 缺失数据
df.dropna()

# 数据聚合
df.groupby('star').sum()

# 创建新列
star_to_number = {
    '力荐' : 5,
    '推荐' : 4,
    '还行' : 3,
    '较差' : 2,
    '很差' : 1
}
df['new_star'] = df['star'].map(star_to_number)

print(df)
```
##### 测试用数据集,可以用来配合pandas做练习：
```python
from sklearn import datasets #引入数据集
# 鸢尾花数据集
iris = datasets.load_iris()
X, y = iris.data, iris.target

# 查看特征
iris.feature_names

# 查看标签
iris.target_names

# 按照3比1的比例划分训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# load_xxx 各种数据集
# load_boston Boston房屋价格 回归
# load_digits 手写体  分类
# load_iris   鸢尾花 分类聚类
```
##### 2、pandas数据类型：
###### 1）、结构：
pandas引入两个重要数据类型：Series，DataFrame<br>
Series类型有两个基本属性：index，value<br>
Series中的一列中，每列的值都有一个索引，索引也可自定义<br>
DataFrame可以当做看作为excel这种多行多列结构<br>
###### 2）创建和操作：
Series可以通过列表、字典，进行创建，通过列表创建时可以自定义索引；<br>
Series可以转成列表类型，，也可以单独取出索引和值，使用索引查找时会提升查询性能；<br>
```python
import pandas as pd
import numpy as np

# 从列表创建Series
pd.Series(['a', 'b', 'c'])
# 0    a
# 1    b
# 2    c
# dtype: object
# 自动创建索引

# 通过字典创建带索引的Series
s1 = pd.Series({'a':11, 'b':22, 'c':33})
# 通过关键字创建带索引的Series
s2 = pd.Series([11, 22, 33], index = ['a', 'b', 'c'])
s1
s2

# 获取全部索引
s1.index
# 获取全部值
s1.values

# 类型
type(s1.values)    # <class 'numpy.ndarray'>
type(np.array(['a', 'b']))

# 转换为列表
s1.values.tolist()

# 使用index会提升查询性能
#    如果index唯一，pandas会使用哈希表优化，查询性能为O(1)
#    如果index有序不唯一，pandas会使用二分查找算法，查询性能为O(logN)
#    如果index完全随机，每次查询都要扫全表，查询性能为O(N)

# 取出email
emails = pd.Series(['abc at amazom.com', 'admin1@163.com', 'mat@m.at', 'ab@abc.com'])
import re
pattern ='[A-Za-z0-9._]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,5}'
mask = emails.map(lambda x: bool(re.match(pattern, x)))
emails[mask]
```
dataFrame支持列表，嵌套列表创建，可以自定义列索引和行索引<br>
```python
import pandas as pd
# 列表创建dataframe
df1 = pd.DataFrame(['a', 'b', 'c', 'd'])
# 嵌套列表创建dataframe
df2 = pd.DataFrame([
                     ['a', 'b'], 
                     ['c', 'd']
                    ])
# 自定义列索引
df2.columns= ['one', 'two']
# 自定义行索引
df2.index = ['first', 'second']

df2
# 可以在创建时直接指定 DataFrame([...] , columns='...', index='...' )
# 查看索引
df2.columns, df2.index
type(df2.values)
```
##### 3、pandas常规操作：
###### 1）、数据导入：
pandas支持大量格式的数据导入，使用的是read_*()形式;<br>
示例如下：
```python
import pandas as pd
# pip install xlrd
# 导入excel文件
excel1 = pd.read_excel(r'1.xlsx')
# 指定导入哪个Sheet
pd.read_excel(r'1.xlsx',sheet_name = 0)

# 支持其他常见类型 sep为分割符 nrows：需要读取的行数
pd.read_csv(r'c:\file.csv',sep=' ', nrows=10, encoding='utf-8')

pd.read_table( r'file.txt' , sep = ' ')

import pymysql
sql  =  'SELECT * FROM mytable'
conn = pymysql.connect('ip','name','pass','dbname','charset=utf8')
df = pd.read_sql(sql,conn)


# 熟悉数据
# 显示前几行
excel1.head(3)

# 行列数量
excel1.shape

# 详细信息
excel1.info()
excel1.describe()
```
###### 2）、数据预处理：
数据预处理主要两个方面：缺失值处理，重复值处理；<br>
缺失值处理：爬虫反复爬取数据填补缺失值，或者第三方(用户)补全<br>
重复值处理：根据不同业务场景特性判断是否需要删掉重复数据<br>
pandas常用的用来处理数据的函数：
```python
import pandas as pd
import numpy as np

x = pd.Series([ 1, 2, np.nan, 3, 4, 5, 6, np.nan, 8])
#检验序列中是否存在缺失值
x.hasnans
# 将缺失值填充为平均值
x.fillna(value = x.mean())

# 前向填充缺失值
df3=pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
                 
df3.isnull().sum() # 查看缺失值汇总
df3.ffill() # 用上一行填充
df3.ffill(axis=1)  # 用前一列填充

# 缺失值删除
df3.info()
df3.dropna()

# 填充缺失值
df3.fillna('无')

# 重复值处理
df3.drop_duplicates()
```
###### 3）、数据调整：
清洗数据之后，就要按照我们需要的形式对数据进行进一步调整(比如数据格式，存储方式，内容筛选等等)；<br>
- pandas中可以通过dataFrame实例对数据进行多种方式筛选：<br>
- 如可以根据列明和列序号，列值对列筛选，根据行序号对行筛选；<br>
- 可以用指定值对指定列中的值进行替换，支持一对一，多对一，多对多；<br>
- 可以对数据进行排序，支持多列；<br>
- 可以对数据进行删除，支持行删除，列删除；<br>
- 可以对数据进行行列转换；<br>
- 可以对数据进行堆叠展开(透视表处理)；<br>
以下为具体示例：
```python
import pandas as pd
# 行列调整
df = pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
# 列的选择,多个列要用列表
df[ ['A', 'C'] ]
# 某几列
df.iloc[:, [0,2]] # :表示所有行，获得第1和第3列
# 行选择
df.loc[ [0, 2] ] # 选择第1行和第3行
df.loc[ 0:2    ] # 选择第1行到第3行
# 比较
df[ ( df['A']<5 ) & ( df['C']<4 )   ]

# 数值替换
# 一对一替换
# 用于单个异常值处理
df['C'].replace(4,40)

import numpy as np
df.replace(np.NaN, 0)
# 多对一替换
df.replace([4,5,8], 1000)
# 多对多替换
df.replace({4:400,5:500,8:800})
# 排序
# 按照指定列降序排列
df.sort_values ( by = ['A'] ,ascending = False)
# 多列排序
df.sort_values ( by = ['A','C'] ,ascending = [True,False])

# 删除
# 删除列
df.drop( 'A' ,axis = 1)
# 删除行
df.drop( 3 ,axis = 0)
# 删除特定行
df [  df['A'] < 4 ]
# 行列互换
df.T
df.T.T
# 索引重塑
df4 = pd.DataFrame([
                     ['a', 'b', 'c'], 
                     ['d', 'e', 'f']
                    ],
                    columns= ['one', 'two', 'three'],
                    index = ['first', 'second']
                   )       
df4.stack()
df4.unstack()    
df4.stack().reset_index()             
```
##### 4、pandas计算：
pandas计算涉及到，数据行列与数值计算、列与列间计算、数学参数处理pandas数据(除了比较运算，空值没有办法参与其他运算，返回的只能是NaN)；<br>
示例：
```python
import pandas as pd
df = pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
# 算数运算
# 两列之间的加减乘除
df['A'] + df['C'] 

# 任意一列加/减一个常数值，这一列中的所有值都加/减这个常数值
df['A'] + 5

# 比较运算
df['A'] > df ['C']  

# count非空值计数
df.count()

# 非空值每列求和
df.sum()
df['A'].sum()

# 以下运算包括其他运算函数，可以查找pandas官方文档

# mean求均值
# max求最大值
# min求最小值
# median求中位数  
# mode求众数
# var求方差
# std求标准差
```
##### 5、pandas分组聚合：
pandas可以通过dataFrame方式对数据根据某些字段进行分组并计算，需要注意的是透视表；<br>
示例：
```python
import pandas as pd
import numpy as np

# 聚合
sales = [{'account': 'Jones LLC','type':'a', 'Jan': 150, 'Feb': 200, 'Mar': 140},
         {'account': 'Alpha Co','type':'b',  'Jan': 200, 'Feb': 210, 'Mar': 215},
         {'account': 'Blue Inc','type':'a',  'Jan': 50,  'Feb': 90,  'Mar': 95 }]

df2 = pd.DataFrame(sales)
df2.groupby('type').groups

for a, b in df2.groupby('type'):
    print(a)
    print(b)

# 聚合后再计算
df2.groupby('type').count()
# df2.groupby('Jan').sum()


# 各类型产品的销售数量和销售总额
df2.groupby('type').aggregate( {'type':'count' , 'Feb':'sum' })

group=['x','y','z']
data=pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "salary":np.random.randint(5,50,10),
    "age":np.random.randint(15,50,10)
    })

data.groupby('group').agg('mean')
data.groupby('group').mean().to_dict()
data.groupby('group').transform('mean')

# 数据透视表 注意其中columns参数与index类似，是按列分组
pd.pivot_table(data, 
               values='salary', 
               columns='group', 
               index='age', 
               aggfunc='count', 
               margins=True  
            ).reset_index()
```
##### 5、pandas多表拼接：
pandas支持多表数据关联，类似sql，支持一对一，一对多，多对多，左连接，右链接，内连接，外连接，和类似union等操作；<br>
```python
import pandas as pd
import numpy as np

group = ['x','y','z']
data1 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "age":np.random.randint(15,50,10)
    })

data2 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "salary":np.random.randint(5,50,10),
    })

data3 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "age":np.random.randint(15,50,10),
    "salary":np.random.randint(5,50,10),
    })

# 一对一
pd.merge(data1, data2)

# 多对一
pd.merge(data3, data2, on='group')

# 多对多
pd.merge(data3, data2)

# 连接键类型，解决没有公共列问题
pd.merge(data3, data2, left_on= 'age', right_on='salary')

# 连接方式
# 内连接，不指明连接方式，默认都是内连接
pd.merge(data3, data2, on= 'group', how='inner')
# 左连接 left
# 右连接 right
# 外连接 outer

# 纵向拼接
pd.concat([data1, data2])
```
##### 6、pandas输出和绘图：
pandas可以对数据进行多种输出：主要会用到转成excel、csv、pkl等格式，pkl格式性能较高;<br>
pandas对数据进行转换输出:
```python
# 导出为.xlsx文件
df.to_excel( excel_writer = r'file.xlsx')

# 设置Sheet名称
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1')

# 设置索引,设置参数index=False就可以在导出时把这种索引去掉
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1', index = False)

# 设置要导出的列
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1', 
             index = False, columns = ['col1','col2'])

# 设置编码格式
enconding = 'utf-8'

# 缺失值处理
na_rep = 0 # 缺失值填充为0

# 无穷值处理
inf_rep = 0

# 导出为.csv文件
to_csv()

# 性能
df.to_pickle('xx.pkl') 

agg(sum) # 快
agg(lambda x: x.sum()) # 慢
```
pandas用可视化图形展示数据：主要用到matplotlib.pyplot, seaborn
```python
import pandas as pd
import numpy as np

dates = pd.date_range('20200101', periods=12)
df = pd.DataFrame(np.random.randn(12,4), index=dates, columns=list('ABCD'))

import matplotlib.pyplot as plt
plt.plot(df.index, df['A'], )
plt.show()

plt.plot(df.index, df['A'], 
        color='#FFAA00',    # 颜色
        linestyle='--',     # 线条样式
        linewidth=3,        # 线条宽度
        marker='D')         # 点标记

plt.show()

# seaborn其实是在matplotlib的基础上进行了更高级的API封装，从而使绘图更容易、更美观
import seaborn as sns
# 绘制散点图
plt.scatter(df.index, df['A'])
plt.show()

# 美化plt
sns.set_style('darkgrid')
plt.scatter(df.index, df['A'])
plt.show()

```
#### 二、分词、关键词提取，jieba：
有一些业务场景，如书籍，电影评价等，会涉及到自然语言处理、分词、关键词等，这里就需要用jieba库，可以简单实现语义分析；<br>
**jieba分词：**<br>
主要有精确模式、全模式，jieba默认使用精确模式；<br>
jieba也可以使用搜索模式切分出比较流行的词；<br>
```python
import jieba
strings = ['我来自极客大学', 'Python进阶训练营真好玩']

for string in strings:
    result = jieba.cut(string, cut_all=False) # 精确模式
    print('Default Mode: ' + '/'.join(list(result)))

for string in strings:
    result = jieba.cut(string, cut_all=True) # 全模式
    print('Full Mode: ' + '/'.join(list(result)))

result = jieba.cut('钟南山院士接受采访新冠不会二次暴发') # 默认是精确模式
print('/'.join(list(result)))
# "新冠" 没有在词典中，但是被Viterbi算法识别出来了

result = jieba.cut_for_search('小明硕士毕业于中国科学院计算所，后在日本京都大学深造') # 搜索引擎模式
print('Search Mode: ' + '/'.join(list(result)))
```
**jieba提取关键词：**<br>
主要使用两种算法：TF-IDF、TextRank
```python
import jieba.analyse
text = '机器学习，需要一定的数学基础，需要掌握的数学基础知识特别多，如果从头到尾开始学，估计大部分人来不及，我建议先学习最基础的数学知识'
# 基于TF-IDF算法进行关键词抽取
tfidf = jieba.analyse.extract_tags(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=True)         # 返回每个关键字的权重值
# 基于TextRank算法进行关键词抽取
textrank = jieba.analyse.textrank(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=False)         # 返回每个关键字的权重值

import pprint             # pprint 模块提供了打印出任何Python数据结构的类和方法
pprint.pprint(tfidf)
pprint.pprint(textrank)
```
**jieba结束词功能：**<br>
提取关键词、分词时，屏蔽某些词;<br>
```python
import jieba
import jieba.analyse
text = '机器学习，需要一定的数学基础，需要掌握的数学基础知识特别多，如果从头到尾开始学，估计大部分人来不及，我建议先学习最基础的数学知识'
stop_words=r'2jieba/extra_dict/stop_words.txt'
# stop_words 的文件格式是文本文件，每行一个词语
jieba.analyse.set_stop_words(stop_words)

textrank = jieba.analyse.textrank(text,
topK=5,                   
withWeight=False)         

import pprint             # pprint 模块提供了打印出任何Python数据结构的类和方法
pprint.pprint(textrank)

```
stop_words.txt 文件格式：
```txt
需要
掌握
...
```
**用户词典，用指定的词，让jieba进行匹配：**<br>
首先要新建一个指定词语文本，让jieba可以根据该文本进行匹配，格式如下
```
Python进阶训练营 3 nt
```
分别代表指定词语，匹配权重，词性<br>
可以使用自定义用户词典，动态加载词典方式实现，使用用户词典时就需要重新加载；<br>
使用词典例子：
```python
import jieba
string = '极客大学Python进阶训练营真好玩'
user_dict=r'2jieba/extra_dict/user_dict.txt'

# 自定义词典
jieba.load_userdict(user_dict)

result = jieba.cut(string, cut_all=False)
print('自定义: ' + '/'.join(list(result)))

print('=' * 40 )

```
动态加载词典：
```python
# 动态添加词典
jieba.add_word('极客大学')

# 动态删除词典
jieba.del_word('自定义词')

result = jieba.cut(string, cut_all=False)
print('动态添加: ' + '/'.join(list(result)))

print('=' * 40 )

string2 = '我们中出了一个叛徒'
result = jieba.cut(string2, cut_all=False)
print('错误分词: ' + '/'.join(list(result)))

print('=' * 40 )
# 关闭自动计算词频
result = jieba.cut(string2, HMM=False)
print('关闭词频: ' + '/'.join(list(result)))


print('=' * 40 )
# 调整分词，合并
jieba.suggest_freq('中出', True)

result = jieba.cut(string2, HMM=False)
print('分词合并: ' + '/'.join(list(result)))

print('=' * 40 )
# 调整词频，分开分词
string3 = '如果放到Post中将出错'
jieba.suggest_freq(('中','将'), True)
result = jieba.cut(string3, HMM=False)
print('分开分词: ' + '/'.join(list(result)))


# 词性表

# 1. 名词 (1个一类，7个二类，5个三类)
# 名词分为以下子类：
# n 名词
# nr 人名
# nr1 汉语姓氏
# nr2 汉语名字
# nrj 日语人名
# nrf 音译人名
# ns 地名
# nsf 音译地名
# nt 机构团体名
# nz 其它专名
# nl 名词性惯用语
# ng 名词性语素
# 2. 时间词(1个一类，1个二类)
# t 时间词
# tg 时间词性语素
# 3. 处所词(1个一类)
# s 处所词
# 4. 方位词(1个一类)
# f 方位词
# 5. 动词(1个一类，9个二类)
# v 动词
# vd 副动词
# vn 名动词
# vshi 动词“是”
# vyou 动词“有”
# vf 趋向动词
# vx 形式动词
# vi 不及物动词（内动词）
# vl 动词性惯用语
# vg 动词性语素
# 6. 形容词(1个一类，4个二类)
# a 形容词
# ad 副形词
# an 名形词
# ag 形容词性语素
# al 形容词性惯用语
# 7. 区别词(1个一类，2个二类)
# b 区别词
# bl 区别词性惯用语
# 8. 状态词(1个一类)
# z 状态词
# 9. 代词(1个一类，4个二类，6个三类)
# r 代词
# rr 人称代词
# rz 指示代词
# rzt 时间指示代词
# rzs 处所指示代词
# rzv 谓词性指示代词
# ry 疑问代词
# ryt 时间疑问代词
# rys 处所疑问代词
# ryv 谓词性疑问代词
# rg 代词性语素
# 10. 数词(1个一类，1个二类)
# m 数词
# mq 数量词
# 11. 量词(1个一类，2个二类)
# q 量词
# qv 动量词
# qt 时量词
# 12. 副词(1个一类)
# d 副词
# 13. 介词(1个一类，2个二类)
# p 介词
# pba 介词“把”
# pbei 介词“被”
# 14. 连词(1个一类，1个二类)
# c 连词
# cc 并列连词
# 15. 助词(1个一类，15个二类)
# u 助词
# uzhe 着
# ule 了 喽
# uguo 过
# ude1 的 底
# ude2 地
# ude3 得
# usuo 所
# udeng 等 等等 云云
# uyy 一样 一般 似的 般
# udh 的话
# uls 来讲 来说 而言 说来
# uzhi 之
# ulian 连 （“连小学生都会”）
# 16. 叹词(1个一类)
# e 叹词
# 17. 语气词(1个一类)
# y 语气词(delete yg)
# 18. 拟声词(1个一类)
# o 拟声词
# 19. 前缀(1个一类)
# h 前缀
# 20. 后缀(1个一类)
# k 后缀
# 21. 字符串(1个一类，2个二类)
# x 字符串
# xx 非语素字
# xu 网址URL
# 22. 标点符号(1个一类，16个二类)
# w 标点符号
# wkz 左括号，全角：（ 〔 ［ ｛ 《 【 〖 〈 半角：( [ { <
# wky 右括号，全角：） 〕 ］ ｝ 》 】 〗 〉 半角： ) ] { >
# wyz 左引号，全角：“ ‘ 『
# wyy 右引号，全角：” ’ 』
# wj 句号，全角：。
# ww 问号，全角：？ 半角：?
# wt 叹号，全角：！ 半角：!
# wd 逗号，全角：， 半角：,
# wf 分号，全角：； 半角： ;
# wn 顿号，全角：、
# wm 冒号，全角：： 半角： :
# ws 省略号，全角：…… …
# wp 破折号，全角：—— －－ ——－ 半角：--- ----
# wb 百分号千分号，全角：％ ‰ 半角：%
# wh 单位符号，全角：￥ ＄ ￡ ° ℃ 半角：$
```
#### 三、情感倾向分析，snownlp：
可以像jieba一样分词，还有另一项功能，做情感倾向分析：
```python
from snownlp import SnowNLP
text = '其实故事本来真的只值三星当初的中篇就足够了但是啊看到最后我又一次被东野叔的反战思想打动了所以就加多一星吧'
s = SnowNLP(text)

# 1 中文分词
s.words

# 2 词性标注 (隐马尔可夫模型) 接近1正面
list(s.tags) 

# 3 情感分析（朴素贝叶斯分类器）
s.sentiments
text2 = '这本书烂透了'
s2 = SnowNLP(text2)
s2.sentiments

# 4 拼音（Trie树）
s.pinyin

# 5 繁体转简体
text3 = '後面這些是繁體字'
s3 = SnowNLP(text3)
s3.han

# 6 提取关键字
s.keywords(limit=5)

# 7 信息衡量
s.tf # 词频越大越重要
s.idf # 包含此条的文档越少，n越小，idf越大，说明词条t越重要

# 8 训练
from snownlp import seg
seg.train('data.txt')
seg.save('seg.marshal') # 新训练模型位置
# 修改snownlp/seg/__init__.py的 data_path 指向新的模型即可
```

**补充：**

作业涉及到：
dataframe中的loc函数：
```python
df = pd.DataFrame(data)
result = df.loc[ (df[id] < 1000) & (df[age] > 30) ]
```
简单的说：
iloc，即index locate 用index索引进行定位，所以参数是整型，如：df.iloc[10:20, 3:5]
loc，则可以使用column名和index名进行定位，如：
df.loc[‘image1’:‘image10’, ‘age’:‘score’]






