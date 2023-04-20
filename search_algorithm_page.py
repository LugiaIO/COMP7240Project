import numpy as np
import pandas as pd


def dataPreprocessing():
    books = "./model/Goodreads_BestBooksEver_1-10000.csv"
    books_df = pd.read_csv(books)
    books_df.isna().sum()
    books_clean_df = books_df.dropna()
    books_useful_df = books_clean_df[
        [
            "bookTitle",
            "bookRating",
            "bookImage",
            "bookAuthors",
            "bookPages",
            "bookDesc",
            "bookGenres",
        ]
    ]
    return books_useful_df


def userPreferenceJudge(prefer):
    if prefer == "long":
        min_pages = 500
        max_pages = 1000
    elif prefer == "short":
        min_pages = 1
        max_pages = 500
    else:
        min_pages = 1
        max_pages = 1000

    return min_pages, max_pages


def recommendByPages(min_pages, max_pages, num_recommendations=None):
    df = dataPreprocessing()
    df["bookPages"] = df["bookPages"].str.extract(r"(\d+)")
    suitable_book = df[(df["bookPages"].astype(int) >= min_pages)]
    suitable_book = suitable_book[(suitable_book["bookPages"].astype(int) <= max_pages)]
    book_recommend = suitable_book.head(num_recommendations)
    return book_recommend.to_dict("records")


def recommendByRatingAndPages(
    rating_threshold, min_pages, max_pages, num_recommendations=None
):
    df = dataPreprocessing()
    suitable_book = df
    [
        (df["bookRating"] >= rating_threshold)
        & (df["bookPages"].str.extract(r"(\d+)", expand=False).astype(int) >= min_pages)
        & (df["bookPages"].str.extract(r"(\d+)", expand=False).astype(int) <= max_pages)
    ]
    book_recommend = suitable_book.sort_values("bookRating", ascending=False)
    return book_recommend.head(num_recommendations)
