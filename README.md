# Book Recommendation System

This is a book recommendation system built using Python. It utilizes a hybrid algorithm that combines content-based filtering and collaborative filtering techniques to provide personalized book recommendations to users. The system is implemented as a web application using Flask framework.

## Table of Contents

- [Book Recommendation System](#book-recommendation-system)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)
  - [Data](#data)
  - [Dependencies](#dependencies)
  - [Contributing](#contributing)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Niltopia/COMP7240Project.git
```

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the database:

- The system uses a SQLite database to store user information and ratings. Ensure that you have SQLite installed.
- Create a new SQLite database file `database.db` and import the provided database schema.
- Update the database file path in the `connection()` function in `portal.py`.

4. Train the recommendation models:

- Run the following commands to train the content-based and matrix factorization-based recommendation models:

```bash
python hybrid_algorithm.py
```

This will generate the required model files: `tf_idf_model.pkl` and `mf_model.pkl`.

5. Run the application:

```bash
python app.py
```

The application will be accessible at `http://localhost:8081` by default.

## Usage

- Register a new user account or log in with an existing account.
- Enter a book title or select a book from the list.
- Get personalized book recommendations based on your preferences and ratings.
- Rate a book to provide feedback and improve the recommendations.

## Features

- Hybrid algorithm: The recommendation system combines content-based and collaborative filtering techniques for better personalized recommendations.
- User registration and authentication: Users can create new accounts and log in securely.
- Book search: Users can search for books by title and select a book from the list.
- Personalized recommendations: The system suggests books based on user preferences and ratings.
- Rating feedback: Users can rate books to provide feedback and improve the recommendation accuracy.

## Data

The system uses a dataset of book information obtained from [Goodreads](https://www.goodreads.com). The dataset includes book titles, authors, descriptions, genres, and ratings.

## Dependencies

The system relies on the following Python libraries:

- Flask: A micro web framework for building the web application.
- SQLite: A lightweight relational database used for storing user information and ratings.
- Surprise: A Python scikit for building and analyzing recommender systems.
- pandas: A data manipulation library for handling and processing the book dataset.
- numpy: A library for mathematical operations and computations.
- scikit-learn: A machine learning library used for feature extraction and similarity calculations.
- nltk: A natural language processing library for text preprocessing.

## Contributing

Developer: Vesper - [@LugiaIO](https://github.com/LugiaIO) - pccw@duck.com

Developer: Henry Zheng - [@FEI120483](https://github.com/FEI120483) - 1204831218@qq.com
