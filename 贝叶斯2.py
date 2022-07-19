# -*- coding: utf-8 -*-
"""
朴素贝叶斯分类器
"""
#导入数据
from sklearn.datasets import fetch_20newsgroups
news=fetch_20newsgroups(subset='all')
 
#数据分割，形成训练集和测试集
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(news.data,news.target,test_size=0.25,random_state=33)
#构建模型
from sklearn.feature_extraction.text import CountVectorizer
vec=CountVectorizer()
x_train=vec.fit_transform(x_train)
x_test=vec.transform(x_test)
#导入bayes模型
from sklearn.naive_bayes import MultinomialNB
mnb=MultinomialNB()
#训练数据
mnb.fit(x_train,y_train)
#预测
y_pred=mnb.predict(x_test)
#评估模型
from sklearn.metrics import classification_report
print("朴素贝叶斯分类器的准确率为:",mnb.score(x_test,y_test))
print(classification_report(y_test,y_pred,target_names=news.target_names))
