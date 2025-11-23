# recommender.py
import pandas as pd
from sqlalchemy import create_engine
from recommender_model import recommend_books_personalized, get_similar_books_personalized, user_mapping, book_genres_matrix, books

# -------------------------
# Подключение к базе
# -------------------------
engine = create_engine("sqlite:///library.db")
users = pd.read_sql("SELECT * FROM user", engine)

# -------------------------
# Персональные рекомендации
# -------------------------
user_example = list(user_mapping.keys())[0]  # первый пользователь
print("\nПерсональные рекомендации для пользователя:")
recs = recommend_books_personalized(user_example, n=5)
print(pd.DataFrame(recs))

# -------------------------
# Похожие книги
# -------------------------
# Берём первую книгу, которая точно есть в book_genres_matrix
if not book_genres_matrix.empty:
    book_example = book_genres_matrix.index[0]
    similar_books = get_similar_books_personalized(book_example, n=5)
    print("\nПохожие книги для книги:")
    print(pd.DataFrame(similar_books))
else:
    print("\nНет книг с жанрами для теста похожих книг.")
