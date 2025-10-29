# import
import pandas as pd
import numpy as np

ratings = pd.read_csv('Downloads/BX-Book-Ratings.csv', encoding='cp1251', sep=',')
ratings = ratings[ratings['Book-Rating'] != 0]

books = pd.read_csv('Downloads/BX-Books.csv', encoding='cp1251', sep=';', error_bad_lines=False)
# error_bad_lines is deprecated, will show a warning in recent pandas versions

dataset = pd.merge(ratings, books, on=['ISBN'])
dataset_lowercase = dataset.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)
# applying str.lower to the whole dataframe may be slow for large datasets; could select only necessary columns

tolkien_readers = dataset_lowercase['User-ID'][
    (dataset_lowercase['Book-Title'] == 'the fellowship of the ring (the lord of the rings, part 1)') & (
        dataset_lowercase['Book-Author'].str.contains("tolkien"))]

tolkien_readers = tolkien_readers.tolist()
tolkien_readers = np.unique(tolkien_readers)

books_of_tolkien_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(tolkien_readers))]

number_of_rating_per_book = books_of_tolkien_readers.groupby(['Book-Title']).agg('count').reset_index()
# agg('count') counts all columns, better to count 'User-ID'

books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
books_to_compare = books_to_compare.tolist()
ratings_data_raw = books_of_tolkien_readers[['User-ID', 'Book-Rating', 'Book-Title']][books_of_tolkien_readers['Book-Title'].isin(books_to_compare)]

ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()
#works, but might be unnecessary if dataset already has no duplicates

ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
# pivot may create lots of NaNs; could use fillna or sparse structures for memory efficiency

LoR_list = ['the fellowship of the ring (the lord of the rings, part 1)']

result_list = []
worst_list = []

for LoR_book in LoR_list:

    dataset_of_other_books = dataset_for_corr.copy(deep=False)
    dataset_of_other_books.drop([LoR_book], axis=1, inplace=True)
    #deep=False is risky; changes could propagate; better to explicitly copy if modifying

    book_titles = []
    correlations = []
    avgrating = []

    for book_title in list(dataset_of_other_books.columns.values):
        book_titles.append(book_title)
        correlations.append(dataset_for_corr[LoR_book].corr(dataset_of_other_books[book_title]))
        tab = (ratings_data_raw[ratings_data_raw['Book-Title'] == book_title].groupby(ratings_data_raw['Book-Title']).mean())
        #groupby here is redundant since tab has only one book; inefficient
        avgrating.append(tab['Book-Rating'].min())
        #min() of a single value is redundant; could just take the value


    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)),
                                   columns=['book', 'corr', 'avg_rating'])
    corr_fellowship.head()
    #head() does nothing here

    result_list.append(corr_fellowship.sort_values('corr', ascending=False).head(10))

    worst_list.append(corr_fellowship.sort_values('corr', ascending=False).tail(10))

print("Correlation for book:", LoR_list[0])
rslt = result_list[0]
