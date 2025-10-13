import { useState } from "react";
import "./BookGrid.css";

export default function BookGrid({ books }) {
    const [currentPage, setCurrentPage] = useState(1);
    const booksPerPage = 6;

    const totalPages = Math.ceil(books.length / booksPerPage);
    const startIndex = (currentPage - 1) * booksPerPage;
    const currentBooks = books.slice(startIndex, startIndex + booksPerPage);

    return (
        <div>
            <h3>Recommended books:</h3>
            <div className="grid-container">
                {currentBooks.map((book) => (
                    <div key={book.id} className="grid-item">
                        <img src={book.url_m} alt={book.book_name} />
                        <h4>{book.book_name}</h4>
                        <p><b>Author:</b> {book.book_author}</p>
                        <p><b>Publisher:</b> {book.publisher}</p>
                        <p><b>Year:</b> {book.year}</p>
                        <p><b>ISBN:</b> {book.book_isbn}</p>
                        <p><b>Rating: </b>{book.avg_rating}/10</p>
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
