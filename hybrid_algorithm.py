import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk_dl
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from surprise import Dataset
from surprise import Reader
from surprise import SVD
import pickle
import json
from portal import getRating, getUserId, storeRating


def getDataset():
    books = pd.read_csv("./model/Goodreads_BestBooksEver_1-10000.csv")
    books.dropna(inplace=True)
    books = books[:1500]
    return books


def checkSameGenre(book_title_1, orgin_book, score):
    books = getDataset()
    book_1 = books[books["bookTitle"] == book_title_1]
    book_2 = books[books["bookTitle"] == orgin_book]
    book_concat = pd.concat([book_1, book_2], axis=0)
    book_concat = book_concat["bookGenres"].apply(slashGenres)
    book_concat = book_concat.to_list()
    common_elements = list(set(book_concat[0]) & set(book_concat[1]))
    output = {"bookTitle": book_title_1, "sameGenre": common_elements, "score": score}
    return output


def slashGenres(genres):
    genres = str(genres)
    genre_list = genres.split("|")
    before_slash_list = list(map(lambda x: x.split("/")[0], genre_list))
    return before_slash_list


def slashGenresString(genres):
    genres = str(genres)
    genre_list = genres.split("|")
    before_slash_list = list(map(lambda x: x.split("/")[0], genre_list))
    return " ".join(before_slash_list)


def preprocessDescription(desc):
    desc = str(desc)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(desc.lower())
    words = [w for w in words if not w in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)


def preProcess():
    df = getDataset()
    df["bookGenres"] = df["bookGenres"].apply(slashGenresString)
    df["bookDesc"] = df["bookDesc"].apply(preprocessDescription)
    return df


def trainContentBased():
    books = preProcess()
    books["content"] = books["bookDesc"] + " " + books["bookGenres"]
    tf_idf = TfidfVectorizer(stop_words="english")
    tf_idf_matrix = tf_idf.fit_transform(books["content"])
    with open("./model/tf_idf_model.pkl", "wb") as f:
        pickle.dump(tf_idf_matrix, f)


def trainMFBased():
    books = preProcess()
    reader = Reader(rating_scale=(1, 5))
    books["userID"] = "1145141919810"
    data = Dataset.load_from_df(books[["userID", "bookTitle", "bookRating"]], reader)
    train_set = data.build_full_trainset()
    model = SVD()
    model.fit(train_set)
    with open("./model/mf_model.pkl", "wb") as f:
        pickle.dump(model, f)


def loadFiles(file1, file2):
    with open(file1, "rb") as f1:
        obj1 = pickle.load(f1)
    with open(file2, "rb") as f2:
        obj2 = pickle.load(f2)
    return obj1, obj2


def recommendations(
    user_id, book_title, num_recommendations=6, tf_idf_weight=0.8, mf_weight=0.2
):
    (similarity_matrix, model) = loadFiles(
        "./model/tf_idf_model.pkl", "./model/mf_model.pkl"
    )
    books = preProcess()
    try:
        all_book_titles = books["bookTitle"].unique()
        book_idx = books[books["bookTitle"] == book_title].index[0]
    except IndexError:
        print(f"Could not find the book '{book_title}' in the dataset.")
        return False
    except Exception as e:
        print(f"An error occurred while finding the book index: {e}.")
        return None

    predict_ratings = {}
    total_scores = {}
    tf_idf_scores = {}
    for other_book_title in all_book_titles:
        if other_book_title != book_title:
            other_book_idx = books[books["bookTitle"] == other_book_title].index[0]
            predicted_rating = model.predict(user_id, other_book_title).est
            predicted_rating = (predicted_rating - 0) / (5 - 0)
            predict_ratings[other_book_idx] = predicted_rating
    cosine_similarities = cosine_similarity(
        similarity_matrix[book_idx], similarity_matrix
    ).flatten()
    for i, score in enumerate(cosine_similarities):
        if i != book_idx:
            tf_idf_scores[i] = score
    common_keys = set(predict_ratings.keys()) & set(tf_idf_scores.keys())
    for key in common_keys:
        total_scores[key] = (
            tf_idf_scores[key] * tf_idf_weight + predict_ratings[key] * mf_weight
        )
    total_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    total_scores = total_scores[0:num_recommendations]
    with open("map.json", "r") as f:
        name_map = json.load(f)
        book_name = []
        sim_two_books = []
        for i in total_scores:
            book_name.append(name_map[str(i[0])])
            sim_two_books.append(checkSameGenre(name_map[str(i[0])], book_title, i[1]))
        print(sim_two_books)
        books["bookPages"] = books["bookPages"].str.extract(r"(\d+)")
        sub_books = books[books["bookTitle"].isin(book_name)]
        sub_books = sub_books.loc[
            :,
            [
                "bookTitle",
                "bookImage",
                "bookAuthors",
                "bookPages",
                "bookGenres",
            ],
        ]
        sub_books = sub_books.to_dict("records")
        merged_list = []

        for book1 in sub_books:
            for book2 in sim_two_books:
                if book1["bookTitle"] == book2["bookTitle"]:
                    merged_list.append({**book1, **book2})
                    break
        merged_list = sorted(merged_list, key=lambda x: x["score"], reverse=True)
        if len(merged_list) > 6:
            return merged_list[0:6]
        else:
            return merged_list
    # print(sim_two_books)


def userPreference(user_profile):
    user_profile = user_profile.groupby("bookTitle")["userRating"].mean().reset_index()
    return user_profile


def feedback(username, booktitle, rating, num_recommendations=6):
    storeRating(username, booktitle, rating)
    ratings = getRating(username)
    user_id = getUserId(username)
    rating_record = []
    for rating in ratings:
        new_rating_record = {
            "user_id": user_id,
            "bookTitle": rating[2],
            "userRating": rating[3],
        }
        rating_record.append(new_rating_record)
    rating_record_df = pd.DataFrame(rating_record)
    books = getDataset()
    books["bookGenres"] = books["bookGenres"].apply(slashGenres)
    temp_books = books.copy(deep=True)
    books = books[["bookTitle", "bookGenres"]]
    books = books.drop_duplicates(subset="bookTitle")
    total_feature_list = []
    for index, row in books.iterrows():
        for genre in row["bookGenres"]:
            books.at[index, genre] = 1
            if genre not in total_feature_list:
                total_feature_list.append(genre)
    books = books.fillna(0)
    books_genre_matrix = books[total_feature_list].to_numpy()
    user1_preference_df = userPreference(rating_record_df)
    user_book_rating_df = pd.merge(user1_preference_df, books, validate="one_to_one")
    user_book_rating_df = user_book_rating_df.drop(columns="bookGenres")
    num_cols = user_book_rating_df.iloc[:, 1:].astype("float")
    row_sums = num_cols.sum(axis=1)
    result = num_cols.apply(lambda x: x / row_sums, axis=0)
    df_result = pd.concat([user_book_rating_df.iloc[:, 0], result], axis=1)
    df_result = df_result.drop(columns=["bookTitle", "userRating"])
    user1_profile = df_result.T.dot([1] * len(user1_preference_df))
    u_v_matrix = [user1_profile.values]
    recommendation_table = cosine_similarity(u_v_matrix, books_genre_matrix)
    books["score"] = recommendation_table[0]
    rec_result_plot_based_case_1 = books.sort_values(by=["score"], ascending=False)
    sim_two_books = []
    rec_result_plot_based_case_1 = rec_result_plot_based_case_1[["bookTitle", "score"]][
        1 : num_recommendations + 1
    ]
    temp_books = temp_books.loc[
        :,
        [
            "bookTitle",
            "bookImage",
            "bookAuthors",
            "bookPages",
            "bookGenres",
        ],
    ]
    temp_books["bookPages"] = temp_books["bookPages"].str.extract(r"(\d+)")
    sub_books = temp_books.to_dict("records")

    for index, row in rec_result_plot_based_case_1[["bookTitle", "score"]].iterrows():
        sim_two_books.append(checkSameGenre(row["bookTitle"], booktitle, row["score"]))
    merged_list = []
    for book1 in sub_books:
        for book2 in sim_two_books:
            if book1["bookTitle"] == book2["bookTitle"]:
                merged_list.append({**book1, **book2})
                break
    merged_list = sorted(merged_list, key=lambda x: x["score"], reverse=True)
    if len(merged_list) > 6:
        return merged_list[0:6]
    else:
        return merged_list


# train()
# print(preProcess())
# recommendations("14324", "The Hunger Games")

# trainMFBased()
# trainContentBased()
# print(checkSameGenre("The Pilgrimage", "1984"))
