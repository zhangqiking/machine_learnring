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
print df['Age'].isnull().value_counts() # ͳ������ȱʧ����Ŀ
print df['Cabin'].isnull().value_counts() # ͳ��Cabinȱʧ����Ŀ

# ��ͬ�ƺ�ͷ�εĳ˿��������Ĺ����п��ܵõ��İ�����������ͬ
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

# Ticket��ǰ׺���ܱ�ʾ���ִ��е�λ�ò�ͬ��Ӱ����������
def ticket_pre(x):
    s = x.split(' ')
    if len(s)==1:
        return "NoPre"
    else:
        return s[0]
df['TicketPre'] = df['Ticket'].apply(lambda x: ticket_pre(x))

# ����ȱʧֵ��["Title", "Pclass", "Sex"]����ȡ�м�ֵ
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

print df['Fare'].isnull().value_counts() # ͳ��Fareȱʧ����Ŀ

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


# �������ϵ��
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
# ����DecisionTree��������ѡ��
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



# ѡ��ǰ15������
best_features=param_df.index[1:60].values
X = df[best_features]
y = df['Survived']
# ����ѵ�����Ͳ��Լ�
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.33,random_state=44)

# �������㷨
plt.figure(figsize=(15,7))

#Max Features
plt.subplot(2,3,1)
feature_param = ['auto','sqrt','log2',None]
scores=[]
for feature in feature_param:
    clf = DecisionTreeClassifier(max_features=feature)
    clf.fit(X_train,y_train)
    scoreCV = clf.score(X_test,y_test)   # ������Լ���ƽ����ȷ��
    scores.append(np.mean(scoreCV))

clf = LogisticRegression()
clf.fit(X_train,y_train)
pre = clf.predict(X_test)

print np.mean(pre==y_test)

# �Բ�ͬ����������ͼ
plt.plot(scores, '.-')
plt.axis('tight')
# plt.xlabel('parameter')
# plt.ylabel('score')
plt.title('Max Features')
plt.xticks(range(len(feature_param)), feature_param)
plt.grid()
plt.show()


