#input dataset
import pandas as pd

Books = 'Books.csv'
Ratings = 'Ratings.csv'
Users = 'Users.csv'

Books_df = pd.read_csv(Books)
Ratings_df = pd.read_csv(Ratings)
Users_df = pd.read_csv(Users)

merged_df = pd.merge(Ratings_df, Users_df, on='User-ID')
merged_df = pd.merge(merged_df, Books_df, on='ISBN')

age_bins = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 100]
age_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-100']
merged_df['age_group'] = pd.cut(merged_df['Age'], bins=age_bins, labels=age_labels)

top_books_by_age = merged_df.groupby('age_group')['Book-Title'].apply(lambda x: x.value_counts().index[0])

for i, age_group in enumerate(age_labels):
    print('年龄区间 %s 推荐的书籍是：%s' % (age_group, top_books_by_age[i]))