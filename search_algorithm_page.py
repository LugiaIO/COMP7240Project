import numpy as np
import pandas as pd
from hybrid_algorithm import preProcess, checkSameGenre


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
    df = preProcess()
    df["bookPages"] = df["bookPages"].str.extract(r"(\d+)")
    suitable_book = df[(df["bookPages"].astype(int) >= min_pages)]
    suitable_book = suitable_book[(suitable_book["bookPages"].astype(int) <= max_pages)]
    book_recommend = suitable_book.head(num_recommendations)
    hidden_score = True
    return (book_recommend.to_dict("records"), hidden_score)
