# recommender_model_v2.py
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

# -------------------------
#  Загрузка данных
# -------------------------
with open("interaction_matrix.pkl", "rb") as f:
    interaction_matrix = pickle.load(f)

with open("user_mapping.pkl", "rb") as f:
    user_mapping = pickle.load(f)

with open("copy_mapping.pkl", "rb") as f:
    copy_mapping = pickle.load(f)

inverse_copy_mapping = {v: k for k, v in copy_mapping.items()}

with open("book_genres_matrix.pkl", "rb") as f:
    book_genres_matrix = pickle.load(f)

similarity_matrix = cosine_similarity(book_genres_matrix)

# подключение к базе
engine = create_engine("sqlite:///library.db")
books = pd.read_sql("SELECT * FROM books", engine)
book_copies = pd.read_sql("SELECT id, book_id FROM book_copies", engine)
copy_to_book = book_copies.set_index('id')['book_id'].to_dict()

# -------------------------
#  Персональные рекомендации
# -------------------------
def recommend_books_personalized(user_id, n=5, alpha=0.7):
    if user_id not in user_mapping:
        return []

    user_idx = user_mapping[user_id]

    # коллаборативная фильтрация на уровне копий
    similarity = cosine_similarity(interaction_matrix)
    user_scores_cf = similarity[user_idx] @ interaction_matrix
    user_scores_cf = user_scores_cf / (similarity[user_idx].sum() + 1e-6)

    # контентная фильтрация на уровне книг
    user_interactions = interaction_matrix[user_idx]
    read_copy_idx = np.where(user_interactions > 0)[0]
    read_book_ids = [copy_to_book[inverse_copy_mapping[idx]] for idx in read_copy_idx]

    content_scores = pd.Series(0, index=books['id'])
    for book_id in read_book_ids:
        if book_id in book_genres_matrix.index:
            idx = book_genres_matrix.index.get_loc(book_id)
            sim_scores = pd.Series(similarity_matrix[idx], index=book_genres_matrix.index)
            content_scores = content_scores.add(sim_scores, fill_value=0)

    if len(read_book_ids) > 0:
        content_scores /= len(read_book_ids)

    # объединяем CF и контент
    cf_scores = pd.Series(user_scores_cf, index=[copy_to_book[inverse_copy_mapping[i]] for i in range(len(user_scores_cf))])
    combined_scores = alpha * cf_scores.groupby(cf_scores.index).max() + (1 - alpha) * content_scores

    # исключаем уже прочитанные книги
    combined_scores[read_book_ids] = 0

    # топ-n
    top_books = combined_scores.nlargest(n).index
    return books[books["id"].isin(top_books)].to_dict(orient="records")

# -------------------------
#  Похожие книги
# -------------------------
def get_similar_books_personalized(book_id, n=5, author_boost=0.3):
    if book_id not in book_genres_matrix.index:
        book_id = book_genres_matrix.index[0]

    # индекс книги в матрице жанров
    book_idx = book_genres_matrix.index.get_loc(book_id)
    similarity_scores = similarity_matrix[book_idx].copy()

    # буст книг того же автора (только книги в book_genres_matrix)
    target_author = books.loc[books['id'] == book_id, 'author'].values[0]
    books_in_matrix = books[books['id'].isin(book_genres_matrix.index)]
    author_mask = (books_in_matrix['author'] == target_author).values

    # mapping book_id -> индекс в similarity_scores
    id_to_idx = {bid: i for i, bid in enumerate(book_genres_matrix.index)}
    for i, bid in enumerate(books_in_matrix['id']):
        if bid in id_to_idx and author_mask[i]:
            similarity_scores[id_to_idx[bid]] += author_boost

    # топ-N
    similar_idx = np.argsort(-similarity_scores)[1:n+1]
    similar_book_ids = book_genres_matrix.index[similar_idx]

    return books[books["id"].isin(similar_book_ids)].to_dict(orient="records")

# -------------------------
# Пример работы
# -------------------------
if __name__ == "__main__":
    user_example = list(user_mapping.keys())[0]
    book_example = books['id'].iloc[0]

    print("\nПерсональные рекомендации:")
    recs = recommend_books_personalized(user_example, n=5)
    print(pd.DataFrame(recs))

    print("\nПохожие книги:")
    similar = get_similar_books_personalized(book_example, n=5)
    print(pd.DataFrame(similar))
