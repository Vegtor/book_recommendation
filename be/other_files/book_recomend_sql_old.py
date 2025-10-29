import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://book_owner:book_pass@localhost:5432/book_db"
engine = create_engine(DATABASE_URL)


def recomendation_sql(book_name):
    query_name = text("""SELECT * FROM find_book_by_name(:book_name, 0.3)""")
    with engine.connect() as conn:
        book_name = pd.read_sql(query_name, conn, params={"book_name": book_name})
    if book_name.empty or book_name is None:
        print(f"Book {book_name} not found")
        return None
    book_name = book_name.iloc[0]['title']

    query_avg = text("""SELECT user_id, book_title, avg_rating FROM get_avg_ratings_for_books_of_readers(:book_name)""")
    with engine.connect() as conn:
        df_corr = pd.read_sql(query_avg, conn, params={"book_name": book_name})

    if df_corr.empty or df_corr is None:
        print(f"No usable data for recomendation for book {book_name}")
        return None
    df_corr = df_corr.pivot(index='user_id', columns='book_title', values='avg_rating')

    dataset_of_other_books = df_corr.copy(deep=False)
    dataset_of_other_books.drop(book_name, axis=1, inplace=True)

    book_titles = dataset_of_other_books.columns.tolist()

    correlations = []
    avg_rating = []

    for book_title in book_titles:
        correlations.append(df_corr[book_name].corr(dataset_of_other_books[book_title]))
        avg_rating.append(df_corr[book_title].mean())
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avg_rating)), columns=['book', 'corr', 'avg_rating'])
    result_list = (corr_fellowship.sort_values('corr', ascending=False).head(10))
    worst_list = (corr_fellowship.sort_values('corr', ascending=False).tail(10))
    return result_list, worst_list

def recomendation_sql_v2(book_name):
    query_name = text("""SELECT * FROM find_book_by_name_id(:book_name, 0.2)""")
    with engine.connect() as conn:
        book_id = pd.read_sql(query_name, conn, params={"book_name": book_name})
    if book_id.empty:
        print(f"Book {book_name} not found")
        return None
    book_id = int(book_id.iloc[0]['book_id'])

    query_avg = text("""SELECT user_id, book_id, avg_rating FROM get_avg_ratings_for_books_of_readers_id(:book_id)""")
    with engine.connect() as conn:
        df_corr = pd.read_sql(query_avg, conn, params={"book_id": book_id})
    if df_corr.empty:
        print(f"No usable data for recomendation for book {book_name}")
        return None
    df_corr = df_corr.pivot(index='user_id', columns='book_id', values='avg_rating')

    dataset_of_other_books = df_corr.copy(deep=False)
    dataset_of_other_books.drop(book_id, axis=1, inplace=True)
    books_ids = dataset_of_other_books.columns.tolist()

    correlations = []
    avg_rating = []

    for id_of_book in books_ids:
        correlations.append(df_corr[book_id].corr(dataset_of_other_books[id_of_book]))
        avg_rating.append(df_corr[id_of_book].mean())
    corr_fellowship = pd.DataFrame(list(zip(books_ids, correlations, avg_rating)),
                                   columns=['book', 'corr', 'avg_rating'])
    result_list = corr_fellowship.sort_values('corr', ascending=False).head(10)

    query_all_info = text("""SELECT * FROM get_all_info_id(:book_id, 8)""")
    with engine.connect() as conn:
        df_all_info = pd.read_sql(query_all_info, conn, params={"book_id": book_id})

    result = result_list.merge(df_all_info, left_on='book', right_on='book_id', how='left')
    result.drop(columns=['book'], inplace=True)
    return result
