import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# from fuzzywuzzy import process
import pickle


def getDataset():
    books = pd.read_csv("./model/Goodreads_BestBooksEver_1-10000.csv")
    return books


def train():
    books = pd.read_csv("./model/Goodreads_BestBooksEver_1-10000.csv")
    books = books.dropna()
    tf_idf = TfidfVectorizer(stop_words="english")
    books["text"] = (
        books["bookTitle"]
        + " "
        + books["bookGenres"]
        + " "
        + books["bookDesc"]
        + " "
        + books["bookAuthors"]
    )
    tf_idf_matrix = tf_idf.fit_transform(books["text"])
    similarity_matrix = cosine_similarity(tf_idf_matrix)
    with open("./model/tf_idf_model.pkl", "wb") as f:
        pickle.dump(similarity_matrix, f)


def recommendations(book_title, num_recommendations=9):
    with open("./model/tf_idf_model.pkl", "rb") as f:
        similarity_matrix = pickle.load(f)
        books = getDataset()
        try:
            book_idx = books[books["bookTitle"] == book_title].index[0]
        except IndexError:
            print(f"Could not find the book '{book_title}' in the dataset.")
            return False
        except Exception as e:
            print(f"An error occurred while finding the book index: {e}.")
            return None
        sim_scores = list(enumerate(similarity_matrix[book_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1 : num_recommendations + 1]
        book_indices = [i[0] for i in sim_scores]
        # sim_scores = pd.DataFrame(sim_scores)
        print(sim_scores)
        books["bookPages"] = books["bookPages"].str.extract(r"(\d+)")
        books = books.iloc[book_indices]
        books = books.loc[
            :,
            [
                "bookTitle",
                "bookRating",
                "bookImage",
                "bookAuthors",
                "bookPages",
                "bookDesc",
                "bookGenres",
            ],
        ]
        print(books)
        return books.to_dict("records")


# train()
# print(search("The Pilgrimage"))
