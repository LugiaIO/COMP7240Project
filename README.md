# Book Recommendation System

Our recommendation system provides a personalized experience for users, utilizing a hybrid algorithm, feedback, and preferences to deliver relevant and informative recommendations.

## Live Demo

https://comp7240-4whdf73sva-df.a.run.app

## Prerequisites

- [Python 3.9.16](https://www.python.org/)


## Installing

```bash
pip install requirements.txt
```

## Running

```python
python app.py
```
The terminal will output:
```bash
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead. 
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:8081
* Running on http://198.18.0.1:8081
```
Click the link `http://127.0.0.1:8081`, and enjoy the system.
## Built With

  - [Flask](https://flask.palletsprojects.com/en/2.2.x/) - Web Framework
  - [SQLite](https://sqlite.org/index.html) - Database
  - [Bootstrap](https://getbootstrap.com) - Free and open-source CSS framework
  - [Surprise](https://surprise.readthedocs.io/en/stable/index.html) - Python library “Surprise” for recommendation methods
  - [nltk](https://www.nltk.org) - Python library “nltk” for preprocess text data for further analysis

## Source Tree
```bash
.
├── Dockerfile
├── app.py
├── feedback.py
├── hybrid_algorithm.py
├── map.json
├── model
│   ├── Goodreads_BestBooksEver_1-10000.csv
│   ├── database.db
│   ├── mf_model.pkl
│   └── tf_idf_model.pkl
├── nltk_dl.py
├── portal.py
├── previous codes
│   └── feedback_orgin.py
├── readme.md
├── requirements.txt
├── search_algorithm_page.py
├── static
│   ├── css
│   │   ├── bootstrap.min.css
│   │   └── login.css
│   ├── favicon.ico
│   └── js
│       └── bootstrap.bundle.js
└── templates
    ├── index.html
    ├── login.html
    └── register.html
```

