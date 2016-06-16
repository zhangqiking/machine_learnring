#_*_coding:utf-8_*_

import pandas as pd
import sklearn
import numpy as np
from scipy.stats import spearmanr,pointbiserialr
from sklearn.tree import DecisionTreeClassifier
from  sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import svm

df = pd.read_csv('C:\\Users\\Qi\\Desktop\\tanic\\train.csv')

df['Cabin'].fillna(0,inplace=True)
print df['Age'].isnull().value_counts() # 统计年龄缺失的数目
print df['Cabin'].isnull().value_counts() # 统计Cabin缺失的数目

# 不同称呼头衔的乘客在逃生的过程中可能得到的帮助会有所不同
Title_Dictionary = {
                    "Capt":       "Officer",
                    "Col":        "Officer",
                    "Major":      "Officer",
                    "Jonkheer":   "Royalty",
                    "Don":        "Royalty",
                    "Sir" :       "Royalty",
                    "Dr":         "Officer",
                    "Rev":        "Officer",
                    "the Countess":"Royalty",
                    "Dona":       "Royalty",
                    "Mme":        "Mrs",
                    "Mlle":       "Miss",
                    "Ms":         "Mrs",
                    "Mr" :        "Mr",
                    "Mrs" :       "Mrs",
                    "Miss" :      "Miss",
                    "Master" :    "Master",
                    "Lady" :      "Royalty"
                    }
df['Title'] = df['Name'].apply(lambda x: Title_Dictionary[x.split(',')[1].split('.')[0].strip()])

# Ticket的前缀可能表示在轮船中的位置不同，影响生还几率
def ticket_pre(x):
    s = x.split(' ')
    if len(s)==1:
        return "NoPre"
    else:
        return s[0]
df['TicketPre'] = df['Ticket'].apply(lambda x: ticket_pre(x))

# 年龄缺失值按["Title", "Pclass", "Sex"]属性取中间值
mask_Age = df.Age.notnull()
Age_Sex_Title_Pclass = df.loc[mask_Age, ["Age", "Title", "Sex", "Pclass"]]
Filler_Ages = Age_Sex_Title_Pclass.groupby(by = ["Title", "Pclass", "Sex"]).median()
Filler_Ages = Filler_Ages.Age.unstack(level = -1).unstack(level = -1)

mask_Age = df.Age.isnull()
Age_Sex_Title_Pclass_missing = df.loc[mask_Age, ["Title", "Sex", "Pclass"]]

def Age_filler(row):
    if row.Sex == "female":
        age = Filler_Ages.female.loc[row["Title"], row["Pclass"]]
        return age
    
    elif row.Sex == "male":
        age = Filler_Ages.male.loc[row["Title"], row["Pclass"]]
        return age
    
Age_Sex_Title_Pclass_missing["Age"]  = Age_Sex_Title_Pclass_missing.apply(Age_filler, axis = 1)   
df["Age"] = pd.concat([Age_Sex_Title_Pclass["Age"], Age_Sex_Title_Pclass_missing["Age"]])    

print df['Fare'].isnull().value_counts() # 统计Fare缺失的数目

df['FamilySize'] = df['SibSp'] + df['Parch']
df = df.drop(['Ticket','Cabin'],axis=1)

# Convert categorical variable into dummy variables
dummies_Sex=pd.get_dummies(df['Sex'],prefix='Sex')
dummies_Embarked = pd.get_dummies(df['Embarked'], prefix= 'Embarked') 
dummies_Pclass = pd.get_dummies(df['Pclass'], prefix= 'Pclass')
dummies_Title = pd.get_dummies(df['Title'], prefix= 'Title')
dummies_TicketPrefix = pd.get_dummies(df['TicketPre'], prefix='TicketPre')
df = pd.concat([df, dummies_Sex, dummies_Embarked, dummies_Pclass, dummies_Title, dummies_TicketPrefix], axis=1)
df = df.drop(['Sex','Embarked','Pclass','Title','Name','TicketPre'], axis=1)

df = df.set_index(['PassengerId'])


# 计算相关系数
columns = df.columns.values
param=[]
correlation=[]
abs_corr=[]

for c in columns:
    #Check if binary or continuous
    if len(df[c].unique())<=2:
        corr = spearmanr(df['Survived'],df[c])[0]
    else:
        corr = pointbiserialr(df['Survived'],df[c])[0]
    param.append(c)
    correlation.append(corr)
    abs_corr.append(abs(corr))

#Create dataframe for visualization
param_df=pd.DataFrame({'correlation':correlation,'parameter':param, 'abs_corr':abs_corr})
#Sort by absolute correlation
param_df=param_df.sort_values(by=['abs_corr'], ascending=False)
#Set parameter name as index
param_df=param_df.set_index('parameter')



'''
# 利用DecisionTree进行特征选择
scoresCV = []
scores = []
for i in range(1,len(param_df)):
    new_df=df[param_df.index[0:i+1].values]
    X = new_df.ix[:,1::]
    y = new_df.ix[:,0]
    clf = DecisionTreeClassifier()
    scoreCV = sklearn.cross_validation.cross_val_score(clf, X, y, cv= 10)
    scores.append(np.mean(scoreCV))
     
plt.figure(figsize=(15,5))
plt.plot(range(1,len(scores)+1),scores, '.-')
plt.axis("tight")
plt.title('Feature Selection', fontsize=14)
plt.xlabel('# Features', fontsize=12)
plt.ylabel('Score', fontsize=12)
plt.grid();
'''



# 选择前15个特征
best_features=param_df.index[1:60].values
X = df[best_features]
y = df['Survived']
# 划分训练集和测试集
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.33,random_state=44)

# 决策树算法
plt.figure(figsize=(15,7))

#Max Features
plt.subplot(2,3,1)
feature_param = ['auto','sqrt','log2',None]
scores=[]
for feature in feature_param:
    clf = DecisionTreeClassifier(max_features=feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)   # 计算测试集的平均正确率
    scores.append(np.mean(scoreCV))

clf = LogisticRegression()
clf.fit(X_train,y_train)
pre = clf.predict(X_test)

print np.mean(pre==y_test)

# 对不同参数进行作图
plt.plot(scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Max Features')
plt.xticks(range(len(feature_param)), feature_param)
plt.grid()
plt.show()


