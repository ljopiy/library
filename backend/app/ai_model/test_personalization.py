# test_personalization.py
from recommender_model import recommend_books_personalized, get_similar_books_personalized
from recommender_model import user_mapping, books

# -------------------------
#  Тест персональных рекомендаций
# -------------------------
print("=== Персональные рекомендации ===")
user_ids = list(user_mapping.keys())[:5]  # первые 5 пользователей

for uid in user_ids:
    recs = recommend_books_personalized(uid, n=5)
    print(f"\n--- Пользователь {uid} ---")
    for book in recs:
        print(f"{book['id']} - {book['title']} - {book['author']}")

# -------------------------
# 2Тест похожих книг
# -------------------------
print("\n=== Похожие книги ===")
book_ids = books['id'].head(3).tolist()  # первые 3 книги из таблицы

for bid in book_ids:
    similar = get_similar_books_personalized(bid, n=5)
    print(f"\n--- Книга {bid} ({books.loc[books['id']==bid, 'title'].values[0]}) ---")
    for book in similar:
        print(f"{book['id']} - {book['title']} - {book['author']}")
