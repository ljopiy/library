import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True)


async def read_table(query: str) -> pd.DataFrame:
    async with engine.connect() as conn:
        result = await conn.execute(text(query))
        rows = result.mappings().all()
        return pd.DataFrame(rows)


# --- Загружаем таблицы асинхронно ---
async def load_data():
    users = await read_table("SELECT * FROM user")
    books = await read_table("SELECT * FROM books")
    orders = await read_table("SELECT * FROM orders")
    order_copies_association = await read_table("SELECT * FROM order_copies_association")
    book_genres = await read_table("SELECT * FROM book_genre_association")

    return users, books, orders, order_copies_association, book_genres


# --- Основная инициализация ---
async def prepare_models():
    global books, interaction_matrix, user_mapping, inverse_copy_mapping
    global book_genres_matrix, similarity_matrix

    users, books, orders, order_copies_association, book_genres = await load_data()

    interactions = orders.merge(order_copies_association, left_on='id', right_on='order_id')
    interactions = interactions[['user_id', 'copy_id']]
    interactions['interaction'] = 1

    user_mapping = {uid: i for i, uid in enumerate(interactions['user_id'].unique())}
    copy_mapping = {cid: i for i, cid in enumerate(interactions['copy_id'].unique())}

    num_users = len(user_mapping)
    num_copies = len(copy_mapping)

    interaction_matrix = np.zeros((num_users, num_copies))
    for _, row in interactions.iterrows():
        interaction_matrix[user_mapping[row['user_id']], copy_mapping[row['copy_id']]] = 1

    inverse_copy_mapping = {v: k for k, v in copy_mapping.items()}

    # --- жанры ---
    if not book_genres.empty:
        book_genres_matrix = (
            pd.get_dummies(book_genres.set_index('book_id')['genre_id'])
            .groupby(level=0)
            .max()
        )
        similarity_matrix = cosine_similarity(book_genres_matrix)
    else:
        book_genres_matrix = pd.DataFrame()
        similarity_matrix = np.array([])


# --- Рекомендации ---
def recommend_books_personalized(user_id: int, n: int = 5):
    if user_id not in user_mapping:
        return []

    user_idx = user_mapping[user_id]
    similarity = cosine_similarity(interaction_matrix)
    user_scores = similarity[user_idx] @ interaction_matrix
    user_scores /= (similarity[user_idx].sum() + 1e-6)

    user_interactions = interaction_matrix[user_idx]
    user_scores[user_interactions > 0] = 0

    top_copy_idx = np.argsort(-user_scores)[:n]
    top_copy_ids = [inverse_copy_mapping[i] for i in top_copy_idx]

    return books[books["id"].isin(top_copy_ids)].to_dict(orient="records")


def get_similar_books_personalized(book_id: int, n: int = 5):
    if book_id not in book_genres_matrix.index:
        if not book_genres_matrix.empty:
            book_id = book_genres_matrix.index[0]
        else:
            return []

    book_idx = book_genres_matrix.index.get_loc(book_id)
    similarity_scores = similarity_matrix[book_idx]
    similar_idx = np.argsort(-similarity_scores)[1:n + 1]
    similar_book_ids = book_genres_matrix.index[similar_idx]

    return books[books["id"].isin(similar_book_ids)].to_dict(orient="records")
