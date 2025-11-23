# test_recommender.py
from recommender_model import recommend_books, get_similar_books

# --- Тест персональных рекомендаций ---
user_id_example = 1  # возьми существующего пользователя из базы
recommended = recommend_books(user_id_example, n=5)

print("=== Персональные рекомендации ===")
for book in recommended:
    print(f"{book['id']} - {book['title']}")

# --- Тест похожих книг ---
book_id_example = 3  # возьми существующую книгу из базы
similar_books = get_similar_books(book_id_example, n=5)

print("\n=== Похожие книги ===")
for book in similar_books:
    print(f"{book['id']} - {book['title']}")
