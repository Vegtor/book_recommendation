import "./App.css";

export function SearchedBook({ book }) {
    return (
        <div className="searched-book">
            <h3>Book you searched for:</h3>
            <div className="searched-book-card">
                <img src={book.url_m} alt={book.book_name} />
                <div>
                    <h4>{book.book_name}</h4>
                    <p><b>Author:</b> {book.book_author}</p>
                    <p><b>Publisher:</b> {book.publisher}</p>
                    <p><b>Year:</b> {book.year}</p>
                    <p><b>ISBN:</b> {book.isbn}</p>
                </div>
            </div>
        </div>
    );
}

export function SearchedBookGoodreads({ book }) {
    return (
        <div className="searched-book">
            <h3>Book you searched for:</h3>
            <div className="searched-book-card">
                <img src={book.url_m} alt={book.book_name} />
                <div>
                    <h4>{book.book_name}</h4>
                    {book.original_title && book.original_title !== book.book_name && (
                        <p className="original-title"><i>Original: {book.original_title}</i></p>
                    )}
                    <p><b>Author:</b> {book.book_author}</p>
                    <p><b>Year:</b> {book.year}</p>
                    <p><b>Language:</b> {book.language_code || 'N/A'}</p>
                    <p><b>ISBN:</b> {book.book_isbn}</p>
                    <p><b>Average Rating:</b> {book.average_rating?.toFixed(2)}</p>
                    <p><b>Ratings Count:</b> {book.ratings_count?.toLocaleString()}</p>
                </div>
            </div>
        </div>
    );
}