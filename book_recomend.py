import pandas as pd


def load_data(file_path):
    ratings = pd.read_csv('Downloads/ratings_cleaned.csv')
    ratings = ratings[ratings['Book-Rating']!=0]
    books = pd.read_csv('Downloads/books_cleaned.csv')
    return books, ratings

def get_readers(df_books, df_ratings, name_of_book = None, name_of_author = None):
    dataset = pd.merge(df_ratings, df_books, on=['ISBN'])
    dataset_lowercase = dataset[['User-ID', 'Book-Title', 'Book-Author', 'Book-Rating']]
    dataset_lowercase['Book-Title'] = dataset_lowercase['Book-Title'].str.lower()
    dataset_lowercase['Book-Author'] = dataset_lowercase['Book-Author'].str.lower()
    if name_of_book is not None:
        if name_of_author is not None:
            readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title'] == name_of_book) & (dataset_lowercase['Book-Author'].str.contains(name_of_author))].tolist()
        else:
            readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title'] == name_of_book)].tolist()
    elif name_of_author is not None:
        readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Author'] == name_of_author)].tolist()
    else:
        return None

    books_of_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(readers))]
    number_of_rating_per_book = books_of_readers.groupby(['Book-Title']).agg('count').reset_index()
    books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
    books_to_compare = books_to_compare.tolist()

    ratings_data_raw = books_of_readers[['User-ID', 'Book-Rating', 'Book-Title']][books_of_readers['Book-Title'].isin(books_to_compare)]
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()
    ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()
    dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
    return dataset_for_corr, ratings_data_raw


def recomendation_v1(readers_books, ratings_data_raw, book_name):
    dataset_of_other_books = readers_books.copy(deep=False)
    dataset_of_other_books.drop(book_name, axis=1, inplace=True)

    book_titles = dataset_of_other_books.columns.tolist()

    correlations = []
    avgrating = []

    for book_title in list(dataset_of_other_books.columns.values):
        correlations.append(readers_books[book_name].corr(dataset_of_other_books[book_title]))
        tab = ratings_data_raw[ratings_data_raw['Book-Title'] == book_title]
        avgrating.append(tab['Book-Rating'].min())
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)), columns=['book', 'corr', 'avg_rating'])
    corr_fellowship.head()

    result_list = (corr_fellowship.sort_values('corr', ascending=False).head(10))
    worst_list = (corr_fellowship.sort_values('corr', ascending=False).tail(10))
    return result_list, worst_list

df_books, df_ratings = load_data("Downloads/")
name_of_book = 'the fellowship of the ring (the lord of the rings, part 1)'
dataset_corr, ratings_data_raw  = get_readers(df_books, df_ratings, name_of_book = name_of_book)
result_list, worst_list = recomendation_v1(dataset_corr, ratings_data_raw, name_of_book)
