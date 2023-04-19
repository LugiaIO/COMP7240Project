#input dataset
import numpy as np
import pandas as pd
Books = 'Books.csv'
Ratings = 'Ratings.csv'
Users = 'Users.csv'
Books_df = pd.read_csv(Books)
Ratings_df = pd.read_csv(Ratings)
Users_df = pd.read_csv(Users)

Books_df = Books_df.fillna(0)

Users_df['Age'].describe()
Users_df.loc[Users_df['Age'] > 100, 'Age'] = None
Users_df = Users_df.fillna(0)

####
# 这一部分暂时没有用到 把user和rating的dataframe合并在一块儿了
Merge_Ratings_df = pd.merge(Users_df,Ratings_df,how='outer')
Merge_Ratings_df = Merge_Ratings_df.fillna(0)
Merge_Ratings_df
####

preBooks_df = Books_df[:10000]
from sklearn.model_selection import train_test_split
preratings_df = Ratings_df[:10000]
training_set, test_set = train_test_split(preratings_df,test_size=0.2,random_state=42)
preusers_df = Users_df[:10000]

# First let's make a copy of the users_df
users_age = preusers_df[['User-ID','Age']].copy(deep=True)
age_list = [] # Store the occurred age range
for index, row in preusers_df.iterrows():
    age = int(row['Age'] // 10) * 10 # Group the age into a range of 10
    if age not in age_list:
        age_list.append(age)
    users_age.at[index, str(age)] = 1
age_range = [str(age) for age in age_list]
users_age = users_age.fillna(0)

#Age with vector
users_age_matrix = users_age.drop(columns=['User-ID','Age'])
age_list_matrix = users_age_matrix.values

#Build User profile
users_Rating = preratings_df[preratings_df['User-ID']==243]
users_preference_df = users_Rating.sample(frac=0.20, random_state=1)
users_preference_df = users_preference_df.reset_index(drop=True)
users_preference_df 

users_book_rating_df = pd.merge(users_preference_df,users_age)
users_book_rating_df

users_book_df = users_book_rating_df.copy(deep=True)
users_book_df = users_book_df[age_range]

rating_weight = users_preference_df['Book-Rating'] / users_preference_df['Book-Rating'].sum()

user_profile = users_book_df.T.dot(rating_weight)
user_profile

user_profile_normalized = user_profile / sum(user_profile.values)

#Recoomend Book
books_with_age = users_age[age_range]
u_v = user_profile_normalized.values
u_v_matrix = np.array([u_v] * len(books_with_age))

books_with_age_np = np.array(books_with_age)

res = np.multiply(u_v_matrix,books_with_age_np)
res = res.sum(axis=1)

# Concate the ranking result into the movie dataframe
recommendation_table_df = Books_df[['ISBN','Book-Title']].copy(deep=True)
recommendation_table_df['RankingScore'] = pd.Series(res)
recommendation_table_df = recommendation_table_df.fillna(0)

rec_result_GENRE_based = recommendation_table_df.sort_values(by=['RankingScore'], ascending=False)
rec_result_GENRE_based.head(20)