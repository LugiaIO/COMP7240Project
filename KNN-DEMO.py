#input dataset
import pandas as pd
from surprise import KNNBasic, dump
Books = 'Books.csv'
Ratings = 'Ratings.csv'
Users = 'Users.csv'

Books_df = pd.read_csv(Books)
Ratings_df = pd.read_csv(Ratings)
Users_df = pd.read_csv(Users)
#Dispose data
Books_df = Books_df.fillna(0)
Users_df.loc[Users_df['Age'] > 100, 'Age'] = None
Users_df = Users_df.fillna(0)
# 合并 Ratings_df 和 Users_df 数据集
merged_df = pd.merge(Ratings_df, Users_df, on='User-ID')
merged_df = merged_df.fillna(0)
# 合并 Books_df 和合并后的数据集
merged_df = pd.merge(merged_df,Books_df, on='ISBN')
merged_df = merged_df.fillna(0)
data_df = merged_df[['Age','ISBN','Book-Rating']].copy(deep=True)
data_df1 = data_df[:10000]
data_df1 = data_df[data_df['Book-Rating'] != 0]
# 将用户的年龄分成若干个区间
age_bins = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 100]
age_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-100']
merged_df['age_group'] = pd.cut(merged_df['Age'], bins=age_bins, labels=age_labels)

# 使用KNN算法进行改进
from surprise import Reader, Dataset, KNNBasic

# 将数据集转换成适合surprise模型的格式
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(data_df1, reader)

# 使用KNN算法进行训练
sim_options = {'name': 'cosine', 'user_based': False, 'min_support': 2, 'shrinkage': 100}
model = KNNBasic(sim_options=sim_options)
trainset = data.build_full_trainset()
model.fit(trainset)

# 输出每个年龄区间内的推荐书籍
for age_group in age_labels:
    testset = trainset.build_anti_testset()
    testset = [x for x in testset if str(x[0]) in merged_df[merged_df['age_group'] == age_group]['User-ID'].unique().tolist()]
    predictions = model.test(testset)
    top_n = []
    for uid, iid, true_r, est, _ in predictions:
        if uid == merged_df[merged_df['age_group'] == age_group]['User-ID'].iloc[0]:
            top_n.append((iid, est))
    top_n = sorted(top_n, key=lambda x: x[1], reverse=True)[:10]
    top_books = [Books_df[Books_df['ISBN'] == i[0]]['Book-Title'].iloc[0] for i in top_n]
    print('年龄区间 %s 推荐的书籍是：%s' % (age_group, top_books))