import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://book_owner:book_pass@localhost:5432/book_db"
engine = create_engine(DATABASE_URL)

def recomendation_sql_v3(book_name, author=None, book_publisher=None, year_pb=None, isbn=None):
    query = text("""SELECT * FROM find_book_by_info_id(:book_name, :search_author, :search_publisher, :search_year, :search_isbn, 0.3)""")

    with engine.connect() as conn:
        book_id_df = pd.read_sql(
            query,
            conn,
            params={
                "book_name": book_name,
                "search_author": author,
                "search_publisher": book_publisher,
                "search_year": year_pb,
                "search_isbn": isbn
            }
        )

    if book_id_df.empty or book_id_df is None:
        raise Exception(-1, "No book found for this search query")
    book_id = int(book_id_df.iloc[0]['book_id'])

    query_searched_book = text("""SELECT b."Book-Title"  AS book_name,
                                         b."Book-Author" AS book_author,
                                         b."Publisher"   AS publisher,
                                         b."Year-Of-Publication" AS year, b."ISBN" AS isbn, b."Image-URL-M" AS url_m
                                  FROM books b
                                  WHERE b."id" = :book_id""")
    with engine.connect() as conn:
        searched_book = pd.read_sql(query_searched_book, conn, params={"book_id": book_id})

    query_avg = text("""SELECT user_id, book_id, avg_rating FROM get_avg_ratings_for_books_of_readers_id(:book_id)""")
    with engine.connect() as conn:
        df_corr = pd.read_sql(query_avg, conn, params={"book_id": book_id})
    if df_corr.empty or df_corr is None:
        return searched_book, []
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
    return searched_book, result

a , b = recomendation_sql_v3('1984')
k = 5
