import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://book_owner:book_pass@localhost:5432/book_db"
engine = create_engine(DATABASE_URL)

def recomendation_sql(book_name):
    query_avg = text("""SELECT user_id, book_title, avg_rating FROM get_avg_ratings_for_books_of_readers(:book_name)""")
    with engine.connect() as conn:
        df_corr = pd.read_sql(query_avg, conn, params={"book_name": book_name})

    if df_corr.empty:
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
    return corr_fellowship.head()

neco = recomendation_sql("1984")
k = 5