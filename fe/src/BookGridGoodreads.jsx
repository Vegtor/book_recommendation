import { useState } from "react";
import "./BookGrid.css";

export default function BookGridGoodreads({ books }) {
    const [currentPage, setCurrentPage] = useState(1);
    const booksPerPage = 6;

    const totalPages = Math.ceil(books.length / booksPerPage);
    const startIndex = (currentPage - 1) * booksPerPage;
    const currentBooks = books.slice(startIndex, startIndex + booksPerPage);

    return (
        <div>
            <h3>Recommended Books:</h3>
            <div className="grid-container">
                {currentBooks.map((book) => (
                    <div key={book.book_id} className="grid-item">
                        <img src={book.url_m} alt={book.book_name} />
                        <h4>{book.book_name}</h4>
                        {book.original_title && book.original_title !== book.book_name && (
                            <p className="original-title"><i>Original: {book.original_title}</i></p>
                        )}
                        <p><b>Author:</b> {book.book_author || 'Not Specified'}</p>
                        <p><b>Year:</b> {book.year || 'Not Specified'}</p>
                        <p><b>Language:</b> {book.language_code || 'N/A'}</p>
                        <p><b>ISBN:</b> {book.book_isbn || 'Not Specified'}</p>
                        <p><b>Average Rating:</b> {book.average_rating?.toFixed(2)} ({book.ratings_count?.toLocaleString()} ratings)</p>

                        <div className="recommendation-scores">
                            <p><b>Hybrid Score:</b> {book.hybrid_score?.toFixed(4)}</p>
                            <p><b>Collaborative:</b> {book.collab_score?.toFixed(4)}</p>
                            <p><b>Tag Similarity:</b> {book.tag_score?.toFixed(4)}</p>
                            <p><b>To-Read Score:</b> {book.to_read_score?.toFixed(4)}</p>
                        </div>

                    </div>
                ))}
            </div>

            <div className="pagination">
                <button
                    onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <span>
                    {currentPage} / {totalPages}
                </span>
                <button
                    onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
                    disabled={currentPage === totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    );
}