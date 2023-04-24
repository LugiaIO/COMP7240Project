import numpy as np
import pandas as pd

books = "Goodreads_BestBooksEver_1-10000.csv"
books_df = pd.read_csv(books)
books_clean_df = books_df.dropna()
books_useful_df = books_clean_df[
    ["bookTitle", "bookRating", "ratingCount", "reviewCount", "bookPages", "bookGenres"]
]
books_useful_df = books_useful_df.drop_duplicates(subset="bookTitle")
df = books_useful_df.copy(deep=True)

books_inform_df = df[["bookTitle", "bookGenres"]].copy(deep=True)
for i, row in books_inform_df.iterrows():
    feature_list = []
    for genre in row["bookGenres"].split("|"):
        feature, _ = genre.split("/")
        feature = feature.strip()
        feature_list.append(feature)
    row["bookGenres"] = feature_list

book_with_genres = books_inform_df[["bookTitle", "bookGenres"]].copy(deep=True)
total_feature_list = []
for index, row in books_inform_df.iterrows():
    for genre in row["bookGenres"]:
        book_with_genres.at[index, genre] = 1
        if genre not in total_feature_list:
            total_feature_list.append(genre)

book_with_genres = book_with_genres.fillna(0)
book_with_genres.head()

books_genre_matrix = book_with_genres[total_feature_list].to_numpy()

rating_record = []


def store_rating(user_id, bookTitle, Rating, rating_record):
    new_rating_record = {
        "user_id": user_id,
        "bookTitle": bookTitle,
        "userRating": Rating,
    }
    rating_record.append(new_rating_record)
    return rating_record


#### Testing data
rating_record = store_rating(1, "The Hunger Games", 4, rating_record)
rating_record = store_rating(1, "The Hunger Games", 5, rating_record)
rating_record = store_rating(1, "Twilight", 5, rating_record)
rating_record = store_rating(2, "Twilight", 5, rating_record)
####
rating_record_df = pd.DataFrame(rating_record)


##### function not used, need improvement
def user_rating_record(user_id):
    return rating_record_df[rating_record_df["user_id"] == user_id]


def user_profile(userdata):
    user_profile = userdata.groupby("bookTitle")["userRating"].mean().reset_index()
    return user_profile


def user_preference(user_profile):
    user_preference = user_profile.sample(frac=1.0, random_state=1)
    user_preference = user_preference.reset_index(drop=True)
    return user_preference


user1 = user_rating_record(1)
user1_profile = user_profile(user1)
user1_preference_df = user_preference(user1_profile)

user_book_rating_df = pd.merge(
    user1_preference_df, book_with_genres, validate="one_to_one"
)
user_book_rating_df = user_book_rating_df.drop(columns="bookGenres")
user_book_rating_df

num_cols = user_book_rating_df.iloc[:, 1:].astype("float")
row_sums = num_cols.sum(axis=1)
result = num_cols.apply(lambda x: x / row_sums, axis=0)
df_result = pd.concat([user_book_rating_df.iloc[:, 0], result], axis=1)
df_result = df_result.drop(columns=["bookTitle", "userRating"])

user1_profile = df_result.T.dot([1] * len(user1_preference_df))

user1_profile

from sklearn.metrics.pairwise import cosine_similarity

# Compute the cosine similarity
u_v = user1_profile.values
u_v_matrix = [u_v]

recommendation_table = cosine_similarity(u_v_matrix, books_genre_matrix)

recommendation_table_df = df.copy(deep=True)

recommendation_table_df = df[["bookTitle"]].copy(deep=True)
recommendation_table_df["similarity"] = recommendation_table[0]
recommendation_table_df

rec_result_plot_based_case_1 = recommendation_table_df.sort_values(
    by=["similarity"], ascending=False
)
rec_result_plot_based_case_1.head(20)
